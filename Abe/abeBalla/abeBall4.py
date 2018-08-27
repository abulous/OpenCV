import cv2
import numpy as np
from collections import deque

from CirFrameBuf import CirFrameBuf



width = 640
height = 480

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

video = cv2.VideoCapture("tvBreak2.mov")



xMid = width/2
yMid = height/2

dMax = yMid

#define green in hsv
#lower_green = np.array([29,86, 6]) 
#upper_green = np.array([64, 255, 255])

lower_green = np.array([29,40, 6]) 
upper_green = np.array([104, 255, 255]) 

loop = 1

blender = 1

weight1 = 1
weight2 = 0
radius = 0

size = 40 # ...# of frames
pixdepth = 3

cfbuf = CirFrameBuf(size+1, height, width, pixdepth)

dframe = None

nfback = 1
inc = 1
    
while(True):

    # Take each frame
    _, frame = cap.read()

    (ret, play) = video.read()
##    play = cv2.cvtColor(play, cv2.COLOR_BGR2GRAY)

    # Write out to the circular buffer
    cfbuf.write(frame)

# This is to modulate the delay, so the buffer gets either bigger or smaller depending on where it is.
    if nfback >= size: 
        inc = -1
    elif nfback <= 1:
        inc = 2
    nfback += inc

    dframe = cfbuf.readback(nfback)

# Video Loop
    loop +=1
    if loop == video.get(7):
        video.set(1, 0)
        loop = 0

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

    blend = cv2.addWeighted(frame, 0.5, dframe, 0.5, 0)
    blend = cv2.addWeighted(blend, weight1, play, weight2, 0)
    # show the frame to our screen
    cv2.imshow("Frame", blend)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
            break
 
cv2.destroyAllWindows()
