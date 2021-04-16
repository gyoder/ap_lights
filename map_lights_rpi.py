import socket # used for connecting and sending commands back
import board    #used for gpio on rpi
import neopixel #used for controlling led on rpi
import sys

pixel_pin = board.D18   #used gpio pin 18
pixels = neopixel.NeoPixel(#initalises lights.
    pixel_pin, 50, brightness=1, auto_write=True, pixel_order=neopixel.GRB
)
pixels.fill(0)

host = ''
port = 50007

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
print('run camera program on other computer')
conn, addr = s.accept()
print('connected to', addr)
#data = conn.recv(1024)





while True:
    data = conn.recv(4096)
    if not data:
        print('exiting')
        break
    if int(data.decode()) == 500:
        data = conn.recv(8192)
        with open('cords.conf', 'w') as file:
            file.write(data.decode())
        break
    else:
        try:
            pixels.fill(0)
            pixels[int(data.decode())] = (255, 255, 255)
            print(f'Turning on LED {int(data.decode())}')
        except:
            sys.stderr.write('Data Is Unreadable')
conn.close()
