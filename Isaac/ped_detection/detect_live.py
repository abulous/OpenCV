# USAGE
# python detect.py --images images

# import the necessary packages
from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import imutils
import cv2

# init basic capture stuff
#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(1) # works for usb webcam
cap.set(3, 640) # Change Width to 640. The 'set' function retrieves it from the camera you're using.
cap.set(4, 480) # Change Height to 480
print(cap.get(3)) # Print Width
print(cap.get(4)) # Print Height

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

while(True):
        ret, image = cap.read()
        
        # load the image and resize it to (1) reduce detection time
        # and (2) improve detection accuracy
        ret, image = cap.read()
        image = imutils.resize(image, width=min(400, image.shape[1]))
        orig = image.copy()

        # detect people in the image
        (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
                padding=(8, 8), scale=1.05)
        
        # draw the original bounding boxes
        for (x, y, w, h) in rects:
                cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # apply non-maxima suppression to the bounding boxes using a
        # fairly large overlap threshold to try to maintain overlapping
        # boxes that are still people
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

        # draw the final bounding boxes
        for (xA, yA, xB, yB) in pick:
                cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

        # show some information on the number of bounding boxes
        # () () () adapt this later ...
        #filename = imagePath[imagePath.rfind("/") + 1:]
        #print("[INFO] {}: {} original boxes, {} after suppression".format(
                #filename, len(rects), len(pick)))

        # show the output images
        # only show final result for live stream
        #cv2.imshow("Before NMS", orig)
        cv2.imshow("After NMS", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break

cap.release()
cv2.destroyAllWindows()
