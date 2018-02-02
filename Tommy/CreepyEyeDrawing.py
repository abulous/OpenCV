#Look at your camera
#should show blue around your face, green around your eyes
## Will only recognize the FRONT of your face. not the sides.
#Your eyes must be inside your face... although you can change that requirement

#------------ IMPORTANT --------------
"""
This will absolutely not work on your computer until your figure out
where on your computer the Haar Cascades are saved.
Notice the long string below for a path.
You need to change these to whatever they are on your computer
do a search for:
  haarcascade_frontalface
open the containing folder and copy that path over
you should notice a bunch of .xml files
these are models which have been trained to detect certain objects in images
"""

import cv2 as cv
import numpy as np
import os, sys

path = 'C:\\Users\\tlsha\\AppData\\Local\\Programs\\Python\\Python36-32\\Lib\\site-packages\\cv2\\data\\'
eyeLocs = []
frameHist = []

face_cascade = cv.CascadeClassifier()
face_cascade.load(path+'haarcascade_frontalface_default.xml')
if not face_cascade:
  print("face_cascade.load() failed")
eye_cascade = cv.CascadeClassifier()
eye_cascade.load(path+'haarcascade_eye.xml')
if not eye_cascade:
  print("eye_cascade.load() failed")


cap = cv.VideoCapture(1)


while True:
  ret, frame = cap.read()
  gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
  frameHist.append(frame)
  
  #get faces and eyes
  faces = face_cascade.detectMultiScale(gray, 1.3, 10)
  
  for (x, y, w, h) in faces:
    #cv.circle(frame, (int(x+w/2), int(y+h/2)), h, (255,0,0), 4)
    eye_region = gray[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(eye_region, 1.35, 15)
    #Same variables for the eyes - definitely more finnicky than the face detection
    for (ix, iy, iw, ih) in eyes: #i referring to 'eye'
      cv.circle(frame, (int(x+ix+iw/2), int(y+iy+ih/2)), int(iw/8), (0,255,0), int(w/80))
      eyeLocs.append((x+ix+iw/2, y+iy+iw/2, iw, ih))
    
  if (len(eyeLocs) >= 40):
    eyeLocs.pop(0)
  if (len(frameHist) >= 20):
    frameHist.pop(0)
  #Display
  for i in range(len(eyeLocs)):
    #cv.circle(gray, (int(loc[0]), int(loc[1])), 2, (0,200,0), 2)
    if (i>2):
      if ( abs(eyeLocs[i][0] - eyeLocs[i-2][0]) < eyeLocs[i][3] ):
        #print(abs(eyeLocs[i][1] - eyeLocs[i-2][1]))
        cv.line(frame, (int(eyeLocs[i][0]), int(eyeLocs[i][1])), (int(eyeLocs[i-2][0]), int(eyeLocs[i-2][1])), (0,200,0), 2)
  
  blend = cv.addWeighted(frame, 0.5, frameHist[len(frameHist)-1], 0.5, 0)
  cv.imshow("Hello World", frame)

  #Exit
  if cv.waitKey(1) & 0xFF == ord('q'):
    break


#Wrap everything up
cap.release()
cv.destroyAllWindows()
