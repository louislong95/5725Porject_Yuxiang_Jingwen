import cv2 
import pytesseract
from picamera.array import PiRGBArray
from picamera import PiCamera
import os, requests, uuid, json
import numpy as np
import pyzbar.pyzbar as pyzbar

camera = PiCamera()
camera.resolution = (1024, 768)
camera.framerate = 30

rawCapture = PiRGBArray(camera, size=(1024, 768))

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
    
    rawCapture.truncate(0)

    if key == ord("s"):
        cv2.imshow("Frame", image)
        cv2.imwrite('test.png',image)
        cv2.waitKey(0)
        break

image = cv2.imread("test.png")

decodedObjects = pyzbar.decode(image)

for obj in decodedObjects:
    print("Type:", obj.type)
    print("Data:", obj.data, "\n")

cv2.imshow("Frame", image)
cv2.waitKey(0)