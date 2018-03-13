# Isaac Nealey / Abe King 2018
# adapted from https://stackoverflow.com/questions/37586520/python-udp-videostreaming-with-cv2

import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import time

#UDP_IP = "xxx.xxx.x.x" - Inet_4 address for udp
UDP_IP = "127.0.0.1"
#UDP_PORT = xxxx - port for udp
UDP_PORT = 8012
cap=cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # SOCK_DGRAM for udp
time.sleep(2) # some time to set up

while True:
    ret,frame=cap.read()
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # drop it down to one channel if needed
    #res = cv2.resize(frame,(64, 64), interpolation = cv2.INTER_AREA) # aiming for buffer size of 4096 = 64*64*1
    res = cv2.resize(frame,(140, 140), interpolation = cv2.INTER_AREA) # aiming for buffer size of 58800 = 140*140*3

    data = np.array(res)
    
    #check print if unsure of final size
    #print(data)

    dataToSend = pickle.dumps(data)

    clientsocket.sendto(dataToSend, (UDP_IP, UDP_PORT))

