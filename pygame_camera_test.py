import pygame
import pygame.camera
import cv2
from time import sleep
import socket
import numpy as np


pygame.init()
pygame.camera.init() #get the camera working
video_input = pygame.camera.Camera('/dev/video0', (1280,720), 'RGB')
video_input.start()
image = video_input.get_image()
pygame.image.save(image, 'led.png')
