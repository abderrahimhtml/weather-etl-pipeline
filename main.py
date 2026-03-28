from src.extract import get_weather, CITIES
from src.transform import transform_weather
from src.load import load_to_db
import time

def run_pipeline():
    print(f"Iniciando pipeline ETL — {len(CITIES)} ciudades...")

    success = 0
    errors = 0

    for city in CITIES:
        try:
            print(f"Extrayendo {city}...")
            raw_data = get_weather(city)
            df = transform_weather(raw_data)
            load_to_db(df)
            success += 1
            time.sleep(1.2)
        except Exception as e:
            print(f"✗ Error en {city}: {e}")
            errors += 1

    print(f"\nPipeline completado: {success} ciudades OK, {errors} errores")

if __name__ == "__main__":
    run_pipeline()