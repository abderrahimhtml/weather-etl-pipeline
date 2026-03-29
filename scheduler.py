import sys
import os
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/pipeline.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
sys.path.insert(0, os.path.dirname(__file__))

CITIES = ["Madrid", "Barcelona", "Sevilla", "Valencia", "Bilbao"]

def run_pipeline():
    logger.info("=== Iniciando pipeline ETL ===")
    try:
        from extract import get_weather
        from transform import transform_weather
        from load import load_to_db

        for city in CITIES:
            logger.info(f"Procesando {city}...")
            raw = get_weather(city)
            df = transform_weather(raw)
            load_to_db(df)
            logger.info(f"{city} guardada correctamente")

        logger.info("=== Pipeline completado con éxito ===")

        from alerts import check_alerts, send_email
        alerts = check_alerts()
        if alerts:
            send_email(alerts)
            logger.info(f"Alertas enviadas: {len(alerts)}")
        else:
            logger.info("Sin alertas activas.")

    except Exception as e:
        logger.error(f"Error en el pipeline: {e}")

if __name__ == "__main__":
    logger.info("Scheduler iniciado. El pipeline se ejecutará cada hora.")
    run_pipeline()

    scheduler = BlockingScheduler()
    scheduler.add_job(run_pipeline, "interval", hours=1)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler detenido.")