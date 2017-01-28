import numpy as np
import cv2
import math
import sys
import time
import serial

import BoilerLine
import BoilerStack
import LineFollower
import SpringDetect

video_capture = cv2.VideoCapture(-1)
video_capture.set(3, 160)
video_capture.set(4, 120)

showVideo = 0

ser = serial.Serial('/dev/ttyAMA0', baudrate = 115200)

while(True):
    data = ser.readline()
    ser.flush()

    print "incoming: "+data
	
    if '0' in data:
        #ret, frame = video_capture.read()
        #sendData = BoilerLine.findBoilerLine(ret, frame)
        sendData = 'BoilerLine not working yet :('
    elif '1' in data:
        ret, frame = video_capture.read()
        sendData = BoilerStack.findBoilerStack(ret, frame)
    elif '2' in data:
        ret, frame = video_capture.read()
        sendData = LineFollower.lineOffset(ret, frame)
    elif '3' in data:
        ret, frame = video_capture.read()
        sendData = SpringDetect.findSpring(ret, frame)
    else:
        sendData = 'Bad request: ' + data
    ser.write(bytes(sendData))
    print 'sent: \"' + str(sendData) + '\"'
    #Show Window
    if showVideo == 1:
        cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
