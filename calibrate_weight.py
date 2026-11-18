from hx711 import HX711
from statistics import median
import time
import os

hx = HX711(dout_pin=5, pd_sck_pin=6)
hx.reset()

print("Keep the platform completely empty.")
print("Taking calibration measurements...")

time.sleep(2)

readings_list = []

for _ in range(15):
    readings = hx.get_raw_data()
    average = sum(readings) / len(readings)
    readings_list.append(average)
    time.sleep(0.3)

zero = median(readings_list)

os.makedirs("data", exist_ok=True)

with open("data/weight_zero.txt", "w") as file:
    file.write(str(zero))

print(f"Calibration saved!")
print(f"Zero reading: {zero:.1f}")
