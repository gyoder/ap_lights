import board
import neopixel
from time import sleep
from random import randint
import threading
from picoboard import PicoBoard
from init_lights import *
with open('cords.conf', 'r') as cordfile:
    exec('cords = ' + str(cordfile.read()))
l = led_lights()
pb = PicoBoard('/dev/ttyUSB0') #device file for PicoBoard
while True:
    blues = []
    reds = []
    others = []
    intensity = pb.read()['slider']
    l.fill_all((127, 0, 127))
    for i in cords:
        if i[1] - 100 > intensity:
            blues.append(i[2])
        elif i[1] + 100 < intensity:
            reds.append(i[2])
        else:
            others.append(i[2])
    l.fill_some((127,0,127), others)
    l.fill_some((0, 0, 255), blues)#filter(lambda x: x[2] + 100 <= intensity, cords))
    #l.fill_some((255, 0, 0), filter(lambda x: x[2] + 100 >= intensity and x[2] - 100 <= intensity, cords))
    l.fill_some((255, 0, 0), reds)#filter(lambda x: x[2] - 100 >= intensity, cords))


    l.write()
