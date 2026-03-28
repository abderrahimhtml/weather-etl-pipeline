import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

CITIES = [
    "Madrid", "Barcelona", "Sevilla", "Valencia", "Bilbao",
    "London", "Paris", "Berlin", "Rome", "Madrid",
    "Tokyo", "Beijing", "Shanghai", "Mumbai", "Delhi",
    "New York", "Los Angeles", "Chicago", "Toronto", "Mexico City",
    "São Paulo", "Buenos Aires", "Lima", "Bogotá", "Santiago",
    "Cairo", "Lagos", "Nairobi", "Johannesburg", "Casablanca",
    "Moscow", "Istanbul", "Dubai", "Riyadh", "Tehran",
    "Bangkok", "Jakarta", "Singapore", "Kuala Lumpur", "Manila",
    "Seoul", "Sydney", "Melbourne", "Auckland", "Karachi",
    "Dhaka", "Colombo", "Kathmandu", "Islamabad", "Kabul"
]

def get_weather(city: str) -> dict:
    api_key = os.getenv("API_KEY")
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "es"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def extract_all() -> list:
    results = []
    for city in CITIES:
        try:
            data = get_weather(city)
            results.append(data)
            print(f"✓ {city}")
            time.sleep(1.2)  # Respetar límite API
        except Exception as e:
            print(f"✗ {city}: {e}")
    return results

if __name__ == "__main__":
    extract_all()