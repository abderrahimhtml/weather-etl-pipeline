import duckdb
import sqlite3
import pandas as pd

SQLITE_PATH = "data/weather.db"
DUCKDB_PATH = "data/weather_warehouse.duckdb"

def extract_from_sqlite():
    conn = sqlite3.connect(SQLITE_PATH)
    df = pd.read_sql("SELECT * FROM weather_data", conn)
    conn.close()
    print(f"Extraídos {len(df)} registros de SQLite")
    return df

def load_to_duckdb(df):
    conn = duckdb.connect(DUCKDB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS raw_weather (
            ciudad VARCHAR,
            pais VARCHAR,
            temperatura FLOAT,
            sensacion_termica FLOAT,
            humedad INTEGER,
            descripcion VARCHAR,
            velocidad_viento FLOAT,
            fecha_extraccion TIMESTAMP
        )
    """)

    conn.execute("DELETE FROM raw_weather")
    conn.execute("INSERT INTO raw_weather SELECT * FROM df")

    print(f"{len(df)} registros cargados en DuckDB")
    conn.close()

def create_analytics_views():
    conn = duckdb.connect(DUCKDB_PATH)

    conn.execute("""
        CREATE OR REPLACE VIEW avg_temperature AS
        SELECT
            ciudad,
            ROUND(AVG(temperatura), 2) AS temp_media,
            ROUND(AVG(sensacion_termica), 2) AS sensacion_media,
            ROUND(AVG(humedad), 2) AS humedad_media,
            ROUND(AVG(velocidad_viento), 2) AS viento_medio
        FROM raw_weather
        GROUP BY ciudad
        ORDER BY temp_media DESC
    """)

    conn.execute("""
        CREATE OR REPLACE VIEW latest_weather AS
        SELECT *
        FROM raw_weather
        QUALIFY ROW_NUMBER() OVER (
            PARTITION BY ciudad
            ORDER BY fecha_extraccion DESC
        ) = 1
    """)

    print("Vistas analíticas creadas correctamente")
    conn.close()

def show_summary():
    conn = duckdb.connect(DUCKDB_PATH)
    print("\n--- Temperatura media por ciudad ---")
    print(conn.execute("SELECT * FROM avg_temperature").df().to_string(index=False))
    print("\n--- Último registro por ciudad ---")
    print(conn.execute("SELECT ciudad, temperatura, descripcion, fecha_extraccion FROM latest_weather").df().to_string(index=False))
    conn.close()

if __name__ == "__main__":
    df = extract_from_sqlite()
    load_to_duckdb(df)
    create_analytics_views()
    show_summary()