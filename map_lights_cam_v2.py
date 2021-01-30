import pygame
import pygame.camera
import cv2
from time import sleep
import socket
import numpy as np
import math
from PIL import Image



def init_network(host = '192.168.0.79', port = 50007):
    #https://docs.python.org/3/library/socket.html#example
    #i did write the communication code but not the init code
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

def get_bright_old(image):
    #the majority of this code is taken from https://www.pyimagesearch.com/2014/09/29/finding-brightest-spot-image-using-python-opencv/
    grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #greyscale image for faster procesing
    grey_image_blur = cv2.GaussianBlur(grey_image,(15,15),cv2.BORDER_DEFAULT)
    #the image is blured ^^ to make sure there are no false positives for a different point
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(grey_image_blur) #find values for birgtest
    return maxLoc, maxVal # return the values to check to see if they are too high

def get_bright(image):
    npimage = np.array(image)
    xcord = 0
    ycord = 0
    red_cords = []
    for i in npimage:
        xcord += 1
        ycord = 0
        for j in i:
            ycord += 1
            contrast = (int(j[0]) - ((int(j[1]) + int(j[2])) / 2))
            if contrast > 150:
                red_cords.append((xcord, ycord, contrast))

    red_cords = np.array(red_cords)

    (locX, locY, contrast) = np.median(red_cords, axis=0) #https://numpy.org/doc/stable/reference/generated/numpy.median.html


    return locX, locY, contrast

def main():
    pygame.init()
    pygame.camera.init() #init pygame
    #camera on pygame only works with linux so you need to pull the camera from /dev
    video_input = pygame.camera.Camera('/dev/video0', (1280,720), 'RGB')
    video_input.start()

    rpi = init_network() # get the rpi connect
    cords = [[0, 0, -1]]
    sleep(5)
    for i in range(50): # there are 50 lights so this is how to get them
        contrast = 0
        # the maxVal is to make sure its not too dark. the lights get bright so it is fine
        while (contrast < 200):
            request_light(rpi, i)
            save_image(video_input, i)
            (locX, locY, contrast) = get_bright(Image.open('led.png'))
            #there has to be a cleaner way to do this where i dont have the
            #same code twice in a row, but this check is nessasary
            while (locX == cords[-1][0]) or (locY == cords[-1][1]):
                request_light(rpi, i)
                save_image(video_input, i)
                (locX, locY, contrast) = get_bright(Image.open('led.png'))
        cords.append((locX, locY, i)) #put the cordinates on the list
    cords.pop(0)
    print(cords)
    for i in range(48):
        cords[i+1].append((math.sqrt(((cords[i+1][0]-cords[i][0])**2) + ((cords[i+1][1]-cords[i][1])**2))) + (math.sqrt(((cords[i+1][0]-cords[i-1][0])**2) + ((cords[i][1]-cords[i-1][1])**2))))
    cords[0].append(cords[1][3])
    cords[49].append(cords[48][3])
    cordsdist = 0
    for i in cords:
        #print(i[3])
        cordsdist += i[3]
    cordsdist = cordsdist / 50
    print(cordsdist)
    print(cords)

main()
