import sys
import os
import pytest
import duckdb
import pandas as pd
from pathlib import Path
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from api import app

client = TestClient(app)


# --- Tests API ---

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Global Weather API" in response.json()["message"]

def test_get_cities():
    response = client.get("/cities")
    assert response.status_code == 200
    data = response.json()
    assert "cities" in data
    assert data["total"] > 0

def test_get_all_weather():
    response = client.get("/weather")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_city_weather_valid():
    response = client.get("/weather/Madrid")
    assert response.status_code == 200
    data = response.json()
    assert data["ciudad"] == "Madrid"
    assert "temperatura" in data

def test_get_city_weather_invalid():
    response = client.get("/weather/CiudadQueNoExiste")
    assert response.status_code == 404

def test_get_hottest():
    response = client.get("/analytics/hottest?limit=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    temps = [d["temperatura"] for d in data]
    assert temps == sorted(temps, reverse=True)

def test_get_coldest():
    response = client.get("/analytics/coldest?limit=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    temps = [d["temperatura"] for d in data]
    assert temps == sorted(temps)

def test_get_summary():
    response = client.get("/analytics/summary")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "temp_media" in data[0]


# --- Tests ETL ---

def test_transform_output():
    from transform import transform_weather
    mock_raw = {
        "name": "TestCity",
        "sys": {"country": "TC"},
        "main": {"temp": 20.0, "feels_like": 19.0, "humidity": 50},
        "weather": [{"description": "cielo claro"}],
        "wind": {"speed": 3.0}
    }
    df = transform_weather(mock_raw)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df["ciudad"].iloc[0] == "TestCity"
    assert df["temperatura"].iloc[0] == 20.0

def test_duckdb_warehouse_exists():
    path = Path("data/weather_warehouse.duckdb")
    assert path.exists(), "El warehouse DuckDB no existe"

def test_duckdb_views():
    conn = duckdb.connect("data/weather_warehouse.duckdb")
    df = conn.execute("SELECT * FROM avg_temperature LIMIT 5").df()
    conn.close()
    assert len(df) > 0
    assert "ciudad" in df.columns