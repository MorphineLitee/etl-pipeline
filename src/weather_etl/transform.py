"""TRANSFORM: turn nested API JSON into one clean, flat table."""
import pandas as pd


def transform(raw: list[dict]) -> pd.DataFrame:
    frames = []
    for item in raw:
        df = pd.DataFrame(item["daily"])  # columns: time, temperature_2m_max, ...
        df["city"] = item["city"]
        frames.append(df)
    df = pd.concat(frames, ignore_index=True)

    # rename to friendlier column names
    df = df.rename(columns={
        "time": "date",
        "temperature_2m_max": "temp_max_c",
        "temperature_2m_min": "temp_min_c",
        "precipitation_sum": "precipitation_mm",
    })

    # fix types, drop bad rows
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df = df.dropna(subset=["temp_max_c", "temp_min_c"]).drop_duplicates(["city", "date"])
    df["precipitation_mm"] = df["precipitation_mm"].fillna(0)

    # derive new columns
    df["temp_avg_c"] = ((df["temp_max_c"] + df["temp_min_c"]) / 2).round(1)
    df["temp_avg_f"] = (df["temp_avg_c"] * 9 / 5 + 32).round(1)
    df["is_rainy"] = df["precipitation_mm"] > 1

    return df[["city", "date", "temp_max_c", "temp_min_c", "temp_avg_c", "temp_avg_f",
               "precipitation_mm", "is_rainy"]].sort_values(["city", "date"])
