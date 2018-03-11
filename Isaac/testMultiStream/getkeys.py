import time
import cv2

while (1):
    time.sleep(2)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    print(k)
    
    
    
