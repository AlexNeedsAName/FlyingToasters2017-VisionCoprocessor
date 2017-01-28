import numpy as np
import cv2
import math
import sys
import time
import serial

#import BoilerLine
#import BoilerStack
#import LineFollower
import SpringDetect

ser = serial.Serial('/dev/ttyAMA0')
print(ser.name)
ser.write('TEST TEST TEST')

video_capture = cv2.VideoCapture(-1)
video_capture.set(3, 240)
video_capture.set(4, 180)

#Change these two values to run different conencted programs
showVideo = 1
data = 3

while(True):
    if data == 0:
        ret, frame = video_capture.read()
        sendData = BoilerLine.findBoilerLine(ret, frame)
    if data == 1:
        ret, frame = video_capture.read()
        sendData = BoilerStack.findBoilerStack(ret, frame)
    if data == 2:
        ret, frame = video_capture.read()
        sendData = LineFollower.lineOffset(ret, frame)
    elif data == 3:
        ret, frame = video_capture.read()
        sendData = SpringDetect.findSpring(ret, frame)
    print(sendData)
    ser.write(bytes(sendData))
    #Quit Key
    if showVideo == 1:
        cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
