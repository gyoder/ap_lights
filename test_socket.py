import socket
from time import sleep

HOST = '192.168.0.79'    # The remote host
PORT = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
#s.send('show'.encode())
#data = s.recv(1024)
cords = [[355, 131, 0], [351, 130, 1], [351, 129, 2], [351, 129, 3], [215, 214, 4], [173, 272, 5], [175, 273, 6], [249, 209, 7], [211, 146, 8], [263, 79, 9], [237, 85, 10], [203, 151, 11], [216, 201, 12], [265, 238, 13], [223, 291, 14], [223, 292, 15], [252, 368, 16], [211, 413, 17], [240, 436, 18], [268, 479, 19], [262, 479, 20], [322, 462, 21], [270, 420, 22], [343, 380, 23], [345, 328, 24], [293, 283, 25], [309, 231, 26], [353, 200, 27], [330, 167, 28], [329, 167, 29], [338, 101, 30], [336, 53, 31], [353, 195, 32], [337, 217, 33], [346, 269, 34], [349, 273, 35], [343, 301, 36], [355, 371, 37], [290, 449, 38], [217, 419, 39], [190, 401, 40], [178, 375, 41], [176, 300, 42], [151, 274, 43], [141, 217, 44], [141, 216, 45], [141, 115, 46], [210, 93, 47], [210, 93, 48], [158, 148, 49]]

for i in range(50):
    s.send(str(i).encode())
    input('')
s.close()
