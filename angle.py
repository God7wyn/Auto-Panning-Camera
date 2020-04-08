import cv2
import os
from math import sin, cos, radians
import ctypes

user32 = ctypes.windll.user32
scl,scb = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
print("Width: ",scl,"Height: ",scb) #screen metrics

os.chdir("F:\Machine Learning")

camera =  cv2.VideoCapture(0)

w = camera.set(3, 1280)#scl
h = camera.set(4, 720)#scb
face = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
fps = camera.get(cv2.CAP_PROP_FPS)
print("fps: ",fps)
settings = {
    'scaleFactor': 1.3, 
    'minNeighbors': 3, 
    'minSize': (50, 50), 

}
print("width = ",camera.get(3))
print("height = ",camera.get(4))

def rotate_image(image, angle):
    if angle == 0: return image
    height, width = image.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((width/2, height/2), angle, 0.9)
    result = cv2.warpAffine(image, rot_mat, (width, height), flags=cv2.INTER_LINEAR)
    return result

def rotate_point(pos, img, angle):
    if angle == 0: return pos
    x = pos[0] - img.shape[1]*0.4
    y = pos[1] - img.shape[0]*0.4
    newx = x*cos(radians(angle)) + y*sin(radians(angle)) + img.shape[1]*0.4
    newy = -x*sin(radians(angle)) + y*cos(radians(angle)) + img.shape[0]*0.4
    return int(newx), int(newy), pos[2], pos[3]

tx = 0
ty = 0

while True:
    ret, imgn = camera.read()
    img = cv2.flip(imgn, +1)

    for angle in [0, -25, 25]:
        rimg = rotate_image(img, angle)
        detected = face.detectMultiScale(rimg, **settings)
        if len(detected):
            detected = [rotate_point(detected[-1], img, -angle)]
            break

    # Make a copy as we don't want to draw on the original image:
    for x, y, w, h in detected[-1:]:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255,0,0), 2)
        l = x+w/2
        b = y+h/2
       # print
        dx = (0.5 - l/1280)*100
        dy = (0.5 - b/720)*60
        tx = dx
        ty = dy
        print("go right by",tx,"go down by",ty)

    # detete this line if you dont want if to print the center.

    cv2.imshow('facedetect', img)
    if cv2.waitKey(5) != -1:
        break

cv2.destroyWindow("facedetect")

'''
for my laptop the x and y angles are 100 and 60 degrees resp.
so now we plug them into 
'''



