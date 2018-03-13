# Isaac Nealey
# March 2018
# for use in VIS 198 and show
# much love to pyimagesearch guy

# USAGE
# python track_and_send.py --video object_tracking_example.mp4
# python track_and_send.py

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import socket
import pickle
import cv2
import time

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
help="max buffer size")
args = vars(ap.parse_args())

# init stuff for udp streaming
HOST='0.0.0.0'  # host Inet_4 address for udp x.x.x.x
TRACKING_PORT = 8101 # this comes from clearPi01 - RGB stream

### IMPORTANT ########
# the port for sound input
MIC_PORT = 12501 # this comes from clearPi03

# create and bind the sockets
trackingSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # SOCK_DGRAM for udp
soundSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
print ('\nsockets created')

trackingSocket.bind((HOST, TRACKING_PORT))
soundSocket.bind((HOST, MIC_PORT))
print ('\nSocket binding complete')
print('\nlistening for a 140 x 140 RGB stream @ 8101')
print('listening for a char trigger @ 12500')

trackingData = ""
soundData = ""

# define the lower and upper boundaries of the "green"
# ball in the HSV color space
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
pts = deque(maxlen=args["buffer"])
counter = 0
(dX, dY) = (0, 0)
direction = ""

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
        #camera = cv2.VideoCapture(0)
        print('\nstarting network stream')

# otherwise, grab a reference to the video file
else:
        camera = cv2.VideoCapture(args["video"])

# grab from sound data before we start
soundData = soundSocket.recvfrom(1024)
oldsoundData = soundData
soundToggle = False

# timer
timer = time.time()

# keep looping
while True:
        # get image to track:
        trackingData, addr = trackingSocket.recvfrom(58993) #buffer size of incoming image.
        frame = pickle.loads(trackingData)

        # check sound trigger
        soundData = soundSocket.recvfrom(18)
        if soundData != oldsoundData:
                soundToggle = not soundToggle
                oldsoundData = soundData
        
        # resize the frame, blur it, and convert it to the HSV
        # color space
        frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, greenLower, greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                # only proceed if the radius meets a minimum size
                if radius > 10:
                        # draw the circle and centroid on the frame,
                        # then update the list of tracked points
                        #cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                        cv2.circle(camImg, center, 5, (0, 0, 255), -1)
                        pts.appendleft(center)

        # loop over the set of tracked points
        for i in np.arange(1, len(pts)):
                # if either of the tracked points are None, ignore
                # them
                if pts[i - 1] is None or pts[i] is None:
                        continue

                # check to see if enough points have been accumulated in
                # the buffer
                if counter >= 10 and i == 1 and pts[-10] is not None:
                        # compute the difference between the x and y
                        # coordinates and re-initialize the direction
                        # text variables
                        dX = pts[-10][0] - pts[i][0]
                        dY = pts[-10][1] - pts[i][1]
                        (dirX, dirY) = ("", "")

                        # ensure there is significant movement in the
                        # x-direction
                        if np.abs(dX) > 20:
                                dirX = "East" if np.sign(dX) == 1 else "West"

                        # ensure there is significant movement in the
                        # y-direction
                        if np.abs(dY) > 20:
                                dirY = "North" if np.sign(dY) == 1 else "South"

                        # handle when both directions are non-empty
                        if dirX != "" and dirY != "":
                                direction = "{}-{}".format(dirY, dirX)

                        # otherwise, only one direction is non-empty
                        else:
                                direction = dirX if dirX != "" else dirY

                # otherwise, compute the thickness of the line and
                # draw the connecting lines
                thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
                cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

        # show the movement deltas and the direction of movement on
        # the frame
        #cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                #0.65, (0, 0, 255), 3)
        #cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY),
                #(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                #0.35, (0, 0, 255), 1)

        # reformat img
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        camImg = cv2.resize(gray,(640, 480), interpolation = cv2.INTER_AREA) 

        # show the frame to our screen and increment the frame counter
        canny = cv2.Canny(camImg,60, int(np.abs(dY)), 1)
        if soundToggle == True:
                blend = cv2.addWeighted(camImg, (1 - np.abs(dX / 600)), canny, np.abs(dX / 600), 0)
        else:
                blend = cv2.addWeighted(camImg, np.abs(dX / 600), canny, (1 - np.abs(dX / 600)), 0)
        #blend = cv2.addWeighted(gray, 0.5, canny, 0.5, 0)
        cv2.imshow("remote param mods", blend)
        key = cv2.waitKey(1) & 0xFF
        counter += 1

        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
                break

# cleanup the camera and close any open windows
#camera.release()
cv2.destroyAllWindows()
trackingSocket.close()
soundSocket.close()
