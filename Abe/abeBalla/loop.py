import numpy as np
import cv2

video = cv2.VideoCapture('roadO.mov')
video1 = cv2.VideoCapture('roadV.mov') 

counter = 1
counter1 = 1

while(True):
    # Capture frame-by-frame
    ret, play = video.read()
    ret1, play1 = video1.read()

    counter += 1
    if counter == video.get(7):
        counter = 0 #Or whatever as long as it is the same as next line
        video.set(1, 0) #CAP_PROP_POS_FRAMES 0-based index of the frame to be decoded/captured next.

    counter1 += 1
    if counter1 == video1.get(7):
        counter1 = 0 #Or whatever as long as it is the same as next line
        video1.set(1, 0) #CAP_PROP_POS_FRAMES 0-based index of the frame to be de

##    blend = cv2.addWeighted(play, 0.5, play1, 0.5, 0)
    
##    cv2.imshow('blend', blend)
    cv2.imshow('play', play)
    cv2.imshow('play1', play1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
video.release()
cv2.destroyAllWindows()

