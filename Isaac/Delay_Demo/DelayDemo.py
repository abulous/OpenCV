from CirFrameBuf import CirFrameBuf
import numpy as np
import cv2

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

        dframe = cfbuf.readback(nfback)

# Blend the two images: real time and delay time. Must be the same pix depth
        blend = cv2.addWeighted(gray, 0.5, dframe, 0.5, 0)
        
        cv2.imshow("frame", blend)

        key = cv2.waitKey(25) & 0xFF
        if key == ord("q"):
            break

print("Info Cleaning Up")
cap.release()
cv2.destroyAllWindows()







   



            
