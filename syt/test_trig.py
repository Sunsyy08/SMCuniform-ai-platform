# test_trig.py
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

GPIO.output(23, 1)
time.sleep(0.5)
GPIO.output(23, 0)
