# Weather ETL Pipeline & Analytics Dashboard

Sistema de ingeniería de datos que extrae información meteorológica en tiempo real de 5 ciudades españolas, la transforma, almacena en una base de datos local y en un Data Warehouse, y la visualiza en un dashboard interactivo. El pipeline se ejecuta automáticamente cada hora.

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
  warehouse.py       ← DuckDB Data Warehouse + analytics views
        ↓
  dashboard.py       ← Streamlit + Plotly (visualization)
```

## Features

- Extrae datos meteorológicos en tiempo real para Madrid, Barcelona, Sevilla, Valencia y Bilbao
- Limpia y estructura los datos con Pandas
- Persiste registros en SQLite con modo append (historial completo)
- Se ejecuta automáticamente cada hora con logs de ejecución
- Data Warehouse local con DuckDB con vistas analíticas
- Dashboard interactivo con KPIs, gráficos, radar comparativo y tabla de datos

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
│   ├── extract.py           # API calls
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
├── warehouse.py             # DuckDB Data Warehouse
├── dashboard.py             # Streamlit dashboard
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

Crea un archivo `.env` en la raíz:
```
API_KEY=your_openweathermap_api_key
```

Obtén tu clave gratuita en [openweathermap.org](https://openweathermap.org/api).

## Usage

### Run the pipeline once
```bash
python main.py
```

### Run with hourly automation
```bash
python scheduler.py
```

### Run the Data Warehouse
```bash
python warehouse.py
```

### Launch the dashboard
```bash
streamlit run dashboard.py
```

## Roadmap

- [x] Modular ETL pipeline (Python + SQLite)
- [x] Interactive analytics dashboard (Streamlit + Plotly)
- [x] Hourly automation (APScheduler)
- [x] Local Data Warehouse (DuckDB)
- [ ] Expand to world capitals
- [ ] Cloud deployment

## Author

**Abderrahim** — Data Engineering portfolio project  
GitHub: [github.com/abderrahimhtml](https://github.com/abderrahimhtml)