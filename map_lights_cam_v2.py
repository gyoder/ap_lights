import pygame
import pygame.camera
import cv2
from time import sleep
import socket
import numpy as np



def init_network(host = '192.168.0.79', port = 50007):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # this is what the documentation said
    s.connect((host, port)) # connect to the rpi. the rpi's ip is the default
    return s

def request_light(device, light):
    device.send(str(light).encode()) # the socket send function needs binary data
    print('sent request for image', light) # debug statments: remove in final product
    sleep(.5) # this is to give the lights enough time to turn on with network
    print('slept')# delay. it can be much lower but it could cause problems so be careful

def save_image(device, light):
    image = device.get_image()     # pygame cannot import into opencv
    print('took image for', light)          # so i need to save it to a file
    pygame.image.save(image, 'led.png') # this is very janky but it will
    print('saved image for', light)         # have to do because i cant fix it

def get_bright(image):
    grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #greyscale image for faster procesing
    grey_image_blur = cv2.GaussianBlur(grey_image,(15,15),cv2.BORDER_DEFAULT)
    #the image is blured ^^ to make sure there are no false positives for a different point
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(grey_image_blur) #find values for birgtest
    return maxLoc, maxVal # return the values to check to see if they are too high

def main():
    pygame.init()
    pygame.camera.init() #init pygame
    #camera on pygame only works with linux so you need to pull the camera from /dev
    video_input = pygame.camera.Camera('/dev/video0', (1280,720), 'RGB')
    video_input.start()

    rpi = init_network() # get the rpi connect
    cords = [[0, 0, -1]]
    for i in range(50): # there are 50 lights so this is how to get them
        maxVal = 0
        # the maxVal is to make sure its not too dark. the lights get bright so it is fine
        while (maxVal < 200):
            request_light(rpi, i)
            save_image(video_input, i)
            (maxLoc, maxVal) = get_bright(cv2.imread('led.png'))
            #there has to be a cleaner way to do this where i dont have the
            #same code twice in a row, but this check is nessasary
            while (maxLoc[0] == cords[-1][0]) or (maxLoc[1] == cords[-1][1]):
                request_light(rpi, i)
                save_image(video_input, i)
                (maxLoc, maxVal) = get_bright(cv2.imread('led.png'))
        cords.append([maxLoc[0], maxLoc[1], i]) #put the cordinates on the list
    cords.pop(0)
    print(cords)

main()
