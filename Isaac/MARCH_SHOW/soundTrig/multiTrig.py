# Isaac Nealey
# March 2018
# testing the mic yoooo!
# now its going to send a packet over UDP every frame in order to
# trigger something on the network.
from socket import *
import RPi.GPIO as GPIO
import time

# host = "xxx.xxx.x.x" -inet address for place to send trigger
stickerPi_IP = "192.168.0.110"
stripePi_IP = "192.168.0.109"
blackPi_IP = "192.168.0.108"
# port = xxxx -port number
port1 = 12500
port2 = 12501
port3 = 12502
# bundle em together
stickerPi = (stickerPi_IP, port1)
blackPi = (blackPi_IP, port2)
stripePi = (stripePi_IP, port3)

stickerSocket = socket(AF_INET, SOCK_DGRAM) # set up a udp socket
blackSocket = socket(AF_INET, SOCK_DGRAM)
stripeSocket = socket(AF_INET, SOCK_DGRAM)

#set pin to input
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

trigOn = False
trigTimer = time.time()
sendTimer = time.time()
#spf = 0.1   # 10 fps:  1sec/10frames = 0.1 spf
#spf = 0.15 
spf = 0.17 
#spf = 0.2
# ^ play with this for preference

print('\nsending out @ 12500, 12501, 12502:')

# prgm loop
while True:
    # if trigger flipped, send 1
    if trigOn:
        data = "1"
    else:
        data = "0"
        
    # send 'er off @ ~10 fps
    if time.time() - sendTimer > spf:
        stickerSocket.sendto(data.encode('utf-8'), stickerPi)
        blackSocket.sendto(data.encode('utf-8'), blackPi)
        stripeSocket.sendto(data.encode('utf-8'), stripePi)
        sendTimer = time.time()
    
    # listen for sounds at pin 7
    if GPIO.input(4) == 1:
        if time.time() - trigTimer > 2:
            trigOn = not trigOn
            trigTimer = time.time()
            print('\ntrigger flipped: ')
            print(trigOn)
            
stickerSocket.close()
blackSocket.close()
stripeSocket.close()
GPIO.cleanup()

