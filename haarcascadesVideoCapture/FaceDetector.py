import numpy as np
import cv2

width = 640
height = 480

iWIDTH = 3
iHEIGHT = 4
iFPS = 5 # Frames per Second

cap = cv2.VideoCapture(0)

cap.set(iWIDTH, width)
cap.set(iHEIGHT, height)
cap.set(iFPS, 30)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')



while True:

        ret, frame = cap.read()
        
        frame = cv2.resize(frame, None, fx=0.25, fy=0.25,interpolation=cv2.INTER_CUBIC)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        

        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
        for (x,y,w,h) in faces:
                img = cv2.rectangle(gray,(x,y),(x+w,y+h),255,2)
                if x>1:
                        print("I SEE YOU")
        # Bad latency, but uncomment if you want to see it. Comment out cv2.resize if you want
        #cv2.imshow("frame", gray)
        key = cv2.waitKey(25) & 0xFF
        if key == ord("q"):
            break



cap.release()
cv2.destroyAllWindows()
