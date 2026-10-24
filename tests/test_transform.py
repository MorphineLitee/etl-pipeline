import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "weather_etl"))

from transform import transform


def sample(city="Delhi"):
    return {
        "city": city,
        "daily": {
            "time": ["2026-10-11", "2026-10-12"],
            "temperature_2m_max": [30.0, 32.0],
            "temperature_2m_min": [20.0, None],
            "precipitation_sum": [None, 2.5],
        },
    }


def test_transform_cleans_and_derives_columns():
    df = transform([sample()])
    assert len(df) == 1  # row with missing min temp is dropped
    row = df.iloc[0]
    assert row["temp_avg_c"] == 25.0
    assert row["temp_avg_f"] == 77.0
    assert row["precipitation_mm"] == 0  # missing precipitation becomes 0
    assert not row["is_rainy"]


def test_transform_combines_cities():
    df = transform([sample("Delhi"), sample("London")])
    assert set(df["city"]) == {"Delhi", "London"}
