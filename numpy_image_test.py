from PIL import Image
import numpy as np

image = Image.open('/home/scie/Pictures/test.jpg')
print(image)
npimage = np.array(image)
#print(npimage)
#print(npimage[:, :, :1])
red_cords = []
xcord = 0
ycord = 0
for i in npimage:
    xcord += 1
    ycord = 0
    for j in i:
        ycord += 1
        contrast = (int(j[0]) - ((int(j[1]) + int(j[2])) / 2))
        if contrast > 150:
            red_cords.append((xcord, ycord, contrast))

red_cords = np.asarray(red_cords)
print(np.median(red_cords, axis=0)) #https://numpy.org/doc/stable/reference/generated/numpy.median.html

#print(red_cords)
