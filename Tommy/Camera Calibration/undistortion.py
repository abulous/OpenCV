import cv2
import numpy as np
from cv2 import aruco
import sys

try:
    mtx = np.load("CALIB/mtx.npy")
    dist = np.load("CALIB/dist.npy")
    rvecs = np.load("CALIB/rvecs.npy")
    tvecs = np.load("CALIB/tvecs.npy")
except:
    print("No calibration files in CALIB folder")
    print("or CALIB folder is missing from current directory.")
    print("Please run CamCalibration.py to calibrate camera.")
    print("Then run undistortion.py")
    sys.exit()
    

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    h, w = frame.shape[:2]
    newCameraMTX, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    #x,y,w,h = roi
    
    #Undistort
    newFrame = cv2.undistort(frame, mtx, dist, None, newCameraMTX)
    #newFrame = newFrame[y:y+h, x:x+w]

    cv2.imshow("HI", newFrame)
    if cv2.waitKey(30) == 27:
        cap.release()
        cv2.destroyAllWindows()
        break
    
