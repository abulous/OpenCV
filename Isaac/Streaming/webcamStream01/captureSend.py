# taken from: https://github.com/yushuhuang/webcam
# being a demo, this code is clunky and could be improved in many ways
#   (tailored for desired performance)
#
# usage: python3 captureSend.py
#   -start after reciever.
# set 'host' and 'port' to address of machine to stream --TO--

"""Webcam video streaming client

Using OpenCV to capture frames from webcam.
Compress each frame to jpeg and save it.
Using socket to read from the jpg and send
it to remote address.
!!!press q to quit!!!
"""
import numpy as np
import cv2
from socket import *

cap = cv2.VideoCapture(0)

# ratio determines how often file is sent off
FPS = cap.get(5)
setFPS = 10
ratio = int(FPS)/setFPS

# specify port/streaming info    
host = "192.168.0.101"
host.encode()
port = 4096
addr = (host, port)
buf = 1024

def sendFile(fName):
    s = socket(AF_INET, SOCK_DGRAM)
    s.sendto(fName, addr)
    f = open(fName, "rb")
    data = f.read(buf)
    while data:
        if(s.sendto(data, addr)):
            data = f.read(buf)
    f.close()
    s.close()

def captureFunc():
    count = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            #cv2.imshow('frame', frame)
            count = count + 1
            if count == ratio:
                cv2.imwrite("img.jpg", frame)
                sendFile("img.jpg")
                count = 0            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

if __name__ == '__main__':
    captureFunc()
    cap.release()
    cv2.destroyAllWindows()
