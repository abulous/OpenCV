# grab a face, send a signal!

import numpy as np
import cv2
import os
from socket import *

host = "0.0.0.0"
port = 13000
addr = (host, port)

UDPSock = socket(AF_INET, SOCK_DGRAM)

width = 640
height = 480

iWIDTH = 3
iHEIGHT = 4
iFPS = 5 # Frames per Second

cap = cv2.VideoCapture(0)


cap.set(iWIDTH, width)
cap.set(iHEIGHT, height)
cap.set(iFPS, 30)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

count = 0
data=""

while True:

        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        

        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
 
        count += 1       


        UDPSock.sendto(data.encode('utf-8'), addr)

        if len(faces)==1:
                data="!"
        else:
                data=""
        
                
        
        for (x,y,w,h) in faces:
                img = cv2.rectangle(gray,(x,y),(x+w,y+h),255,2)

		
			                                                                                                                  
        cv2.imshow("face", gray)
        key = cv2.waitKey(25) & 0xFF
        if key == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
UDPSock.close()
os._exit(0)
