import duckdb
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

DUCKDB_PATH = Path("data/weather_warehouse.duckdb")

app = FastAPI(
    title="Global Weather API",
    description="REST API for real-time weather data from 50 world cities",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_conn():
    if not DUCKDB_PATH.exists():
        raise HTTPException(status_code=503, detail="Warehouse not available")
    return duckdb.connect(str(DUCKDB_PATH))


@app.get("/")
def root():
    return {"message": "Global Weather API", "version": "1.0.0", "docs": "/docs"}


@app.get("/cities")
def get_cities():
    """Lista todas las ciudades disponibles."""
    conn = get_conn()
    result = conn.execute("SELECT DISTINCT ciudad FROM raw_weather ORDER BY ciudad").fetchall()
    conn.close()
    return {"cities": [r[0] for r in result], "total": len(result)}


@app.get("/weather")
def get_all_weather():
    """Último registro de cada ciudad."""
    conn = get_conn()
    df = conn.execute("SELECT * FROM latest_weather ORDER BY ciudad").df()
    conn.close()
    return df.to_dict(orient="records")


@app.get("/weather/{city}")
def get_city_weather(city: str):
    """Datos del último registro de una ciudad específica."""
    conn = get_conn()
    df = conn.execute(
        "SELECT * FROM latest_weather WHERE LOWER(ciudad) = LOWER(?)", [city]
    ).df()
    conn.close()
    if df.empty:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found")
    return df.to_dict(orient="records")[0]


@app.get("/analytics/summary")
def get_summary():
    """Temperatura media, humedad y viento por ciudad."""
    conn = get_conn()
    df = conn.execute("SELECT * FROM avg_temperature").df()
    conn.close()
    return df.to_dict(orient="records")


@app.get("/analytics/hottest")
def get_hottest(limit: int = 5):
    """Las N ciudades más cálidas ahora mismo."""
    conn = get_conn()
    df = conn.execute(
        f"SELECT ciudad, temperatura, descripcion FROM latest_weather ORDER BY temperatura DESC LIMIT {limit}"
    ).df()
    conn.close()
    return df.to_dict(orient="records")


@app.get("/analytics/coldest")
def get_coldest(limit: int = 5):
    """Las N ciudades más frías ahora mismo."""
    conn = get_conn()
    df = conn.execute(
        f"SELECT ciudad, temperatura, descripcion FROM latest_weather ORDER BY temperatura ASC LIMIT {limit}"
    ).df()
    conn.close()
    return df.to_dict(orient="records")


@app.get("/analytics/most-humid")
def get_most_humid(limit: int = 5):
    """Las N ciudades con más humedad."""
    conn = get_conn()
    df = conn.execute(
        f"SELECT ciudad, humedad, descripcion FROM latest_weather ORDER BY humedad DESC LIMIT {limit}"
    ).df()
    conn.close()
    return df.to_dict(orient="records")