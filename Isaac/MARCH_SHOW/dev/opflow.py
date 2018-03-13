import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)

# params for ShiTomasi corner detection
feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Create some random colors
color = np.random.randint(0,255,(100,3))

# Take first frame and find corners in it
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)

#timer
timer = time.time()

while(1):
    #new corners every xxx seconds
    if time.time() - timer > 30:
        mask = np.zeros_like(old_frame)
        timer = time.time()
    
    ret,frame = cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    if p1 is not None:
        # Select good points
        good_new = p1[st==1]
        good_old = p0[st==1]
    else:
        #find some new features
        ret, old_frame = cap.read()
        old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
        p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
        good_new = p1[st==1]
        good_old = p0[st==1]

    # draw the tracks
    for i,(new,old) in enumerate(zip(good_new,good_old)):
        a,b = new.ravel()
        c,d = old.ravel()
        mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 20)
        #frame = cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
        
    ###### FOR DEBUG ######
    # convert back to three channels
    backToRGB = cv2.cvtColor(frame_gray, cv2.COLOR_GRAY2RGB)
    #laplacian = cv2.Laplacian(frame_gray, cv2.CV_64F)
    #img = cv2.add(laplacian,mask)
    #img = cv2.add(frame,mask)
    img = cv2.add(backToRGB,mask)

    #now with funky edge detection
    #laplacian = cv2.Laplacian(img, cv2.CV_64F)
    #sobelx = cv2.Sobel(img, cv2.CV_64F,1,0,ksize=5)

    #cv2.imshow('backinrgbnotblack',backToRGB)
    cv2.imshow('frame.. not anymore!',img)
    #cv2.imshow('edgy',sobelx)
    #cv2.imshow('lap', laplacian)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

    # Now update the previous frame and previous points
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1,1,2)

cv2.destroyAllWindows()
cap.release()
