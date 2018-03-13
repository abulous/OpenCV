# Isaac Nealey 2018
# adapted from https://stackoverflow.com/questions/37586520/python-udp-videostreaming-with-cv2

# this script will ive one clearPi02, sending its rgb stream to blackPi

import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import time

#UDP_IP = "xxx.xxx.x.x" - Inet_4 address for udp
stickerPi_IP = "192.168.0.110"
stripePi_IP = "192.168.0.109"
blackPi_IP = "192.168.0.108"

#UDP_PORT = xxxx - port for udp
TRACKING_PORT = 8101 # send to blackPi
DISP_OUT_PORT01 = 8105 # send to stickerPi
DISP_OUT_PORT02 = 8106 # send to stripePi

stickerPi = (stickerPi_IP, DISP_OUT_PORT01)
blackPi = (blackPi_IP, TRACKING_PORT)
stripePi = (stripePi_IP, DISP_OUT_PORT02)

# create and sockets
colorSocket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # SOCK_DGRAM for udp
graySocket01=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
graySocket02=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
print('client sockets created')

# init camera
cap=cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

time.sleep(2) # some time to set up

while True:
    ret,frame=cap.read()
    res = cv2.resize(frame,(140, 140), interpolation = cv2.INTER_AREA) # aiming for buffer size of 58,800 = 140*140*3
    data = np.array(res)
    
    #check print if unsure of final size
    #print(data)

    # send off to blackPi
    dataToSend = pickle.dumps(data)
    colorSocket.sendto(dataToSend, blackPi)

    # now send off the grayscale ones
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    data = np.array(gray)   
    dataToSend = pickle.dumps(data)     # should be 19,793
    graySocket01.sendto(dataToSend, stickerPi)
    graySocket02.sendto(dataToSend, stripePi)
    
