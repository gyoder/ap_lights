import board
import neopixel
from time import sleep
from random import randint
import threading
from picoboard import PicoBoard
with open('cords.conf', 'r') as cordfile:
    exec('cords = ' + str(cordfile.read())) #actual garbage
pixel_pin = board.D18
pixels = neopixel.NeoPixel(
    pixel_pin, 50, brightness=1, auto_write=False, pixel_order=neopixel.GRB
)
pb = PicoBoard('/dev/ttyUSB0') #device file for PicoBoard
while True:
    intensity = pb.read()['slider']
    for j in cords:

        if j[1] < intensity: #1500 - (i* 10):
            pixels[j[2]] = (0, 0, 255)

        else:
            pixels[j[2]] = (0, 255, 0)

    pixels.show()
    sleep(0.05)
