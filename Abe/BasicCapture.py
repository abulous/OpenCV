import numpy as np
import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 640) # Change Width to 640. The 'set' function retrieves it from the camera you're using.
cap.set(4, 480) # Change Height to 480
print(cap.get(3)) # Print Width
print(cap.get(4)) # Print Height

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
   

    # Change to gray if you want 1 channel of depth. 3 for color. Width x Height x Depth
#    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   
 # Display the resulting frame
    cv2.imshow('Basic Capture',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
