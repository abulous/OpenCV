import cv2
import numpy as np
import sys
import time
import threading
from someSupport import *

path_to_mpi = 'mpi/'
haar_path = 'C:/Users/Tommy/Anaconda3/Library/etc/haarcascades/'

faceCL = cv2.CascadeClassifier(haar_path+'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
ret, frame = cap.read()


switch = False
newFace = False
wasNoFace = False
noface_counter = 0
noface_buffer = 100 #frames
faces = []

HT = HaarThread(faceCL, noface_counter, frame)

while True:
    #standard live capture
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_read = frame.copy()

    #HaarThread running
    if not HT.started:
        print("starting HT")
        HT.start()
    else:
        HT.frame = frame


    #### DETERMINING WHEN TO SWITCH VIDEOS ####
    if HT.noface_counter >= noface_buffer:
        ## IF no face seen for 100 frames, note that there isn't a face
        HT.noFace = True
        wasNoFace = True

    if HT.noFace:
        ## IF no faces, close the write and read videos
        print("closing video")
        if switch:
            close(reader1, writer2)
        else:
            close(reader2, writer1)

    if not HT.noFace and wasNoFace:
        ## IF face seen after period of no face being seen, note that this is a new face
        newFace = True
        wasNoFace = False
    
    if newFace:
        ## IF seeing a new face on screen, switch over to correct read and write files
        print("\n\nswitching\n\n")
        if switch:
            init_read2_write1()
        else:
            init_read1_write2()
        switch = not switch
        newFace = False

    #### READING, WRITING, and DISPLAYING FRAMES ####
    # If see a face: read from history, and write frame out
    if switch and not HT.noFace:
        frame_read = read1_write2(frame)
    elif not switch and not HT.noFace:
        frame_read = read2_write1(frame)

    frame_blend = cv2.addWeighted(frame, 0.5, frame_read, 0.5, 0)

##    if not (frame == frame_read).all():
##        print("\tSHOULD SEE BLEND")
    
    cv2.imshow("Temporal Blend", frame_blend)
    cv2.moveWindow("Temporal Blend", 10,10)
    if cv2.waitKey(33) == 27:
        break





## Close/Release/Join/Destroy everything
HT.release()
HT.join()
cap.release()
reader1.release()
reader2.release()
writer1.release()
writer2.release()

cv2.destroyAllWindows()
print("fin")
