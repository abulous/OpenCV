import cv2
import numpy as np

chessboardDims = (9,6)
goodImgs = []
cap = cv2.VideoCapture(0)

##Getting Images from webcam
while True:
    #Get frame frome camera
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #boolean, nparray
    cornersFound, corners = cv2.findChessboardCorners(frame, chessboardDims) #can be color or gray

    if cornersFound:
        #If the chessboard is found, add it to list of good images
        goodImgs.append(frame)
#        for pt in corners: #Can mess with intersections
#            print(pt[0])
#            cv2.circle(frame, (int(pt[0].item(0)), int(pt[0].item(1))), 5, (200,200,0))
    else:
        cv2.putText(frame, "Looking for Chessboard...", (10,200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (250, 0, 255), 4)

    cv2.imshow("LIVE", frame)
    
    if cv2.waitKey(500) == 27:
        cap.release()
        cv2.destroyAllWindows()
        break
    
#Let User pick out bad images
blank_img = np.zeros((480,640,3), np.uint8)
cv2.putText(blank_img, "DELETE to remove", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
cv2.putText(blank_img, "ENTER/SPACE/other to keep", (10,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
cv2.imshow("Instructions", blank_img)
cv2.waitKey(0)
cv2.destroyWindow("Instructions")

inc=0
for i in range(len(goodImgs)-1,  -1, -1):
    winname ="GOOD #"+str(i)
    cv2.imshow(winname, goodImgs[i])
    cv2.moveWindow(winname, 50,50)
    key = cv2.waitKey(0)
    if key == 0:
        goodImgs.pop(i)
        cv2.destroyWindow(winname)
        inc += 1
    else:
        cv2.destroyWindow(winname)
        continue

print(str(len(goodImgs))+" Images of Chessboard Collected in variable goodImgs")
print(str(inc)+" images removed.")


## NOW ON TO MORE PRECISION AND GETTING VECTORS
#I don't know what this line does... "termination criteria"
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

#I don't know what this does either...
# Prepare object points like (0,0,0), (1,0,0), (2,0,0), ..., (6,5,0)
objp = np.zeros((chessboardDims[0]*chessboardDims[1],3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardDims[0],0:chessboardDims[1]].T.reshape(-1,2)

objpoints = [] #3D points in real world space
imgpoints = [] # 3D points in image plane

for i in range(len(goodImgs)):
    img = goodImgs[i]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cornersFound, corners = cv2.findChessboardCorners(img, chessboardDims)

    if cornersFound:
        objpoints.append(objp)

        fineCorners = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        imgpoints.append(fineCorners)

        #Display corners
        imgCopy = cv2.drawChessboardCorners(img, chessboardDims, fineCorners, cornersFound)
        cv2.imshow("Quick Preview", imgCopy)
        cv2.waitKey(300)
    
## Getting Vectors
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

#Saving Everything to a file
cameraName = str(input("Enter a name for this camera: "))
cameraName = cameraName.replace(" ", "_")
fileName = "CameraCalibration_"+cameraName+".txt"

calibFileOut = open(fileName, 'w')
calibFileOut.write("ret = "+str(ret)+"\n")
calibFileOut.write("mtx = "+str(mtx))
calibFileOut.write("dist = "+str(dist)+"\n")
calibFileOut.write("rvecs = "+str(rvecs)+"\n")
calibFileOut.write("tvecs = "+str(tvecs)+"\n")
calibFileOut.close()
