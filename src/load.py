import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///data/weather.db"

def load_to_db(df: pd.DataFrame, table_name: str = "weather_data"):
    engine = create_engine(DATABASE_URL)
    
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="append",
        index=False
    )
    print(f"{len(df)} registros guardados en '{table_name}'")

if __name__ == "__main__":
    from extract import get_weather
    from transform import transform_weather
    
    raw = get_weather("Madrid")
    df = transform_weather(raw)
    load_to_db(df)