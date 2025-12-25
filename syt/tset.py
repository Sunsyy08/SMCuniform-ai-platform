import torch, torchvision
print("Torch:", torch.__version__)
print("Torchvision:", torchvision.__version__)
print("CUDA 사용 가능:", torch.cuda.is_available())