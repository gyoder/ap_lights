import socket # used for connecting and sending commands back
import board    #used for gpio on rpi
import neopixel #used for controlling led on rpi

pixel_pin = board.D18   #used gpio pin 18
pixels = neopixel.NeoPixel(#initalises lights.
    pixel_pin, 50, brightness=1, auto_write=True, pixel_order=neopixel.GRB
)
pixels.fill(0)

for i in cords:
    if i[3] =< cordsdist:
        pixels[i][2] = (255, 0, 0)
    elif: i[3] < cordsdist + 200:
        pixels[i][3] = (125, 125, 0)
    else:
        pixel[i][3] = (0, 255, 0)
