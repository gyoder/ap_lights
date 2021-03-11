'''
this is going to be a file that i import to
make the rpi simpiler to write programs for
from init_lights import *
'''
import board
import neopixel
from time import sleep
from random import randint
from picoboard import PicoBoard

class led_lights:
    def __init__(self, count = 50, brightness = 1):
        self.count = count
        self.lights = neopixel.NeoPixel(
            board.D18, count, brightness=brightness,
            auto_write=False, pixel_order=neopixel.GRB
            )

    def fill_all(self, color):
        self.lights.fill((color[1], color[0], color[2]))

    def fill_some(self, color, lights):
        for i in lights:
            self.lights[i] = (color[1], color[0], color[2])

    def write(self):
        self.lights.show()


def get_cords(file = 'cords.conf'): # does not work at all, TODO: FIX IT!
    with open('/home/pi/cords.conf', 'r') as cordfile:
        exec('cords = ' + str(cordfile.read()))
        print(cordfile.read())
        return cords
