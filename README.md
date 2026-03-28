# Global Weather ETL Pipeline & Analytics Dashboard

Automated data engineering system that extracts real-time meteorological data from the 50 most important cities in the world, transforms and stores it in a local database and a Data Warehouse, and exposes it through an interactive global dashboard. The pipeline runs automatically every hour.

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
  scheduler.py       ← APScheduler (hourly automation)
        ↓
  warehouse.py       ← DuckDB Data Warehouse + analytics views
        ↓
  dashboard.py       ← Streamlit + Plotly (global visualization)
```

## Features

- Extracts live weather data for 50 major world cities across 6 continents
- Cleans and structures data with Pandas
- Persists all records in SQLite with append mode (full historical log)
- Runs automatically every hour with execution logs
- Local Data Warehouse with DuckDB including analytics views
- Interactive global dashboard with KPIs, charts, world map and data table
- Filters by city and date range

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.14 |
| Extraction | OpenWeatherMap API + Requests |
| Transformation | Pandas |
| Storage | SQLite + SQLAlchemy |
| Data Warehouse | DuckDB |
| Automation | APScheduler |
| Visualization | Streamlit + Plotly |

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
│   └── test_pipeline.py
├── scheduler.py             # Hourly automation
├── warehouse.py             # DuckDB Data Warehouse + analytics views
├── dashboard.py             # Streamlit global dashboard
├── main.py                  # Manual pipeline execution
├── .env                     # API key (not included)
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

### 4. Configure API key

Create a `.env` file in the root directory:
```
API_KEY=your_openweathermap_api_key
```

Get your free key at [openweathermap.org](https://openweathermap.org/api).

## Usage

### Run the pipeline once
```bash
python main.py
```

### Run with hourly automation
```bash
python scheduler.py
```

The scheduler runs the pipeline immediately on start, then every hour automatically. Logs are saved to `logs/pipeline.log`.

### Update the Data Warehouse
```bash
python warehouse.py
```

### Launch the dashboard
```bash
streamlit run dashboard.py
```

## Cities Covered

**Europe:** Madrid, Barcelona, Sevilla, Valencia, Bilbao, London, Paris, Berlin, Rome

**Asia:** Tokyo, Beijing, Shanghai, Mumbai, Delhi, Bangkok, Jakarta, Singapore, Kuala Lumpur, Manila, Seoul, Karachi, Dhaka, Colombo, Kathmandu, Islamabad, Kabul, Dubai, Riyadh, Tehran

**North America:** New York, Los Angeles, Chicago, Toronto, Mexico City

**South America:** São Paulo, Buenos Aires, Lima, Bogotá, Santiago

**Africa:** Cairo, Lagos, Nairobi, Johannesburg, Casablanca

**Oceania:** Sydney, Melbourne, Auckland

**Europe/Asia:** Moscow, Istanbul

## Roadmap

- [x] Modular ETL pipeline (Python + SQLite)
- [x] Interactive analytics dashboard (Streamlit + Plotly)
- [x] Hourly automation (APScheduler)
- [x] Local Data Warehouse (DuckDB)
- [x] Global expansion — 50 world cities
- [x] Interactive world map with temperature heatmap
- [ ] Cloud deployment
- [ ] Historical trend analysis

## Author

**Abderrahim** — Data Engineering portfolio project  
GitHub: [github.com/abderrahimhtml](https://github.com/abderrahimhtml)