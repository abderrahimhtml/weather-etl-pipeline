import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_weather(city: str) -> dict:
    api_key = os.getenv("API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "es"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    data = get_weather("Madrid")
    print(data)