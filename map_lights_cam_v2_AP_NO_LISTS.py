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
    npimage = np.array(image) #make the image a numpy array for raw data processing
    red_cords = find_brightness_points(npimage)
    while len(red_cords) == 0:
        #red_cords = find_brightness_points(npimage)
        return (0, 0, 0)
    #print(len(red_cords))
    red_cords = sorted(red_cords, key = lambda x: x[2]) #https://www.geeksforgeeks.org/python-sort-list-according-second-element-sublist/
    # ^^ sorts it by contrast

    #for i in range(round(len(red_cords) * .9) - 1):
        #red_cords.pop(0)# gets the top 10% of contrast lights
    #print(red_cords)
    red_cords = np.array(red_cords)
    #print(red_cords)

    (locX, locY, contrast) = np.mean(red_cords, axis=0) #https://numpy.org/doc/stable/reference/generated/numpy.median.html
    #find the median
    ## TODO: make it so that it will check for advrage vs median just to see what is off

    return locX, locY, contrast

def find_contrast_points(img_array):
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
        xcord += 1 #this is a bit bad. make it read what idderation its on
        ycord = 0# reset each time
        for j in i:
            ycord += 1
            brighness = (int(j[0]) + int(j[1]) + int(j[2])) / 3 # find the brighness
            if brighness > 240:# might want to make this more reasonable
                high_brightness_points.append((xcord, ycord, brighness))
    return high_brightness_points

def get_cords(led, prev_loc, net_dev, video_input): #moved to a recursive function to make logging more verbose
    request_light(net_dev, led)
    save_image(video_input, led)
    (locX, locY, contrast) = get_bright(Image.open('led.png'))
    if (contrast < 200): # if it is too dark
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
    '''
    camlist = pygame.camera.list_cameras()
    for i in camlist: # loop through camera list so it doesnt just fail
        try:
            video_input = pygame.camera.Camera(i, (1280,720), 'RGB')
            video_input.start()
        except:
            sys.stderr.write('ERROR: camera ' +  str(i) + ' Failed To Start\n')

    #video_input.start()
    this might need more work
    '''
    video_input = pygame.camera.Camera('/dev/video0', (1280,720), 'RGB')
    video_input.start()
    try:
        rpi = init_network() # get the rpi connect
    except:
        sys.stderr.write('make sure the pi server is up first\nERROR: network failed to connect: exiting\n')
        exit()
    input('Point Your Camera at the Lights. Press ENTER or RETURN to continue')
    #For instructions requirement
    #cords = [[0, 0, -1]] # just a thing so that error checking is able to be calculated
    sleep(.5)
    '''
    for i in range(50): # there are 50 lights so this is how to get them

        cords.append(get_cords(i, (cords[-1][0], cords[-1][1]), rpi, video_input)) #put the cordinates on the list
    cords.pop(0)
    '''
    cord0x, cord0y = get_cords(i, (0, 0), rpi, video_input)
    cord1x, cord1y = get_cords(i, (cord0x, cord0y), rpi, video_input)
    cord2x, cord2y = get_cords(i, (cord1x, cord1y), rpi, video_input)
    cord3x, cord3y = get_cords(i, (cord2x, cord2y), rpi, video_input)
    cord4x, cord4y = get_cords(i, (cord3x, cord3y), rpi, video_input)
    cord5x, cord5y = get_cords(i, (cord4x, cord4y), rpi, video_input)
    cord6x, cord6y = get_cords(i, (cord5x, cord5y), rpi, video_input)
    cord7x, cord7y = get_cords(i, (cord6x, cord6y), rpi, video_input)
    cord8x, cord8y = get_cords(i, (cord7x, cord7y), rpi, video_input)
    cord9x, cord9y = get_cords(i, (cord8x, cord8y), rpi, video_input)
    cord10x, cord10y = get_cords(i, (cord9x, cord9y), rpi, video_input)
    cord11x, cord11y = get_cords(i, (cord10x, cord10y), rpi, video_input)
    cord12x, cord12y = get_cords(i, (cord11x, cord11y), rpi, video_input)
    cord13x, cord13y = get_cords(i, (cord12x, cord12y), rpi, video_input)
    cord14x, cord14y = get_cords(i, (cord13x, cord13y), rpi, video_input)
    cord15x, cord15y = get_cords(i, (cord14x, cord14y), rpi, video_input)
    cord16x, cord16y = get_cords(i, (cord15x, cord15y), rpi, video_input)
    cord17x, cord17y = get_cords(i, (cord16x, cord16y), rpi, video_input)
    cord18x, cord18y = get_cords(i, (cord17x, cord17y), rpi, video_input)
    cord19x, cord19y = get_cords(i, (cord18x, cord18y), rpi, video_input)
    cord20x, cord20y = get_cords(i, (cord19x, cord19y), rpi, video_input)
    cord21x, cord21y = get_cords(i, (cord20x, cord20y), rpi, video_input)
    cord22x, cord22y = get_cords(i, (cord21x, cord21y), rpi, video_input)
    cord23x, cord23y = get_cords(i, (cord22x, cord22y), rpi, video_input)
    cord24x, cord24y = get_cords(i, (cord23x, cord23y), rpi, video_input)
    cord25x, cord25y = get_cords(i, (cord24x, cord24y), rpi, video_input)
    cord26x, cord26y = get_cords(i, (cord25x, cord25y), rpi, video_input)
    cord27x, cord27y = get_cords(i, (cord26x, cord26y), rpi, video_input)
    cord28x, cord28y = get_cords(i, (cord27x, cord27y), rpi, video_input)
    cord29x, cord29y = get_cords(i, (cord28x, cord28y), rpi, video_input)
    cord30x, cord30y = get_cords(i, (cord29x, cord29y), rpi, video_input)
    cord31x, cord31y = get_cords(i, (cord30x, cord30y), rpi, video_input)
    cord32x, cord32y = get_cords(i, (cord31x, cord31y), rpi, video_input)
    cord33x, cord33y = get_cords(i, (cord32x, cord32y), rpi, video_input)
    cord34x, cord34y = get_cords(i, (cord33x, cord33y), rpi, video_input)
    cord35x, cord35y = get_cords(i, (cord34x, cord34y), rpi, video_input)
    cord36x, cord36y = get_cords(i, (cord35x, cord35y), rpi, video_input)
    cord37x, cord37y = get_cords(i, (cord36x, cord36y), rpi, video_input)
    cord38x, cord38y = get_cords(i, (cord37x, cord37y), rpi, video_input)
    cord39x, cord39y = get_cords(i, (cord38x, cord38y), rpi, video_input)
    cord40x, cord40y = get_cords(i, (cord39x, cord39y), rpi, video_input)
    cord41x, cord41y = get_cords(i, (cord40x, cord40y), rpi, video_input)
    cord42x, cord42y = get_cords(i, (cord41x, cord41y), rpi, video_input)
    cord43x, cord43y = get_cords(i, (cord42x, cord42y), rpi, video_input)
    cord44x, cord44y = get_cords(i, (cord43x, cord43y), rpi, video_input)
    cord45x, cord45y = get_cords(i, (cord44x, cord44y), rpi, video_input)
    cord46x, cord46y = get_cords(i, (cord45x, cord45y), rpi, video_input)
    cord47x, cord47y = get_cords(i, (cord46x, cord46y), rpi, video_input)
    cord48x, cord48y = get_cords(i, (cord47x, cord47y), rpi, video_input)
    cord49x, cord49y = get_cords(i, (cord48x, cord48y), rpi, video_input)
    '''
    for i in range(48):
        cords[i+1].append(round((math.sqrt(((cords[i+1][0]-cords[i][0])**2) + ((cords[i+1][1]-cords[i][1])**2))) + (math.sqrt(((cords[i+1][0]-cords[i-1][0])**2) + ((cords[i][1]-cords[i-1][1])**2)))))
        # i hope that ^^^ never breaks because i do NOT want to know what i was thinking when writing that
    cords[0].append(cords[1][3])
    cords[49].append(cords[48][3])
    cordsdist = 0
    for i in cords:
        #print(i[3])
        cordsdist += i[3]
    cordsdist = cordsdist / 50

    #print(cordsdist)
    #print(cords)
    request_light(rpi, 500)
    sleep(.5)
    rpi.send(str(cords).encode())
    print('sent cords')
    '''
    try:
        os.remove('led.png') # delete the temp image file
    except:
        pass
main()
