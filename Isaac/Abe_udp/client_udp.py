# from https://stackoverflow.com/questions/37586520/python-udp-videostreaming-with-cv2
import cv2
import numpy as np
import socket
import sys
import pickle
import struct

#UDP_IP = "xxx.xxx.x.x" # Inet_4 address for udp
UDP_IP = "192.168.0.101" # Inet_4 address for udp
UDP_PORT = 8012
cap=cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

clientsocket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # SOCK_DGRAM for udp

while True:
    ret,frame=cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # drop it down to one channel
    res = cv2.resize(frame,(64, 64), interpolation = cv2.INTER_AREA) # aiming for buffer size of 4096 = 64*64*1
                                                                     # but check and notice print(data). It is a little bigger.
                                                                     # probably because of resizing interpolation or
                                                                     # from pickling. docs says it adds a little more data
                                                                     # Most important point is that the value returned from
                                                                     # print(data) is the value that will for buffer size of
                                                                     # the server (socket.recvfrom(buffer))
    data = np.array(res)
##    print(data)

    dataToSend = pickle.dumps(data)
##    size = sys.getsizeof(dataToSend)

##    print(size)
##    cv2.imshow('resized', res) 
##    cv2.waitKey(4)
    clientsocket.sendto(dataToSend, (UDP_IP, UDP_PORT))

