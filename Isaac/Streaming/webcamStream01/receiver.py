# taken from: https://github.com/yushuhuang/webcam
# being a demo, this code is clunky and could be improved in many ways
#   (tailored for desired performance)
#
# usage: python3 reciever.py
#   -start before sender.
# set 'host' and 'port' to address of --THIS-- machine

from socket import *
import numpy as np
import cv2

host = "127.0.0.1"
port = 4096
buf = 1024
addr = (host, port)
fName = 'img.jpg'
timeOut = 0.05

def foo():
    while True:
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind(addr)

        data, address = s.recvfrom(buf)
        f = open(data, 'wb')

        data, address = s.recvfrom(buf)

        try:
            while(data):
                f.write(data)
                s.settimeout(timeOut)
                data, address = s.recvfrom(buf)
        except timeout:
            f.close()
            s.close()
        image = cv2.imread(fName)
        cv2.imshow('recv', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    foo()
    cv2.destroyAllWindows()
