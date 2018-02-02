import numpy as np
import cv2

cap = cv2.VideoCapture('Test.mov') 
frame_counter = 0

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame_counter += 1
    #If the last frame is reached, reset the capture and the frame_counter
    if frame_counter == cap.get(7):
        frame_counter = 0 #Or whatever as long as it is the same as next line
        cap.set(1, 0) #CAP_PROP_POS_FRAMES 0-based index of the frame to be decoded/captured next.
    
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

