import cv2
import numpy as np
from collections import deque

width = 640
height = 480

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

video = cv2.VideoCapture("roadV.mov")
##video1 = cv2.VideoCapture("roadO.mov")
##video2 = cv2.VideoCapture("Test.mov")
mov = video

counter = 1
counter1 = 1
movCount = 1

xMid = width/2
yMid = height/2

dMax = yMid

#green
lower_green = np.array([29,40, 6]) 
upper_green = np.array([104, 255, 255])
##greenRange = (lowerGreen

#blue
lower_blue = np.array([110, 50, 50]) 
upper_blue = np.array([130, 255, 255])

#red
lower_red = np.array([30,150,50])
upper_red = np.array([255,255,180])

weight1 = 1
weight2 = 0
radius = 0

frame = None
    

def loop():
    global counter, video
    counter +=1
    if counter == video.get(7):
        video.set(1, 0)
        counter = 0
##
##def loop1():
##    global counter1, video1
##    counter1 += 1
##    if counter1 == video1.get(7):
##        counter1 = 0
##        video1.set(1, 0)


def colorTrack(lowerColor, upperColor):
    global frame, weight1, weight2 

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lowerColor, upperColor)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
    noTarget = True

    if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            cx = (int(M["m10"] / M["m00"]))
            cy = (int(M["m01"] / M["m00"]))
            center = (cx, cy) # center of ball
                        
            if radius > 30 and radius < 120:
                noTarget = False
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                        (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)


                d = ((cx - xMid)**2 + (cy - yMid)**2)**0.5

                if d < dMax:
                    weight1 = d/dMax
                else:                        
                   weight1 = 1
 
    if noTarget and weight1 < 1:
        weight1 += 0.02 
        if weight1 > 1:
            weight1 = 1

    weight2 = 1-weight1


while(True):
    # Take each frame
    _, frame = cap.read()
    (ret, play) = video.read()
    loop()
    colorTrack(lower_green, upper_green)
    colorTrack(lower_blue, upper_blue)
    colorTrack(lower_red, upper_red)

##    movCount += 1
##    if movCount < 60:
##        mov = video1
##    else: mov = video
##    if movCount >= 120:
##        movCount = 0
        
    blend = cv2.addWeighted(frame, weight1, play, weight2, 0)
    cv2.imshow("Frame", blend)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
            break
 
cv2.destroyAllWindows()
