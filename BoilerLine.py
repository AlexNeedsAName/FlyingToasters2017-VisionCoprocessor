import numpy as np
import cv2


video_capture = cv2.VideoCapture(-1)
video_capture.set(3, 160)
video_capture.set(4, 120)

while(True):

    # Capture the frames
    ret, frame = video_capture.read()

    # Gaussian blur
    blur = cv2.GaussianBlur(frame,(5,5),0)

    #Convert to Hue, Saturation, and Value colorspace
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # define range of white color in HSV
    lower_white = np.array([20, 100, 100])
    upper_white = np.array([80, 255, 255])

    # Threshold the HSV image to get only white colors
    thresh = cv2.inRange(hsv, lower_white, upper_white)

    # Color thresholding
    #ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)

    # Find the contours of the frame
    contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

    # Find the biggest contour (if detected)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        cv2.line(frame,(cx,0),(cx,720),(255,0,0),1)
        cv2.line(frame,(0,cy),(1280,cy),(255,0,0),1)

        # then apply fitline() function
        [vx, vy, x, y] = cv2.fitLine(c, cv2.cv.CV_DIST_L2, 0, 0.01, 0.01)

        # Now find two extreme points on the line to draw line
        lefty = int((-x * vy / vx) + y)
        righty = int(((thresh.shape[1] - x) * vy / vx) + y)

        # Finally draw the line
        cv2.line(frame, (thresh.shape[1] - 1, righty), (0, lefty), 255, 2)

        cv2.drawContours(frame, contours, -1, (255,0,0), 1)

    else:
        print "I don't see the line"

    #Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break