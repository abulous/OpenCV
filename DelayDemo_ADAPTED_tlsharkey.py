from CirFrameBuf import CirFrameBuf
import numpy as np
import cv2

path = '/home/pi/opencv-3.3.0/data/haarcascades/'

faceHist = []

face_cascade = cv2.CascadeClassifier()
face_cascade.load(path+'haarcascade_frontalface_default.xml')
if face_cascade.empty():
  print("face_cascade.load() failed")
eye_cascade = cv2.CascadeClassifier()
eye_cascade.load(path+'haarcascade_eye.xml')
if eye_cascade.empty():
  print("eye_cascade.load() failed")

  
width = 640
height = 480
size = 40 # ...# of frames
pixdepth = 1

cfbuf = CirFrameBuf(size+1, height, width, pixdepth)
cap = cv2.VideoCapture(0)

iWIDTH = 3
iHEIGHT = 4
iFPS = 5 # Frames per Second

cap.set(iWIDTH, width)
cap.set(iHEIGHT, height)
cap.set(iFPS, 30)


print(width)
print(height)
print(cap.get(iFPS))

count = 0

dframe = None

nfback = 1
inc = 1

while True:

        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        

# Write out to the circular buffer
        cfbuf.write(gray)

# This is to modulate the delay, so the buffer gets either bigger or smaller depending on where it is.
        if nfback >= size: 
            inc = -1
        elif nfback <= 1:
            inc = 2
        nfback += inc
        nfback = 10
        while len(faceHist) > nfback:
                faceHist.pop(0)
        

        dframe = cfbuf.readback(nfback)

        #Face
        faces = face_cascade.detectMultiScale(gray, 1.3, 10)
        for (x, y, w, h) in faces:
                #cv2.circle(gray, (int(x+w/2), int(y+h/2)), int(h/2), (255), 4)
                faceHist.append( (x, y, w, h) )
                cntr = (int(x+w/2), int(y+h/2))
                cntr_ofHist = (int( faceHist[0][0] + faceHist[0][2]/2 ), int( faceHist[0][1] + faceHist[0][3]/2 ))
                cv2.line(gray, cntr, cntr_ofHist, (0), 10)
                cv2.circle(gray, cntr, h, (0), h)
                cv2.circle(dframe, cntr_ofHist, faceHist[0][2], (255), faceHist[0][2])
# Blend the two images: real time and delay time. Must be the same pix depth
        blend = cv2.addWeighted(gray, 0.5, dframe, 0.55, 0)
        
        cv2.imshow("frame", blend)

        key = cv2.waitKey(25) & 0xFF
        if key == ord("q"):
            break

print("Info Cleaning Up")
cap.release()
cv2.destroyAllWindows()







   



            
