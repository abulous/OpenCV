# Isaac Nealey
# testing the mic yoooo!

import RPi.GPIO as GPIO
import time

#set pin to input
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
start = time.time()
while True:
    file = open("/home/pi/soundTrig/soundTrigger.txt","w")
    
    # listen for sounds at pin 7
    if GPIO.input(4) == 1:
        print('i heard a sound at: ')   
        print(time.time())
        print()
        file.write("1")
    else:
        file.write("0")
    file.close() 
    # break after a half minute of listening 
    if time.time() - start > 30:
        break
print('\n sound test complete')
GPIO.cleanup()

