import cv2
import numpy as np
from collections import deque

import os
import sys
import numpy as np
import mpi4py import MPI
import time

comm = MPI.COMM_WORLD
size - comm.Get_size()
rank - comm.Get_rank()
name - MPI.Get_processor_name()

os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
os.environ['DISPLAY'] = '0, 0'

comm.Barrier

width = 640
height = 480

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

video = cv2.VideoCapture("roadV.mov")
video1 = cv2.VideoCapture("roadO.mov")



xMid = width/2
yMid = height/2

dMax = yMid

#define green in hsv
#lower_green = np.array([29,86, 6]) 
#upper_green = np.array([64, 255, 255])

lower_green = np.array([29,40, 6]) 
upper_green = np.array([104, 255, 255]) 

counter = 1
counter1 = 1

blender = 1

weight1 = 1
weight2 = 0
radius = 0
    
while(True):
    if rank = 0:
        # Take each frame
        _, frame = cap.read()

        (ret, play) = video.read()
    ##    play = cv2.cvtColor(play, cv2.COLOR_BGR2GRAY)

        counter +=1
        if counter == video.get(7):
            video.set(1, 0)
            counter = 0

        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        

        # Threshold the HSV image to get only green colors
        mask = cv2.inRange(hsv, lower_green, upper_green)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
        

        noTarget = True
        # only proceed if at least one contour was found
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

        comm.send(weight1, dest = 1, tag = 11)
        comm.send(weight2, dest = 1, tag = 22)
        blend = cv2.addWeighted(frame, weight1, play, weight2, 0)
        cv2.imshow("Frame", blend)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
                break

    if rank = 1:
        weight1 = comm.recv(source = 0, tag = 11)
        weight2 = comm.recv(source = 0, tag = 22)

        _, frame = cap.read
        ret, play = video1.read()
        counter1 += 1
        if counter1 == video1.get(7):
            counter1 = 0 
            video1.set(1, 0)

        blend = cv2.addWeighted(frame, weight1, play, weight2, 0)
        cv2.imshow("Frame", blend)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
                break
                   
        
cv2.destroyAllWindows()
