import os
import json
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()

# Ruta a la clave JSON
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp-key.json"

# Leer el project_id desde la clave JSON
with open("gcp-key.json") as f:
    key_data = json.load(f)
    PROJECT_ID = key_data["project_id"]

DATASET_ID = "weather_raw"
TABLE_ID = "weather_data"

def load_to_bigquery(df):
    client = bigquery.Client(project=PROJECT_ID)
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND",
        autodetect=True
    )

    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()

    print(f"{len(df)} registros cargados en BigQuery → {table_ref}")

if __name__ == "__main__":
    import sys
    sys.path.insert(0, "src")
    from extract import get_weather
    from transform import transform_weather

    cities = ["Madrid", "Barcelona", "Sevilla", "Valencia", "Bilbao"]
    
    for city in cities:
        print(f"Procesando {city}...")
        raw = get_weather(city)
        df = transform_weather(raw)
        load_to_bigquery(df)

    print("Carga completa en BigQuery.")