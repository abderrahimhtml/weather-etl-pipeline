# Weather ETL Pipeline & Analytics Dashboard

Automated data engineering system that extracts real-time meteorological data from 5 Spanish cities, transforms and stores it in a local database, and exposes it through an interactive dashboard. The pipeline runs automatically every hour via a built-in scheduler.

## Architecture
```
OpenWeatherMap API
        ↓
   extract.py        ← HTTP requests, raw JSON
        ↓
  transform.py       ← Pandas cleaning & structuring
        ↓
    load.py          ← SQLAlchemy → SQLite
        ↓
  scheduler.py       ← APScheduler (hourly automation)
        ↓
  dashboard.py       ← Streamlit + Plotly (visualization)
```

## Features

- Extracts live weather data for Madrid, Barcelona, Sevilla, Valencia and Bilbao
- Cleans and structures data with Pandas
- Persists records in SQLite with append mode (full historical log)
- Runs automatically every hour with execution logs
- Interactive dashboard with KPIs, charts, radar comparison and data table

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.14 |
| Extraction | OpenWeatherMap API + Requests |
| Transformation | Pandas |
| Storage | SQLite + SQLAlchemy |
| Automation | APScheduler |
| Visualization | Streamlit + Plotly |

## Project Structure
```
weather-etl-pipeline/
├── src/
│   ├── extract.py       # API calls
│   ├── transform.py     # Data transformation
│   └── load.py          # Database persistence
├── data/
│   └── weather.db       # SQLite database
├── logs/
│   └── pipeline.log     # Execution logs
├── tests/
│   └── test_pipeline.py
├── scheduler.py         # Hourly automation
├── dashboard.py         # Streamlit dashboard
├── .env                 # API key (not included)
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

### Launch the dashboard
```bash
streamlit run dashboard.py
```

## Roadmap

- [x] Modular ETL pipeline (Python + SQLite)
- [x] Interactive analytics dashboard (Streamlit + Plotly)
- [x] Hourly automation (APScheduler)
- [ ] Cloud Data Warehouse (dbt + AWS/GCP)

## Author

**Abderrahim** — Data Engineering portfolio project  
GitHub: [github.com/abderrahimhtml](https://github.com/abderrahimhtml)