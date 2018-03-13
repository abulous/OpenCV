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
    pts1 = np.float32([[56,65],[368,52],[28,387],[389,398]])   
    pts2 = np.float32([[0,0],[300,0],[0,300],[300,300]])

    M = cv2.getPerspectiveTransform(pts1,pts2)

    dst = cv2.warpPerspective(frame,M,(300,300))

    plt.subplot(121),plt.imshow(frame),plt.title('Input') 
    plt.subplot(122),plt.imshow(dst),plt.title('Output')
    
    plt.show() 
    #cv2.imshow('Basic Capture',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
