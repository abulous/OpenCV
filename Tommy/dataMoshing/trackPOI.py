from poiMovement import *
import cv2
import numpy as np
import time

someCol = (100, 0, 255)
someThick = 2

cap = cv2.VideoCapture(0)
time.sleep(1)

setPOI_params(500, 0.02, 3, 3) #Mess around with these values

def setup():
  ret, frame = cap.read()
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  init(gray)
  global mask
  mask = np.zeros_like(frame) #use for drawing later

while True:
  ret, frame = cap.read()
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  try:
    change = getChange(gray)
    #will raise a trackback error if all POIs are lost
  except:
    setup()
    #restart program if lost all POIs
    continue
  
  for poiPair in change:
    mask = cv2.line(mask, poiPair[0], poiPair[1], someCol, someThick)

  frame_forDisplay = cv2.add(frame, mask)
  cv2.imshow("POI Movement", frame_forDisplay)
  if cv2.waitKey(33) == 27:
    cap.release()
    cv2.destroyAllWindows()
    break
