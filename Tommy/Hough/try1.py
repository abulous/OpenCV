import cv2
import numpy as np
import math


cap = cv2.VideoCapture(0)
ret, frame = cap.read()

mask = np.zeros_like(frame)
blank = np.zeros_like(frame)

def drawHoughP(lines):
    global blank
    for line in lines:
        line = line[0] #numpy mess

##        rho = line[0]
##        theta = line[1]
##
##        a = math.cos(theta)
##        b = math.sin(theta)
##
##        x0 = a*rho
##        y0 = b*rho
##
##        pt1 = (int(x0 + 1000*(-b)), int(y0 + 100*(a)))
##        pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
##        blank = cv2.line(blank, pt1, pt2, (0,100,100,100), 2)

        pts = ( (line[0], line[1]), (line[2], line[3]) )
        blank = cv2.line(blank, pts[0], pts[1], (0,100,100,100), 2)

def drawHoughPolar(lines):
    global blank
    for line in lines:
        line = line[0]
        r = line[0]
        theta = line[1]

        x = int(r*math.cos(theta))
        y = int(r*math.sin(theta))

        trans = (100,100)
        blank = cv2.line(blank, (x+trans[0],y+trans[1]), (x+trans[0],y+trans[1]), (100,0,255,255), 2)
    #blank = cv2.line(blank, (trans[0], trans[1]), (trans[0], trans[1]), (255,0,0,255), 10)


while True:
    ret, frame = cap.read()
    edges = cv2.Canny(frame, 50, 200)
    cv2.imshow("CANNY", edges)
    hough = cv2.HoughLines(edges, 1, math.pi/180, 50, 1, 10)
    blank = np.zeros_like(frame)

    drawHoughPolar(hough)

    display = cv2.add(frame, blank)
    cv2.imshow("not HOUGH", blank)
    if cv2.waitKey(33) == 27:
        cap.release()
        cv2.destroyAllWindows()
        break



