FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/

ENV PYTHONUNBUFFERED=1
# Cloud Run sets $PORT (default 8080)
CMD exec uvicorn api:app --app-dir src/weather_etl --host 0.0.0.0 --port ${PORT:-8080}
