import os
import shutil
import yaml
import cv2
import numpy as np
import matplotlib.pyplot as plt
from ultralytics import YOLO
import random

random.seed(821)
np.random.seed(821)

dataset_path = os.path.dirname(os.path.realpath(__file__))

train_path = f"{dataset_path}/dataset/train"
val_path = f"{dataset_path}/dataset/val"

data_yaml = {
    "path": dataset_path,
    "train": "dataset/train/images",
    "val": "dataset/val/images",
    "nc": 2,  # 클래스 개수
    "names": ["school_uniform", "training"]
}


with open(f"{dataset_path}/dataset/data.yaml", "w") as f:
    yaml.dump(data_yaml, f)

if __name__ == "__main__": 
    model = YOLO("yolo11n.pt")

    results = model.train(
        data=f"{dataset_path}/dataset/data.yaml",
        epochs=100,
        imgsz=640, 
        batch=32,
        workers=2,
        device=0,
        project=f"{dataset_path}/runs",
        name="check_uniform",
        save=True,  # 학습 결과 저장 여부
        lr0=0.1,  # 초기 Learning Rate 설정
        patience=10,  # Early Stopping 적용 (10 epoch 동안 개선 없으면 종료)
        optimizer="AdamW",  # AdamW 최적화 적용 (기본값: SGD)
        verbose=True  # 학습 진행 로그 출력
    )

    metrics = model.val()