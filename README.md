# Weather ETL Pipeline

Pipeline de datos automatizado que extrae información meteorológica
de 5 ciudades españolas en tiempo real, la transforma y la almacena
en una base de datos SQL.

## Stack tecnológico
- **Python 3.11** — Lenguaje principal
- **Pandas** — Transformación de datos
- **SQLAlchemy** — Conexión a base de datos
- **SQLite** — Almacenamiento
- **OpenWeatherMap API** — Fuente de datos

## Arquitectura

API (OpenWeatherMap) → extract.py → transform.py → load.py → SQLite DB

## Cómo ejecutarlo

# 1. Clona el repositorio
git clone https://github.com/tuusuario/weather-etl-pipeline

# 2. Instala dependencias
pip install -r requirements.txt

# 3. Crea tu archivo .env con tu API key
echo "API_KEY=tu_clave" > .env

# 4. Ejecuta el pipeline
python main.py

## Próximas mejoras
- [ ] Añadir Airflow para automatizar la ejecución
- [ ] Dashboard con Streamlit
- [ ] Deploy en Docker