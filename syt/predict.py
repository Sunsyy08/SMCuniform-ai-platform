from ultralytics import YOLO
import torch

model = YOLO(r"/media/smc/0F1A-0D21/syt/runs/check_uniform3/weights/best.pt") #

# 테스트할 이미지 경로 설정
image_path = r"/media/smc/0F1A-0D21/syt/syt.JPG"

# 이미지에 대한 추론 실행
# 'verbose=False' 설정으로 기본 콘솔 출력을 줄이고 결과 객체에 집중할 수 있습니다.
results = model(image_path, verbose=False) 

# 결과 프린트 및 처리
for result in results:
    # 탐지된 객체들의 바운딩 박스 정보를 가져옵니다.
    # GPU 사용 시 .cpu()를 사용하여 numpy 배열로 변환해야 할 수 있습니다.
    boxes = result.boxes
    
    for box in boxes:
        # 바운딩 박스 좌표 (xyxy 형식: xmin, ymin, xmax, ymax)
        coordinates = box.xyxy[0].tolist() 
        
        # 신뢰도 점수
        confidence = box.conf[0].item()
        
        # 클래스 ID
        class_id = box.cls[0].item()
        
        # 클래스 이름 (모델의 names 속성 사용)
        class_name = model.names[class_id]
        
        # 결과 프린트
        print(f"객체: {class_name}, 신뢰도: {confidence:.2f}, 좌표 (xyxy): {coordinates}")