# 🌍 Global Weather ETL Pipeline & Analytics Dashboard

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=flat&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![DuckDB](https://img.shields.io/badge/DuckDB-FFF000?style=flat&logo=duckdb&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Pytest](https://img.shields.io/badge/Tests-11%20passed-brightgreen?style=flat&logo=pytest&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success?style=flat)

Automated data engineering system that extracts real-time meteorological data from 50 major world cities, transforms and stores it in a local database and a Data Warehouse, exposes it through a REST API, and visualizes it in an interactive global dashboard. The pipeline runs automatically every hour with email alerts for extreme weather conditions.

---

## Screenshots

### Interactive Global Dashboard
![Dashboard - World Map](docs/screenshots/dashboard_map.png)
> Global temperature heatmap with Plotly scatter map — 50 cities across 6 continents.

### KPI Cards & Analytics Charts
![Dashboard - KPIs](docs/screenshots/dashboard_kpis.png)
> Real-time KPI cards, temperature radar chart, and humidity bar chart.

### REST API — Auto-generated Docs
![FastAPI Docs](docs/screenshots/api_docs.png)
> 8 endpoints with Swagger UI at `/docs`, generated automatically by FastAPI.

---

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
   api.py            ← FastAPI REST API (8 endpoints)
        ↓
  dashboard.py       ← Streamlit + Plotly (global visualization)
```

---

## Features

- Extracts live weather data for 50 major world cities across 6 continents
- Cleans and structures raw JSON with Pandas
- Persists all records in SQLite with append mode (full historical log)
- Runs automatically every hour via APScheduler with execution logs
- Local Data Warehouse with DuckDB including analytics views (hottest, coldest, most humid)
- REST API with FastAPI — 8 endpoints with auto-generated Swagger docs
- Email alerts via Gmail SMTP when extreme temperatures or humidity are detected
- Interactive global dashboard: KPI cards, radar chart, bar chart, world map, data table
- 11 automated tests with pytest covering ETL logic and API endpoints

---

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

---

## Project Structure

```
weather-etl-pipeline/
├── src/
│   ├── extract.py           # API calls (50 cities)
│   ├── transform.py         # Data transformation with Pandas
│   └── load.py              # SQLite persistence via SQLAlchemy
├── data/
│   ├── weather.db           # SQLite database
│   └── weather_warehouse.duckdb  # DuckDB Data Warehouse
├── logs/
│   ├── .gitkeep
│   └── pipeline.log         # Execution logs
├── tests/
│   └── test_pipeline.py     # 11 automated tests
├── scheduler.py             # Hourly automation + email alerts
├── warehouse.py             # DuckDB Data Warehouse + analytics views
├── api.py                   # FastAPI REST API
├── alerts.py                # Email alerts via Gmail SMTP
├── dashboard.py             # Streamlit global dashboard
├── main.py                  # Manual pipeline execution
├── .env                     # Credentials (not included in repo)
├── .gitignore
├── requirements.txt
└── README.md
```

---

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

Create a `.env` file in the root:
```
API_KEY=your_openweathermap_api_key
EMAIL_USER=your_gmail@gmail.com
EMAIL_PASSWORD=your_16_char_app_password
EMAIL_TO=your_gmail@gmail.com
```

> For Gmail, use an [App Password](https://myaccount.google.com/apppasswords), not your regular account password.

---

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
Swagger docs available at `http://127.0.0.1:8000/docs`

### Launch the dashboard
```bash
streamlit run dashboard.py
```

### Run tests
```bash
pytest tests/test_pipeline.py -v
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API info |
| GET | `/cities` | List all 50 cities |
| GET | `/weather` | Latest data for all cities |
| GET | `/weather/{city}` | Latest data for one city |
| GET | `/analytics/summary` | Average metrics per city |
| GET | `/analytics/hottest` | Top N hottest cities |
| GET | `/analytics/coldest` | Top N coldest cities |
| GET | `/analytics/most-humid` | Top N most humid cities |

---

## Cities Covered

**Europe:** Madrid, Barcelona, Sevilla, Valencia, Bilbao, London, Paris, Berlin, Rome, Moscow, Istanbul

**Asia:** Tokyo, Beijing, Shanghai, Mumbai, Delhi, Bangkok, Jakarta, Singapore, Kuala Lumpur, Manila, Seoul, Karachi, Dhaka, Colombo, Kathmandu, Islamabad, Kabul, Dubai, Riyadh, Tehran

**North America:** New York, Los Angeles, Chicago, Toronto, Mexico City

**South America:** São Paulo, Buenos Aires, Lima, Bogotá, Santiago

**Africa:** Cairo, Lagos, Nairobi, Johannesburg, Casablanca

**Oceania:** Sydney, Melbourne, Auckland

---

## Lessons Learned

**Separating concerns from the start saves time.** Splitting the pipeline into `extract.py`, `transform.py`, and `load.py` made debugging significantly easier. When an API call failed or a column was malformed, the problem was immediately isolated to one file instead of buried in a monolithic script.

**Cloud services have real friction for local development.** BigQuery and cloud warehouses like AWS were explored and ultimately dropped — not for technical reasons, but because unexpected billing and Python version incompatibilities created more risk than value at this stage. DuckDB provided equivalent analytical capability with zero infrastructure overhead.

**APScheduler over Airflow/Docker was the right tradeoff on Windows.** Airflow requires WSL2 or Docker, both of which introduced environment conflicts on Windows. APScheduler solved the automation requirement with a single dependency and no container overhead.

**Negative values break assumptions in visualization libraries.** `px.scatter_map` uses a `size` parameter that cannot accept zero or negative values. Cities with sub-zero temperatures caused silent failures. The fix — `.clip(lower=1)` — took seconds once the cause was identified, but finding it required understanding how Plotly handles size encoding internally.

**Environment isolation is non-negotiable.** A corrupted virtual environment mid-project caused a full reinstall. Root cause: the venv was created in a path with spaces. Moving the project to a clean path and recreating the venv resolved it immediately. Now: always create venvs in paths with no spaces.

**pytest forces you to write testable code.** Writing 11 tests after the fact required refactoring functions that had side effects baked in. If tests had been written earlier, the code architecture would have been cleaner from the beginning.

**`.gitignore` before the first commit.** The `.env` file containing API keys was almost pushed to GitHub on the first commit. It wasn't — but it was close. Adding `.gitignore` before any `git add` is now a non-negotiable first step.

---

## Roadmap

- [x] Modular ETL pipeline (Python + SQLite)
- [x] Interactive analytics dashboard (Streamlit + Plotly)
- [x] Hourly automation (APScheduler)
- [x] Local Data Warehouse (DuckDB)
- [x] Global expansion — 50 world cities
- [x] Interactive world map with temperature heatmap
- [x] REST API with FastAPI (8 endpoints)
- [x] Email alerts for extreme weather conditions
- [x] Automated tests with pytest (11/11 passing)
- [ ] Cloud deployment

---

## Author

**Abderrahim** — Data Engineering portfolio project  
GitHub: [github.com/abderrahimhtml](https://github.com/abderrahimhtml)