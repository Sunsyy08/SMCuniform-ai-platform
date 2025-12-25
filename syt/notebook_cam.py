import cv2
from ultralytics import YOLO
from datetime import datetime
import os
import pygame
import random

# =======================
# 1️⃣ YOLO 모델 로드
# =======================
model_path = "runs/check_uniform3/weights/best.pt"  # 경로 수정
model = YOLO(model_path)

# O / X 음성 파일
o_file_path = [
    "voice/세명컴퓨터고등학교 2.wav",
    "voice/세명컴퓨터고등학교 4.wav",
    "voice/세명컴퓨터고등학교 7.wav"
]

x_file_path = [
    "voice/세명컴퓨터고등학교 3.wav",
    "voice/세명컴퓨터고등학교 5.wav",
    "voice/세명컴퓨터고등학교 6.wav"
]

# =======================
# 2️⃣ 저장 폴더 생성
# =======================
save_dir = "capture_img"
os.makedirs(save_dir, exist_ok=True)

# =======================
# 3️⃣ 노트북 웹캠 연결
# =======================
cap = cv2.VideoCapture(0)   # 0 = 기본 웹캠
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("❌ 웹캠을 열 수 없습니다!")
    exit()

print("📸 스페이스바 누르면 사진 촬영, ESC 누르면 종료")

# =======================
# 4️⃣ 실시간 화면 출력 & 촬영
# =======================
while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ 프레임을 읽을 수 없습니다!")
        break

    cv2.imshow("Webcam - Press SPACE to Capture", frame)

    key = cv2.waitKey(1)

    # ESC 종료
    if key == 27:
        break

    # 스페이스바 → 촬영
    if key == 32:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = os.path.join(save_dir, f"capture_{timestamp}.jpg")
        cv2.imwrite(save_path, frame)
        print(f"📸 사진 저장 완료: {save_path}")
        break

cap.release()
cv2.destroyAllWindows()

# =======================
# 5️⃣ YOLO 분석
# =======================
results = model(save_path, verbose=False)

uniform_detected = False

print("모델 클래스 이름:", model.names)

for result in results:
    boxes = result.boxes
    for box in boxes:
        class_id = int(box.cls[0].item())
        class_name = model.names[class_id]
        confidence = box.conf[0].item()
        print(f"👕 객체: {class_name}, 신뢰도: {confidence:.2f}")

        if class_name.lower() in ["school_uniform", "교복"] and confidence >= 0.5:
            uniform_detected = True

# =======================
# 6️⃣ 음성 출력
# =======================
pygame.mixer.init()

if uniform_detected:
    print("✅ 교복 착용")
    file_path = random.choice(o_file_path)
else:
    print("❌ 교복 미착용")
    file_path = random.choice(x_file_path)

pygame.mixer.music.load(file_path)
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pass
