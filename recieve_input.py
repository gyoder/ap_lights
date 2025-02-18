import socket # used for connecting and sending commands back
import board    #used for gpio on rpi
import neopixel #used for controlling led on rpi

pixel_pin = board.D18   #used gpio pin 18
pixels = neopixel.NeoPixel(#initalises lights.
    pixel_pin, 50, brightness=0.2, auto_write=True, pixel_order=neopixel.GRB
)
pixels.fill(0)

host = ''
port = 50007

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
conn, addr = s.accept()
print('connected to', addr)
data = conn.recv(1024)





while True:
    data = conn.recv(1024)
    if not data:
        break
    try:
        #pixels.fill(0)
        pixels[int(data.decode())] = (255, 255, 255)
        print(int(data.decode()))
    except:
        print('did not like data')
conn.close()
