import smtplib
import os
import duckdb
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")
DUCKDB_PATH = Path("data/weather_warehouse.duckdb")

TEMP_MAX = 35.0
TEMP_MIN = -5.0
HUMIDITY_MAX = 90


def check_alerts():
    conn = duckdb.connect(str(DUCKDB_PATH))
    df = conn.execute("SELECT * FROM latest_weather").df()
    conn.close()

    alerts = []

    for _, row in df.iterrows():
        city = row["ciudad"]
        temp = row["temperatura"]
        humidity = row["humedad"]

        if temp >= TEMP_MAX:
            alerts.append(f"🔴 CALOR EXTREMO — {city}: {temp:.1f}°C (límite: {TEMP_MAX}°C)")
        if temp <= TEMP_MIN:
            alerts.append(f"🔵 FRÍO EXTREMO — {city}: {temp:.1f}°C (límite: {TEMP_MIN}°C)")
        if humidity >= HUMIDITY_MAX:
            alerts.append(f"💧 HUMEDAD EXTREMA — {city}: {humidity}% (límite: {HUMIDITY_MAX}%)")

    return alerts


def send_email(alerts: list):
    if not alerts:
        print("Sin alertas activas.")
        return

    subject = f"⚠️ Weather Alert — {len(alerts)} alertas detectadas"
    body = "Se han detectado las siguientes condiciones extremas:\n\n"
    body += "\n".join(alerts)
    body += "\n\nGlobal Weather ETL Pipeline"

    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, EMAIL_TO, msg.as_string())

    print(f"Email enviado con {len(alerts)} alertas.")


if __name__ == "__main__":
    alerts = check_alerts()
    for a in alerts:
        print(a)
    send_email(alerts)