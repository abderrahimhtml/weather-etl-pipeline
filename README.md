# Real-Time Weather ETL Pipeline & Analytics Dashboard (V2)

A comprehensive data engineering project that automates the lifecycle of meteorological data from ingestion to interactive visualization. This system monitors real-time weather conditions across major Spanish cities, leveraging a modular ETL architecture.

## Project Evolution
What began as a backend ETL script has evolved into a full-scale **Data Application**. The current version features:
* **Geospatial Analytics:** Interactive maps for regional trend monitoring.
* **Visual Context:** Real-time weather iconography integration.
* **Relational Persistence:** Robust SQL storage for historical time-series analysis.

## Technical Stack
* **Language:** Python 3.11
* **Data Orchestration:** Pandas (Transformation & Cleaning)
* **Database Layer:** SQLAlchemy (ORM) & SQLite
* **Visualization:** Streamlit & Plotly (Real-time Dashboard)
* **API Ingestion:** OpenWeatherMap API

## System Architecture
The pipeline follows a modular ETL (Extract, Transform, Load) design:
`API (Source) ➔ extract.py ➔ transform.py ➔ load.py ➔ SQLite (Storage) ➔ Streamlit (Data Product)`

---

## Installation & Execution

Follow these steps to deploy the environment and run the application locally.

### 1. Environment Setup
Clone the repository and install the required dependencies:
```bash
git clone [https://github.com/abderrahimhtml/weather-etl-pipeline](https://github.com/abderrahimhtml/weather-etl-pipeline)
cd weather-etl-pipeline
pip install -r requirements.txt