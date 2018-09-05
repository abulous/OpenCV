import cv2
import numpy as np
from collections import deque
import pygame

pygame.init()

width = 640
height = 480

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

video = cv2.VideoCapture("roadV.mov")
video1 = cv2.VideoCapture("roadO.mov")
video2 = cv2.VideoCapture("roadA.mov")
mov = video

effect = pygame.mixer.Sound('sound.wav')
effect1 = pygame.mixer.Sound('sound1.wav')
effect2 = pygame.mixer.Sound('sound2.wav')

counter = 0
counter1 = 0
counter2 = 0
movCount = 0

xMid = width/2
yMid = height/2

dMax = yMid

#green
lower_green = np.array([29,40, 6]) 
upper_green = np.array([104, 255, 255])
greenRange = (lower_green, upper_green)
bgrGreen = (0, 255, 0)

#blue
lower_blue = np.array([110, 50, 50]) 
upper_blue = np.array([130, 255, 255])
bgrBlue = (255, 0, 0)

#red
lower_red = np.array([30,150,50])
upper_red = np.array([255,255,180])
bgrRed = (0, 0, 255)

capWeight = 1
vidWeight = 0
radius = 0

frame = None

greenFlag = False
blueFlag = False
redFlag = False

##flag = greenFlag
    

def loop():
    global counter, video, vidWeight
    if counter == 0:
        effect.play()
    effect.set_volume(vidWeight)
    counter +=1
    if counter == video.get(7):
        video.set(1, 0)
        counter = 0

def loop1():
    global counter1, video1
    if counter1 == 0:
        effect1.play()
    effect1.set_volume(vidWeight)
    counter1 += 1
    if counter1 == video1.get(7):
        counter1 = 0
        video1.set(1, 0)

def loop2():
    global counter2, video2
    if counter2 == 0:
        effect2.play()
    effect2.set_volume(vidWeight)
    counter2 += 1
    if counter2 == video2.get(7):
        counter2 = 0
        video2.set(1, 0)


def colorTrack(lowerColor, upperColor, contourColor):
    global frame, capWeight, vidWeight, greenFlag, blueFlag

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Threshold the HSV image to get only green colors
    maskRange = cv2.inRange(hsv, lowerColor, upperColor)
    mask = cv2.erode(maskRange, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
    noTarget = True

##    if lowerColor == lower_green and upperColor == upper_green:
##        input(maskRange)

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
                cv2.circle(frame, (int(x), int(y)), int(radius), contourColor, 2)
                cv2.circle(frame, center, 5, contourColor, -1)
            
                if contourColor == bgrGreen:
                    greenFlag = True
                else: greenFlag = False
                if contourColor == bgrBlue:
                    blueFlag = True
                else: blueFlag = False
                if contourColor == bgrRed:
                    redFlag = True

                d = ((cx - xMid)**2 + (cy - yMid)**2)**0.5

                if d < dMax:
                    capWeight = d/dMax
                else:                        
                   capWeight = 1
 
    if noTarget and capWeight < 1:
        capWeight += 0.02 
        if capWeight > 1:
            capWeight = 1

    vidWeight = 1-capWeight
    return contourColor


while(True):
    # Take each frame
    _, frame = cap.read()
    (ret, play) = mov.read()
    loop()
    loop1()
    loop2()
    
    colorTrack(lower_green, upper_green, bgrGreen)
    colorTrack(lower_blue, upper_blue, bgrBlue)
    colorTrack(lower_red, upper_red, bgrRed)
    
    if greenFlag is True:
##        print('im GREEN')
        mov = video

    if blueFlag is True:
##        print('IM BLUE')
        mov = video1

    if redFlag is True:
##        print('IM red')
        mov = video2
        
        
    blend = cv2.addWeighted(frame, capWeight, play, vidWeight, 0)
    cv2.imshow("Frame", blend)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        effect.stop()
        effect1.stop()
        effect2.stop()
        break
 
cv2.destroyAllWindows()
