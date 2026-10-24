"""Run the pipeline:  python src/weather_etl/main.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from extract import extract
from load import load
from transform import transform

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def main():
    print("1/3 Extract")
    raw = extract(PROJECT_ROOT / "data" / "raw")
    print("2/3 Transform")
    df = transform(raw)
    print(f"  {len(df)} rows")
    print("3/3 Load")
    path = load(df, PROJECT_ROOT / "data" / "output")
    print(f"  wrote {path}")


if __name__ == "__main__":
    main()
