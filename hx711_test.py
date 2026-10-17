from hx711 import HX711
import time

hx = HX711(dout_pin=5, pd_sck_pin=6)

hx.reset()

print("HX711 test started")

while True:
    readings = hx.get_raw_data()
    average = sum(readings) / len(readings)

    print("Average raw reading:", average)

    time.sleep(1)
