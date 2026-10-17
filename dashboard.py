from flask import Flask, render_template
import csv
from datetime import datetime, timedelta

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
    with open("data/hive1.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        readings = list(reader)

    latest = readings[-1]

    temperatures = [float(reading["temperature"]) for reading in readings]

    minimum = min(temperatures)
    maximum = max(temperatures)

    now = datetime.now()
    twenty_four_hours_ago = now - timedelta(hours=24)

    recent_readings = []

    for reading in readings:
        timestamp = datetime.strptime(
            reading["timestamp"],
            "%d-%m-%Y %H:%M:%S"
        )

        if timestamp >= twenty_four_hours_ago:
            recent_readings.append(reading)

    return render_template(
        "dashboard.html",
        temperature=latest["temperature"],
        timestamp=latest["timestamp"],
        minimum=minimum,
        maximum=maximum,
        reading_count=len(readings),
        readings=recent_readings
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
