import RPi.GPIO as gpio
import time

TRIGER = 24
ECHO = 23

gpio.setmode(gpio.BCM)
gpio.setup(TRIGER, gpio.OUT)
gpio.setup(ECHO, gpio.IN)

try:
    while True:
        # Trigger pulse
        gpio.output(TRIGER, gpio.LOW)
        time.sleep(0.05)
        gpio.output(TRIGER, gpio.HIGH)
        time.sleep(0.00001)  # 10µs
        gpio.output(TRIGER, gpio.LOW)

        # Wait for ECHO HIGH with timeout
        startTime = time.perf_counter()
        timeout = startTime + 0.02  # 20ms timeout
        while gpio.input(ECHO) == 0 and time.perf_counter() < timeout:
            pass
        startTime = time.perf_counter()

        # Wait for ECHO LOW with timeout
        timeout = time.perf_counter() + 0.02
        while gpio.input(ECHO) == 1 and time.perf_counter() < timeout:
            pass
        endTime = time.perf_counter()

        # Calculate distance
        period = endTime - startTime
        dist = period * 34300 / 2  # cm

        print("Distance: %.2f cm" % dist)

        time.sleep(0.2)

except KeyboardInterrupt:
    gpio.cleanup()
