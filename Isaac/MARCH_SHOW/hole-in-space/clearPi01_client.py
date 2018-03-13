# Isaac Nealey 2018
# adapted from https://stackoverflow.com/questions/37586520/python-udp-videostreaming-with-cv2

# this guy will live on clearPi01, sending its RGB stream to stickerPi

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
TRACKING_PORT = 8101 # send to stickerPi
DISP_OUT_PORT01 = 8105 # send to blackPi
DISP_OUT_PORT02 = 8106 # send to stripePi

stickerPi = (stickerPi_IP, TRACKING_PORT)
blackPi = (blackPi_IP, DISP_OUT_PORT01)
stripePi = (stripePi_IP, DISP_OUT_PORT02)

# create and sockets
colorSocket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # SOCK_DGRAM for udp
print('client sockets created')

# init camera
cap=cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

time.sleep(2) # some time to set up

while True:
    ret,frame=cap.read()
    res = cv2.resize(frame,(140, 140), interpolation = cv2.INTER_AREA) 
    data = np.array(res)
    
    #check print if unsure of final size
    #print(data)

    # send off to stickerPi
    dataToSend = pickle.dumps(data)
    colorSocket.sendto(dataToSend, stickerPi)

    
