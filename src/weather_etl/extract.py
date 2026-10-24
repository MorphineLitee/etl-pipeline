"""EXTRACT: pull raw weather data from the Open-Meteo API (free, no API key)."""
import json
from pathlib import Path

import requests

API_URL = "https://api.open-meteo.com/v1/forecast"

CITIES = {
    "Delhi": (28.61, 77.21),
    "Mumbai": (19.08, 72.88),
    "London": (51.51, -0.13),
    "New York": (40.71, -74.01),
}


def fetch_city(name: str, lat: float, lon: float) -> dict:
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",
        "forecast_days": 7,
    }
    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    data["city"] = name
    return data


def extract(raw_dir: Path) -> list[dict]:
    """Fetch every city and keep a copy of the raw JSON (good practice: never lose the source)."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for name, (lat, lon) in CITIES.items():
        data = fetch_city(name, lat, lon)
        (raw_dir / f"{name.lower().replace(' ', '_')}.json").write_text(json.dumps(data, indent=2))
        results.append(data)
        print(f"  extracted {name}")
    return results
