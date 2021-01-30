import board
import neopixel
import numpy as np
from time import sleep

pixel_pin = board.D18
pixels = neopixel.NeoPixel(
    pixel_pin, 50, brightness=1, auto_write=False, pixel_order=neopixel.GRB

cords = np.asarray()
for j in range(2000):
    for i in cords:
        if i[0] + i[1] > j:
            pixels[i[2]] = (255, 255, 255)
