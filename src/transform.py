import pandas as pd
from datetime import datetime

def transform_weather(raw_data: dict) -> pd.DataFrame:
    
    record = {
        "ciudad": raw_data["name"],
        "pais": raw_data["sys"]["country"],
        "temperatura": raw_data["main"]["temp"],
        "sensacion_termica": raw_data["main"]["feels_like"],
        "humedad": raw_data["main"]["humidity"],
        "descripcion": raw_data["weather"][0]["description"],
        "velocidad_viento": raw_data["wind"]["speed"],
        "fecha_extraccion": datetime.now()
    }
    
    return pd.DataFrame([record])

if __name__ == "__main__":
    from extract import get_weather
    raw = get_weather("Madrid")
    df = transform_weather(raw)
    print(df)