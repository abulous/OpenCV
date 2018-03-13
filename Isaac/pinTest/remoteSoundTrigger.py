# Isaac Nealey
# March 2018
# testing the mic yoooo!
# now its going to send a packet over UDP every frame in order to
# trigger something on the network.
from socket import *
import RPi.GPIO as GPIO
import time

# host = "xxx.xxx.x.x" -inet address for place to send trigger
host = "127.0.0.1"
# port = xxxx -port number
port = 12500
# bundle em together
addr = (host, port)

clientSocket = socket(AF_INET, SOCK_DGRAM) # set up a udp socket

#set pin to input
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
#data = "0"
trigOn = False
trigTimer = time.time()
sendTimer = time.time()
spf = 0.1   # 10 fps:  1sec/10frames = 0.1 spf
# prgm loop
while True:
    # if trigger flipped, send 1
    if trigOn:
        data = "1"
    else:
        data = "0"
        
    # send 'er off @ 10 fps
    if time.time() - sendTimer > spf:
        clientSocket.sendto(data.encode('utf-8'), addr)
        sendTimer = time.time()
    
    # listen for sounds at pin 7
    if GPIO.input(4) == 1:
        if time.time() - trigTimer > 2:
            trigOn = not trigOn
            trigTimer = time.time()
            print('\ntrigger flipped: ')
            print(trigOn)
            
        #print('i heard a sound at time: ')   
        #print(time.time())
        #print()
clientSocket.close()
GPIO.cleanup()

