import pygame

file_path = "voice/세명컴퓨터고등학교 6.wav"

pygame.mixer.init()
pygame.mixer.music.load(file_path)
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():  # 재생 중일 때 계속 대기
    pass
