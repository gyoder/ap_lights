import board
import neopixel
from init_lights import *
from time import sleep

with open('cords.conf', 'r') as cordfile:
    exec('cords = ' + str(cordfile.read())) 
l = led_lights(count=50)
red_bar = 120
green_bar = 360
blue_bar = 600

while True:
    red_bar += 1
    green_bar += 1
    blue_bar += 1
    for i in cords:
        color = [0,0,0]
        if abs((red_bar % 720) - i[0]) <= 240:
            color[0] = 256 - abs((red_bar % 720) - i[0])
        elif abs((red_bar % 720) - (i[0] + 720)) <= 240:
            color[0] = 256 - abs((red_bar % 720) - (i[0] + 720))

        if abs((green_bar % 720) - i[0]) <= 240:
            color[1] = 256 - abs((green_bar % 720) - i[0])
        elif abs((green_bar % 720) - (i[0] + 720)) <= 240:
            color[0] = 256 - abs((green_bar % 720) - (i[0] + 720))

        if abs((blue_bar % 720) - i[0]) <= 240:
            color[2] = 256 - abs((blue_bar % 720) - i[0])
        elif abs((blue_bar % 720) - (i[0] + 720)) <= 240:
            color[0] = 256 - abs((blue_bar % 720) - (i[0] + 720))

        l.fill_one(color, i[2])

    sleep(.01)
