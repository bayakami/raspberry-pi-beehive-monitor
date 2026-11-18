from flask import Flask, render_template
import csv
from datetime import datetime, timedelta
import os

app = Flask(__name__)

CSV_FILE = "data/hive1_combined.csv"


def get_readings():
    if not os.path.exists(CSV_FILE):
        return []

    with open(CSV_FILE, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        readings = list(reader)

    for reading in readings:
        reading["temperature"] = float(reading["temperature"])

        reading["weight_kg"] = (
            float(reading["weight_kg"])
            if reading["weight_kg"]
            else None
        )

    return readings


@app.route("/")
def home():

    readings = get_readings()

    if not readings:
        return "No sensor readings available yet."

    latest = readings[-1]

    temperatures = [
        reading["temperature"] for reading in readings
    ]

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

    # Calculate weight change over 24 hours
    valid_weights = [
        reading for reading in recent_readings
        if reading["weight_kg"] is not None
    ]

    weight_change = None

    if len(valid_weights) >= 2:
        weight_change = round(
            valid_weights[-1]["weight_kg"]
            - valid_weights[0]["weight_kg"],
            3
        )

    return render_template(
        "dashboard.html",
        temperature=latest["temperature"],
        weight_kg=latest["weight_kg"],
        weight_change=weight_change,
        timestamp=latest["timestamp"],
        minimum=minimum,
        maximum=maximum,
        reading_count=len(readings),
        readings=recent_readings
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
