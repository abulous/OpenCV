import numpy as np
import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 640) # Change Width to 640. The 'set' function retrieves it from the camera you're using.
cap.set(4, 480)

fgbg = cv2.createBackgroundSubtractorMOG2()

while(1):
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)

    cv2.imshow('frame',fgmask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
