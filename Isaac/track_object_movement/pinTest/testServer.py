import numpy as np
import cv2
from socket import *

# set up socket 
host = "0.0.0.0"
port = 12500
buf = 1024
# bundle em
addr = (host, port)

# init socket
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(addr)
print("listening @ port 12500")

# start a capture
camera = cv2.VideoCapture(0)

# bool to be triggered
blendSwitch = False
while True:
        _,frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 15, 30)

        (data, addr) = serverSocket.recvfrom(buf)
        data.decode('utf-8')
        #print(data)


        if data == b'1':
                blend = cv2.addWeighted(gray, 0.1, canny, 0.9, 0)
        elif data == b'0':
                blend = cv2.addWeighted(gray, 0.9, canny, 0.1, 0)
        else:
                print('got weird data')

                
                
        #print(blendSwitch)
        cv2.imshow("triggered blend", blend)
        k = cv2.waitKey(30) & 0xff
        if k == 113:
                break

serverSocket.close()
cv2.destroyAllWindows()
