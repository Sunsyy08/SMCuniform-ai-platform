from picamera2 import Picamera2
from ultralytics import YOLO
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from time import sleep
import os
from datetime import datetime
import pygame
import random

# =======================
# 1️⃣ YOLO 모델 로드
# =======================
model_path = "/media/smc/0F1A-0D21/syt/runs/check_uniform3/weights/best.pt"
model = YOLO(model_path)

o_file_path = ["voice/세명컴퓨터고등학교 2.wav",
             "voice/세명컴퓨터고등학교 4.wav",
             "voice/세명컴퓨터고등학교 7.wav"]   

x_file_path = ["voice/세명컴퓨터고등학교 3.wav",
             "voice/세명컴퓨터고등학교 5.wav",
             "voice/세명컴퓨터고등학교 6.wav"]

# =======================
# 2️⃣ LED Matrix 설정
# =======================
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1, block_orientation=90)

# O 패턴 (착용) / X 패턴 (미착용)
O_pattern = [
    (2,1),(3,1),(4,1),(5,1),
    (1,2),(6,2),
    (1,3),(6,3),
    (1,4),(6,4),
    (1,5),(6,5),
    (2,6),(3,6),(4,6),(5,6)
]

X_pattern = [
    (1,1),(6,1),
    (2,2),(5,2),
    (3,3),(4,3),
    (3,4),(4,4),
    (2,5),(5,5),
    (1,6),(6,6)
]

def draw_pattern(pattern):
    with canvas(device) as draw:
        for x, y in pattern:
            draw.point((x, y), fill=255)

# =======================
# 3️⃣ 카메라 설정
# =======================
save_dir = "/media/smc/0F1A-0D21/syt/capture_img"
os.makedirs(save_dir, exist_ok=True)

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()
sleep(2)  # 워밍업

# =======================
# 4️⃣ 사진 촬영
# =======================
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
save_path = os.path.join(save_dir, f"capture_{timestamp}.jpg")
print("📸 3초 후 사진 촬영...")
sleep(3)

picam2.capture_file(save_path)
picam2.stop()
print(f"✅ 사진 촬영 완료: {save_path}")

# =======================
# 5️⃣ AI 모델로 교복 판별
# =======================
results = model(save_path, verbose=False)

# 기본값: 미착용
uniform_detected = False

# YOLO 클래스 이름 확인
print("모델 클래스 이름:", model.names)

# 감지 결과 확인
for result in results:
    boxes = result.boxes
    for box in boxes:
        class_id = int(box.cls[0].item())
        class_name = model.names[class_id]
        confidence = box.conf[0].item()
        print(f"👕 객체: {class_name}, 신뢰도: {confidence:.2f}")
        # 교복 감지 시
        if class_name.lower() in ["school_uniform", "교복"] and confidence >= 0.5:
            uniform_detected = True

# =======================
# 6️⃣ LED에 표시
# =======================
if uniform_detected:
    print("✅ 교복 착용 감지됨 (O 표시)")
    draw_pattern(O_pattern)
    file_path = random.choice(o_file_path)
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():  # 재생 중일 때 계속 대기
        pass
else:
    print("❌ 교복 미착용 (X 표시)")
    draw_pattern(X_pattern)
    file_path = random.choice(x_file_path)
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():  # 재생 중일 때 계속 대기
        pass

os.remove(save_path)

# LED 표시 유지
sleep(5)
