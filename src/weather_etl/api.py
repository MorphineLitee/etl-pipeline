"""HTTP API around the ETL pipeline.

Run:  uvicorn api:app --reload     (from src/weather_etl)
Docs: http://127.0.0.1:8000/docs
"""
import os
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, Response

from extract import extract
from load import CSV_NAME, load
from transform import transform

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_DIR = PROJECT_ROOT / "data" / "output"
CSV_PATH = OUTPUT_DIR / CSV_NAME
GCS_BUCKET = os.environ.get("GCS_BUCKET")  # set on Cloud Run; unset = local files only

app = FastAPI(title="Weather ETL API")
_run_lock = threading.Lock()  # the pipeline writes shared files, so one run at a time


def run_pipeline() -> int:
    """Extract -> transform -> load. Returns the number of rows written."""
    with _run_lock:
        try:
            raw = extract(RAW_DIR)
        except requests.RequestException as exc:
            raise HTTPException(status_code=502, detail=f"Upstream API failed: {exc}")
        df = transform(raw)
        load(df, OUTPUT_DIR, bucket=GCS_BUCKET)
        return len(df)


@app.get("/health")
def health():
    try:
        return {"status": "ok"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Health check failed: {exc}")


@app.post("/run")
def run():
    """Fetch fresh data from the third party, transform it, and rebuild the CSV."""
    try:
        rows = run_pipeline()
        return {"rows": rows, "csv": "/forecast.csv"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Pipeline run failed: {exc}")

@app.get("/forecast.csv")
def forecast_csv(refresh: bool = False):
    """Download the CSV. Runs the pipeline first if `refresh=true` or no CSV exists yet."""
    headers = {"Content-Disposition": f'attachment; filename="{CSV_NAME}"'}
    if GCS_BUCKET:
        from google.cloud import storage

        blob = storage.Client().bucket(GCS_BUCKET).blob(CSV_NAME)
        if refresh or not blob.exists():
            run_pipeline()
        return Response(blob.download_as_bytes(), media_type="text/csv", headers=headers)
    if refresh or not CSV_PATH.exists():
        run_pipeline()
    return FileResponse(CSV_PATH, media_type="text/csv", filename=CSV_NAME)
