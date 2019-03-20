import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while( True ):
	_,frame = cap.read()
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	lower_red = np.array([170,10,10])
	upper_red = np.array([255,255,255])

	mask = cv2.inRange(hsv, lower_red, upper_red)
	result = cv2.bitwise_and(frame, frame, mask = mask)

	cv2.imshow('result', result)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
cv2.destroyAllWindows()
cap.release()
