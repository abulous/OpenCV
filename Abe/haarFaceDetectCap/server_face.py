# clients sees face sends signal!
import os
from socket import *
import numpy as np
import cv2
import os
from socket import *

host = ""
port = 13000
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)    
UDPSock.bind(addr)

width = 640
height = 480
iWIDTH = 3
iHEIGHT = 4
iFPS = 5 # Frames per Second

cap = cv2.VideoCapture(0)

cap.set(iWIDTH, width)
cap.set(iHEIGHT, height)
cap.set(iFPS, 30)

w_can=0.5
w_gray=0.5

count = 1
test = 1

                   
print("Waiting to receive messages...")

while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        can = cv2.Canny(gray, 1, 31)


        (data, addr) = UDPSock.recvfrom(buf)
        data.decode('utf-8')

        if data== b'!':
            w_can += 0.1
            if w_can > 1:
                w_can = 1

            w_gray -= 0.1
            if w_gray < 0:
                w_gray=0
                    
        else:
            w_gray += 0.1
            if w_gray > 1:
                w_gray = 1

            w_can -= 0.1
            if w_can < 0:
                w_can = 0
        

        blend = cv2.addWeighted(can, w_can, gray, w_gray, 0)
        cv2.imshow("movie", blend)

        key = cv2.waitKey(25) & 0xFF
        if key == ord("q"):
               break

##       if data == "exit":
##              break
        
        
        
UDPSock.close()
os._exit(0)
