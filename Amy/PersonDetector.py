import numpy as np
import cv2

# amy alexander  04/18
# Adapted from FaceDetector demo in the Basics & Trix folder.
# find faces and profiles in still images



def main ():
    # # for testing only
    for i in range (1, 9):
        name = "thumb" + str(i) + ".jpg"
        print (name)
        (foundfaces, foundprofiles) = facesearch(name)
        print ("I found " + str(foundfaces) + " faces")
        print ("I found " + str(foundprofiles) + " profiles\n\n")

def facesearch (filename):

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    profile_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')
    frame = cv2.imread(filename,0)
    # height, width, channels = frame.shape
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    faces = face_cascade.detectMultiScale(frame, 1.1, 5)
    profiles = profile_cascade.detectMultiScale(frame, 1.1, 5)

    fcount = 0
    pcount = 0

    for (x,y,w,h) in faces:
        # comment out next line if not displaying
        cv2.rectangle(frame,(x,y),(x+w,y+h),255,2)
        if x>1:
                fcount = fcount + 1

    for(x,y,w,h) in profiles:
        # comment out next line if not displaying
        cv2.rectangle(frame,(x,y),(x+w,y+h),255,2)
        if x>1:
            pcount = pcount + 1

    # comment out next 3 lines if not displaying
    cv2.imshow('picture',frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return (fcount, pcount)


main()
