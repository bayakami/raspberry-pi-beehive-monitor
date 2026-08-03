from flask import Flask
import csv
from datetime import datetime

app = Flask(__name__)

CSV_FILE = "data/hive1.csv"


def get_readings():
    with open(CSV_FILE, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def get_latest_reading(readings):
    return readings[-1]


def get_today_temperatures(readings):
    today = datetime.now().strftime("%d-%m-%Y")

    temperatures = []

    for reading in readings:
        if reading["timestamp"].startswith(today):
            temperatures.append(float(reading["temperature"]))

    return temperatures


@app.route("/")
def home():
    readings = get_readings()

    latest = get_latest_reading(readings)

    today_temperatures = get_today_temperatures(readings)

    if today_temperatures:
        minimum = min(today_temperatures)
        maximum = max(today_temperatures)
    else:
        minimum = "No data"
        maximum = "No data"

    return f"""
    <h1>🐝 Hive 1 Dashboard</h1>

    <h2>Current temperature: {latest['temperature']} °C</h2>

    <p>Last updated: {latest['timestamp']}</p>

    <hr>

    <h3>Today's statistics</h3>

    <p>Minimum: {minimum} °C</p>

    <p>Maximum: {maximum} °C</p>

    <p>Total readings stored: {len(readings)}</p>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
