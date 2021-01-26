
import cv2  #used for webcam input
import numpy as np  #used for array storage of datapoints
import socket   #used to connect to rpi in transfer of data
from time import sleep

def init_network(host = '192.168.0.79', port = 50007):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s

def get_bright(image):
    grey_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)    #makes greyscale
    grey_frame_blur = cv2.blur(grey_frame, (10,10), cv2.BORDER_DEFAULT)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(grey_frame_blur)
    cv2.circle(grey_frame, maxLoc, 10, (255, 0, 0), 2)
    cv2.imshow('grey', grey_frame)
    return maxLoc

def get_picture(video_input_device):
    ret, frame = video_input_device.read() #ret is for the error and frame is frame
    if not ret:
        print('failed to get frame')
        #break
    #cv2.imshow('preview', frame)   #shows a preview of the frame

    k = cv2.waitKey(1)  # i need this code here or it wont work
    if k%256 == 27:     # for some reason it needs to have a
        pass           # wait key so it will just quit the program
    return frame


def main():
    video_input = cv2.VideoCapture(0)

    #cv2.namedWindow('preview')  #make window for the cam preview
    cv2.namedWindow('grey')
    #cv2.namedWindow('all lights')
    cords = []
    all_lights = get_picture(video_input)
    rpi = init_network()

    for i in range(50):
        #try:
        rpi.send(str(i).encode())
        #except:
            #print('could not send data')
        sleep(.5)
        maxLoc = get_bright(get_picture(video_input))
        print(maxLoc)
        print('got bright pixel for ', i)
        cords.append([maxLoc[0], maxLoc[1], i])
        cv2.circle(all_lights, maxLoc, 10, (255, 0, 0), 2)
        cv2.imshow('all lights', all_lights)
    sleep(30)
    video_input.release()
    cv2.destroyAllWindows()
    print(cords)
main()
