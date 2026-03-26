from src.transform import transform_weather

def test_transform_returns_dataframe():
    mock_data = {
        "name": "Madrid",
        "sys": {"country": "ES"},
        "main": {"temp": 20.0, "feels_like": 19.0, "humidity": 60},
        "weather": [{"description": "despejado"}],
        "wind": {"speed": 3.5}
    }

    df = transform_weather(mock_data)

    assert len(df) == 1
    assert df["ciudad"][0] == "Madrid"
    assert "temperatura" in df.columns
    print("Test pasadp!")

if __name__ == "__main__":
    test_transform_returns_dataframe()
'''

---

'''