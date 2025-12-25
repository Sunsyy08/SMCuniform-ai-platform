import time
import board
import digitalio
from adafruit_hcsr04 import HCSR04

# GPIO 핀 설정
sensor = HCSR04(trigger_pin=board.D23, echo_pin=board.D24)

print("HC-SR04 거리 측정 시작...")
try:
    while True:
        try:
            distance = sensor.distance
            print(f"거리: {distance:.1f} cm")
        except RuntimeError:
            print("거리 측정 실패")
        time.sleep(1)

except KeyboardInterrupt:
    print("측정 종료")
