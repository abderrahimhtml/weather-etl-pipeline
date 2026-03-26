from src.extract import get_weather
from src.transform import transform_weather
from src.load import load_to_db

CITIES = ["Madrid", "Barcelona", "Sevilla", "Valencia", "Bilbao"]

def run_pipeline():
    print("Iniciando pipeline ETL...")
    
    for city in CITIES:
        print(f"Extrayendo datos de {city}...")
        raw_data = get_weather(city)
        df = transform_weather(raw_data)
        load_to_db(df)
    
    print("Pipeline completado!")

if __name__ == "__main__":
    run_pipeline()