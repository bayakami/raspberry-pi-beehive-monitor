import csv
import glob
import os
import time

from datetime import datetime
from statistics import median
from hx711 import HX711


# Configuration
CSV_FILE = "data/hive1_combined.csv"
ZERO_FILE = "data/weight_zero.txt"

UNITS_PER_GRAM = 20.44
INTERVAL_SECONDS = 1800  # 30 minutes


# Initialise temperature sensor
device_folder = glob.glob('/sys/bus/w1/devices/28-*')[0]
device_file = device_folder + '/w1_slave'


def read_temp():
    with open(device_file, "r") as f:
        lines = f.readlines()

    while lines[0].strip()[-3:] != "YES":
        time.sleep(0.2)
        with open(device_file, "r") as f:
            lines = f.readlines()

    equals_pos = lines[1].find("t=")

    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        return float(temp_string) / 1000.0


# Initialise weight sensor
hx = HX711(dout_pin=5, pd_sck_pin=6)
hx.reset()

# Load permanent calibration
with open(ZERO_FILE, "r") as f:
    ZERO = float(f.read().strip())

print(f"Weight calibration loaded: {ZERO:.1f}")


def read_weight():

    samples = []

    for _ in range(5):
        readings = hx.get_raw_data()
        samples.append(sum(readings) / len(readings))
        time.sleep(0.2)

    raw = median(samples)

    weight_g = (raw - ZERO) / UNITS_PER_GRAM

    # Reject physically implausible readings
    if abs(weight_g) > 100000:
        print(f"Suspicious weight reading: {weight_g:.1f} g")
        return None

    return weight_g / 1000.0


def save_reading(reading):

    file_exists = os.path.exists(CSV_FILE)

    with open(CSV_FILE, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)

        if not file_exists or os.path.getsize(CSV_FILE) == 0:
            writer.writerow([
                "timestamp",
                "temperature",
                "weight_kg"
            ])

        writer.writerow([
            reading["timestamp"],
            reading["temperature"],
            reading["weight_kg"]
        ])


def main():

    os.makedirs("data", exist_ok=True)

    print("Beehive monitoring started!")
    print("Collecting temperature and weight every 30 minutes.")

    try:
        while True:

            timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            temperature = read_temp()
            weight = read_weight()

            reading = {
                "timestamp": timestamp,
                "temperature": round(temperature, 2),
                "weight_kg": round(weight, 3) if weight is not None else None
            }

            save_reading(reading)

            print(reading)

            time.sleep(INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\nBeehive monitoring stopped.")


if __name__ == "__main__":
    main()
