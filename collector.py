import csv
import glob
import os
import time


device_folder = glob.glob('/sys/bus/w1/devices/28-*')[0]
device_file = device_folder + '/w1_slave'

CSV_FILE = "data/hive1.csv"


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


def get_timestamp():
    return time.strftime("%d-%m-%Y %H:%M:%S")


def save_reading(reading):
    file_exists = os.path.exists(CSV_FILE)

    with open(CSV_FILE, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)

        if not file_exists:
            writer.writerow(["timestamp", "temperature"])

        writer.writerow([
            reading["timestamp"],
            reading["temperature"]
        ])


def main():
    while True:
        reading = {
            "timestamp": get_timestamp(),
            "temperature": read_temp()
        }

        save_reading(reading)

        print(reading)

        time.sleep(60)


if __name__ == "__main__":
    main()
