# 🌍 Global Weather ETL Pipeline & Analytics Dashboard

Automated data engineering system that extracts real-time meteorological data from the 50 most important cities in the world, transforms and stores it in a local database and a Data Warehouse, exposes it through a REST API, and visualizes it in an interactive global dashboard. The pipeline runs automatically every hour with email alerts for extreme conditions.

## Architecture
```
OpenWeatherMap API (50 world cities)
        ↓
   extract.py        ← HTTP requests, raw JSON
        ↓
  transform.py       ← Pandas cleaning & structuring
        ↓
    load.py          ← SQLAlchemy → SQLite
        ↓
  scheduler.py       ← APScheduler (hourly automation + alerts)
        ↓
  warehouse.py       ← DuckDB Data Warehouse + analytics views
        ↓
   api.py            ← FastAPI REST API
        ↓
  dashboard.py       ← Streamlit + Plotly (global visualization)
```

## Features

- Extracts live weather data for 50 major world cities across 6 continents
- Cleans and structures data with Pandas
- Persists all records in SQLite with append mode (full historical log)
- Runs automatically every hour with execution logs
- Local Data Warehouse with DuckDB including analytics views
- REST API with FastAPI — 8 endpoints with auto-generated docs
- Email alerts via Gmail when extreme temperatures or humidity detected
- Interactive global dashboard with KPIs, charts, world map and data table
- 11 automated tests with pytest

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.14 |
| Extraction | OpenWeatherMap API + Requests |
| Transformation | Pandas |
| Storage | SQLite + SQLAlchemy |
| Data Warehouse | DuckDB |
| Automation | APScheduler |
| API | FastAPI + Uvicorn |
| Alerts | Gmail SMTP |
| Visualization | Streamlit + Plotly |
| Testing | Pytest |

## Project Structure
```
weather-etl-pipeline/
├── src/
│   ├── extract.py           # API calls (50 cities)
│   ├── transform.py         # Data transformation
│   └── load.py              # SQLite persistence
├── data/
│   ├── weather.db           # SQLite database
│   └── weather_warehouse.duckdb  # DuckDB Data Warehouse
├── logs/
│   └── pipeline.log         # Execution logs
├── tests/
│   └── test_pipeline.py     # 11 automated tests
├── scheduler.py             # Hourly automation + alerts
├── warehouse.py             # DuckDB Data Warehouse
├── api.py                   # FastAPI REST API
├── alerts.py                # Email alerts (Gmail)
├── dashboard.py             # Streamlit global dashboard
├── main.py                  # Manual pipeline execution
├── .env                     # Credentials (not included)
├── requirements.txt
└── README.md
```

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/abderrahimhtml/weather-etl-pipeline
cd weather-etl-pipeline
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
.\venv\Scripts\activate        # Windows
source venv/bin/activate       # Linux / macOS
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure credentials

Create a `.env` file in the root directory:
```
API_KEY=your_openweathermap_api_key
EMAIL_USER=your_gmail@gmail.com
EMAIL_PASSWORD=your_16_char_app_password
EMAIL_TO=your_gmail@gmail.com
```

## Usage

### Run the pipeline once
```bash
python main.py
```

### Run with hourly automation
```bash
python scheduler.py
```

### Update the Data Warehouse
```bash
python warehouse.py
```

### Launch the REST API
```bash
uvicorn api:app --reload
```
API docs available at `http://127.0.0.1:8000/docs`

### Launch the dashboard
```bash
streamlit run dashboard.py
```

### Run tests
```bash
pytest tests/test_pipeline.py -v
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API info |
| GET | `/cities` | List all cities |
| GET | `/weather` | Latest data for all cities |
| GET | `/weather/{city}` | Latest data for one city |
| GET | `/analytics/summary` | Average metrics per city |
| GET | `/analytics/hottest` | Top N hottest cities |
| GET | `/analytics/coldest` | Top N coldest cities |
| GET | `/analytics/most-humid` | Top N most humid cities |

## Cities Covered

**Europe:** Madrid, Barcelona, Sevilla, Valencia, Bilbao, London, Paris, Berlin, Rome, Moscow, Istanbul

**Asia:** Tokyo, Beijing, Shanghai, Mumbai, Delhi, Bangkok, Jakarta, Singapore, Kuala Lumpur, Manila, Seoul, Karachi, Dhaka, Colombo, Kathmandu, Islamabad, Kabul, Dubai, Riyadh, Tehran

**North America:** New York, Los Angeles, Chicago, Toronto, Mexico City

**South America:** São Paulo, Buenos Aires, Lima, Bogotá, Santiago

**Africa:** Cairo, Lagos, Nairobi, Johannesburg, Casablanca

**Oceania:** Sydney, Melbourne, Auckland

## Roadmap

- [x] Modular ETL pipeline (Python + SQLite)
- [x] Interactive analytics dashboard (Streamlit + Plotly)
- [x] Hourly automation (APScheduler)
- [x] Local Data Warehouse (DuckDB)
- [x] Global expansion — 50 world cities
- [x] Interactive world map with temperature heatmap
- [x] REST API with FastAPI
- [x] Email alerts for extreme conditions
- [x] Automated tests with pytest (11/11)
- [ ] Cloud deployment

## Author

**Abderrahim** — Data Engineering portfolio project  
GitHub: [github.com/abderrahimhtml](https://github.com/abderrahimhtml)