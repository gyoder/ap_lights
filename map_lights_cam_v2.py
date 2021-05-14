import pygame
import pygame.camera
import cv2
from time import sleep
import socket
import numpy as np
import math
from PIL import Image
import sys
import os

def init_network(host = '192.168.0.79', port = 50007):
    #https://docs.python.org/3/library/socket.html#example
    #i did write the communication code but not the init code
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # this is what the documentation said
    s.connect((host, port)) # connect to the rpi. the rpi's ip is the default
    return s

def request_light(device, light):
    device.send(str(light).encode()) # the socket send function needs binary data
    print('sent request for image', light) # debug statments: remove in final product
    sleep(.25) # this is to give the lights enough time to turn on with network
    #print('slept')# delay. it can be much lower but it could cause problems so be careful

def save_image(device, light):
    image = device.get_image()     # pygame cannot import into opencv
    #print('took image for', light)          # so i need to save it to a file
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
    npimage = np.array(image) #make the image a numpy array for raw data processing
    high_con_points = find_brightness_points(npimage)
    while len(high_con_points) == 0:
        return (0, 0, 0)

    high_con_points = sorted(high_con_points, key = lambda x: x[2]) #https://www.geeksforgeeks.org/python-sort-list-according-second-element-sublist/
    # ^^ sorts it by brighness
    high_con_points = np.array(high_con_points)
    (locX, locY, brighness) = np.mean(high_con_points, axis=0) #https://numpy.org/doc/stable/reference/generated/numpy.median.html
    return locX, locY, brighness

def find_contrast_points(img_array): # returns a list of high contrast points
    xcord = 0
    high_con_points = []
    for i in img_array:
        xcord += 1 #this is a bit bad. make it read what idderation its on
        ycord = 0# reset each time
        for j in i:
            ycord += 1
            contrast = (int(j[0]) - ((int(j[1]) + int(j[2])) / 2))# find the contrast between red and blue/green
            if contrast > 150:# might want to make this more reasonable
                high_con_points.append((xcord, ycord, contrast))
    return high_con_points

def find_brightness_points(img_array):
    xcord = 0
    high_brightness_points = []
    for i in img_array:
        xcord += 1
        ycord = 0# reset each time
        for j in i:
            ycord += 1
            brighness = (int(j[0]) + int(j[1]) + int(j[2])) / 3 # find the brighness
            if brighness > 240:
                high_brightness_points.append((xcord, ycord, brighness))
    return high_brightness_points

def get_cords(led, prev_loc, net_dev, video_input): # returns tuple containing xcords and ycords and the led
    #moved to a recursive function to make logging more verbose
    request_light(net_dev, led)
    save_image(video_input, led)
    (locX, locY, brighness) = get_bright(Image.open('led.png'))
    if (brighness < 200): # if it is too dark
        print('brighness is too small')
        return get_cords(led, prev_loc, net_dev, video_input)
    elif (locX == prev_loc[0]) or (locY == prev_loc[1]): #if it is the same location
        print('Same location detected')
        return get_cords(led, prev_loc, net_dev, video_input)
    else:
        return [round(locX), round(locY), led]



def main():
    pygame.init()
    pygame.camera.init() #init pygame
    #camera on pygame only works with linux so you need to pull the camera from /dev
    input('Plug In Your Camera. Press ENTER or RETURN to continue')

    camlist = pygame.camera.list_cameras()
    for i in camlist: # loop through camera list so it doesnt just fail
        try:
            video_input = pygame.camera.Camera(i, (1280,720), 'RGB')
            video_input.start()
            break # grabs first camera that works
        except:
            sys.stderr.write('ERROR: camera ' +  str(i) + ' Failed To Start\n')
            video_input = False # this is probably a bad idea but it might work

    if not video_input:
        sys.stderr.write('ERROR: Cameras Failed To Initalised: EXITING\n')
        exit()

    #video_input.start()


    #video_input = pygame.camera.Camera('/dev/video0', (1280,720), 'RGB')
    #video_input.start()
    try:
        rpi = init_network() # get the rpi connect
    except:
        sys.stderr.write('make sure the pi server is up first\nERROR: network failed to connect: EXITING\n')
        exit()
    input('Point Your Camera at the Lights. Press ENTER or RETURN to continue')
    #For instructions requirement
    cords = [[0, 0, -1]] # just a thing so that error checking is able to be calculated
    sleep(.5)
    for i in range(50): # there are 50 lights so this is how to get them
        cords.append(get_cords(i, (cords[-1][0], cords[-1][1]),
            rpi, video_input)) #put the cordinates on the list

    cords.pop(0)

    cords = get_confidence(cords)

    request_light(rpi, 500)
    sleep(.5)
    rpi.send(str(cords).encode())
    print('Cords Sent to Remote Device')
    try:
        os.remove('led.png') # delete the temp image file
    except:
        pass

def get_confidence(cords):
    distance = []
    for i in range(len(cords)-2):
        distance.append(round((math.sqrt(((cords[i+1][0]-cords[i][0])**2)
        + ((cords[i+1][1]-cords[i][1])**2)))
        + (math.sqrt(((cords[i+1][0]-cords[i-1][0])**2)
        + ((cords[i][1]-cords[i-1][1])**2)))))

    mean = 0
    for i in distance:
        mean += i
    mean /= len(distance)

    for i in range(len(distance)):
        if distance[i] >= mean * 2:
            cords[i+1].append('R')
        elif distance[i] >= mean:
            cords[i+1].append('G')
        elif distance[i] <= mean:
            cords[i+1].append('B')
        else:
            cords[i+1].append('R')

    cords[0].append(cords[1][3])
    cords[-1].append(cords[-2][3])

    return cords



main()
