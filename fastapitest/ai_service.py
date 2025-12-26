from ultralytics import YOLO
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

MODEL_PATH = os.path.join(
    ROOT_DIR,
    "syt",
    "runs",
    "check_uniform3",
    "weights",
    "best.pt"
)

model = None  # 🔥 여기 중요

def load_model():
    global model
    if model is None:
        model = YOLO(MODEL_PATH)
    return model

def detect_uniform(image_path: str) -> bool:
    model = load_model()
    results = model(image_path, verbose=False)

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            confidence = float(box.conf[0])

            if class_name.lower() in ["school_uniform", "교복"] and confidence >= 0.5:
                return True

    return False
