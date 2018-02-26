# from https://stackoverflow.com/questions/37586520/python-udp-videostreaming-with-cv2

import socket
import sys
import cv2
import pickle
import numpy as np
import struct

HOST='192.168.0.5'  # Inet_4 address for udp x.x.x.x
PORT=8012

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # SOCK_DGRAM for udp
print ('Socket created')

s.bind((HOST, PORT))
print ('Socket bind complete')

data = ""

i = 0
while True:    
    data, addr = s.recvfrom(4289) #buffer size of incoming image. a little bigger that 4096 = 64 x 64 x 1
##    print(data)
    frame = pickle.loads(data)
    
    
##    i = i + 1
##    print('coming frame' + str(i))
    res = cv2.resize(frame, (640, 480), interpolation = cv2.INTER_LINEAR)

##    thresh = cv2.adaptiveThreshold(res,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,21, 2)
##    ret_thresh, thresh = cv2.threshold(res,127,255,cv2.THRESH_BINARY_INV)
##    canny = cv2.Canny(res, 3, 15)
##    blend = cv2.addWeighted(thresh, 0.5, canny, 0.5, 0)

## effects for playing, otherwise it is boring pixelated feed with low light.
## more importantly these effects are built from signal processing techniques that accentuate the image in order to get desired results.

    cv2.imshow('resized', blend) 
    cv2.waitKey(4) 
##s.close()

