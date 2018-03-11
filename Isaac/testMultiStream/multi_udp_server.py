# Isaac Nealey March 2018
# adapted from https://stackoverflow.com/questions/37586520/python-udp-videostreaming-with-cv2
#
# for this code to run, four intances of ' client_udp.py ' need to be
# running. Their UDP socket should point to the IP of THIS machine,
# using UDP ports 8012, 8013, 8014, 8015
#
# it would be possible to run all four locally, just point IPs to '127.0.0.1', and make sure each
# ' client_udp ' has a unique capture. (i.e. cap = VideoCapture(0) in one file,
#       cap = VideoCapture(1) in the next...)

import socket
import sys
import cv2
import pickle
import numpy as np
import struct

#HOST='xxx.xxx.x.x'  # Inet_4 address for udp x.x.x.x
HOST='0.0.0.0'  # Inet_4 address for udp x.x.x.x
#set up four ports for UDP
PORT01=8012
PORT02=8013
PORT03=8014
PORT04=8015

# create and bind the sockets
s1=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # SOCK_DGRAM for udp
print ('socket 01 created')

s2=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # SOCK_DGRAM for udp
print ('socket 02 created')

s3=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # SOCK_DGRAM for udp
print ('socket 03 created')

s4=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # SOCK_DGRAM for udp
print ('socket 04 created')

print('socket creation complete\n')

print ('binding socket 01 @ port 8012')
s1.bind((HOST, PORT01))

print ('binding socket 02 @ port 8013')
s2.bind((HOST, PORT02))

print ('binding socket 03 @ port 8014')
s3.bind((HOST, PORT03))

print ('binding socket 04 @ port 8015')
s4.bind((HOST, PORT04))

print('socket binding complete\n')

print('beginning network stream\n')
print('Press [ s ] to switch between incoming streams')
print('Press [ q ] to quit\n')

data = ""

streamSelect = 1
while True:    
    #data, addr = s.recvfrom(4289) #buffer size for 64 x 64 grayscale
    #data, addr = s.recvfrom(57793) #buffer size for 240 x 240 grayscale
    #data, addr = s1.recvfrom(58993) #buffer size for 140 x 140 RGB
    
    # switch to decide where to recieve from
    if streamSelect == 1:
        data, addr = s1.recvfrom(58993) 
    elif streamSelect == 2:
        data, addr = s2.recvfrom(58993) 
    elif streamSelect == 3:
        data, addr = s3.recvfrom(58993)
    elif streamSelect == 4:
        data, addr = s4.recvfrom(58993) 

    frame = pickle.loads(data)
    
    res = cv2.resize(frame, (640, 480), interpolation = cv2.INTER_LINEAR)

    cv2.imshow('resized', res)
    
    # switch screens if 's', quit if 'q'
    k = cv2.waitKey(30) & 0xff
    if k == 113:
        break
    elif k == 115:
        streamSelect += 1
    if streamSelect > 4:
        streamSelect = 1

s1.close()
s2.close()
s3.close()
s4.close()
print('all sockets closed')
cv2.destroyAllWindows()

