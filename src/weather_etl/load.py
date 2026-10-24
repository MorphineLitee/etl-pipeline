"""LOAD: write the clean data to a CSV file, and to Cloud Storage when a bucket is set."""
from pathlib import Path

import pandas as pd

CSV_NAME = "weather_forecast.csv"


def load(df: pd.DataFrame, out_dir: Path, bucket: str | None = None) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / CSV_NAME
    df.to_csv(path, index=False)
    if bucket:
        upload_to_gcs(path, bucket)
    return path


def upload_to_gcs(path: Path, bucket: str) -> None:
    # imported here so local runs do not need Google credentials
    from google.cloud import storage

    storage.Client().bucket(bucket).blob(path.name).upload_from_filename(
        str(path), content_type="text/csv"
    )
