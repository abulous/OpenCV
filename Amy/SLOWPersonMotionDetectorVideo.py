#FileVideoStream is supposed to be faster than cv2.VideoCapture.. but so far it isn't!
# Especially slow in python3

import numpy as np
import cv2
from imutils.video import FileVideoStream
from imutils.video import FPS
import imutils
import time

def main ():
    for i in range (1, 4):
        name = "video" + str(i) + ".mp4"
        print (name)
        (foundfaces, foundmovement) = videoproc(name)
        print ("Faces: " + str(foundfaces))
        print ("Live action: " + str(foundmovement))
        if (foundfaces and foundmovement):
            print ("Decision: ok\n")
        else:
            print ("Decision: no good\n")

def facesearch (oneframe):
    myfacecount = 0
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(oneframe, 1.1, 5)

    for (x,y,w,h) in faces:
        # comment out next line if not displaying
        # cv2.rectangle(oneframe,(x,y),(x+w,y+h),255,2)

        if x>1:
            myfacecount = myfacecount + 1

    # comment out next line if not displaying
    #cv2.imshow("frame", oneframe)
    return myfacecount

def motiondetect(mycurframe, myprevframe, mywidth):
    #  quick n dirty frame differencing, since I just want yes or no answer
    #  (i.e. no image pre-processing)
    diff_frames = cv2.absdiff(mycurframe, myprevframe)
    movement = cv2.countNonZero(diff_frames)
    if movement > mywidth: # TODO ... rough figure that represents reasonable movement after quartering.
        return 1
    else:
        return 0

def videoproc (filename):
    # main video capture / processing loop.
    print("[INFO] starting video file thread...")
    # FileVideoStream is threaded, so you read and decode in separate threads
    fvs = FileVideoStream(filename ).start()
    time.sleep(1.0)
    # start the FPS timer
    fps = FPS().start()

    # cap = cv2.VideoCapture(filename)
    # width = cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)   # float
    width = 1280

    # while fvs.more():
    # 	# grab the frame from the threaded video file stream, resize
    # 	# it, and convert it to grayscale (while still retaining 3
    # 	# channels)
    # 	frame = fvs.read()
    # 	frame = imutils.resize(frame, width=450)
    # 	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 	frame = np.dstack([frame, frame, frame])
    #
    # 	# display the size of the queue on the frame
    # 	cv2.putText(frame, "Queue Size: {}".format(fvs.Q.qsize()),
    # 		(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    #


    procframes = 0
    framestoanalyze = 600 # analyze first x frames of video.
    fcount = 0
    movingframes = 0

    for procframes in range (0, framestoanalyze, 1):
        frame = fvs.read()
        frame = imutils.resize(frame, width=320)
        #frame = cv2.resize(frame, None, fx=0.25, fy=0.25,interpolation=cv2.INTER_CUBIC)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cur_frame = gray

        fcount = fcount + facesearch (gray)

        if procframes > 0:
                movingframes = movingframes + motiondetect(cur_frame, prev_frame, width)


        # once we get enough frames of faces and motion, we don't need to finish analyzing the frames
        if (fcount > (framestoanalyze / 10)) and (movingframes > (framestoanalyze * 0.66)):
            facemovie = True
            liveaction = True
            print ("finishing analysis early at frame " + str(procframes))
            break


        prev_frame = cur_frame
        # procframes= procframes + 1

        # can comment out next lines if not displaying
        # key = cv2.waitKey(25) & 0xFF
        # if key == ord("q"):
        #     break


        fps.update()


    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))



    # Are there faces in at least 10% of the frames? (to limit false positives)
    print ("there were " + str(fcount) + " frames with faces")
    print ("there were " + str(movingframes) + " moving frames")

    if fcount > (framestoanalyze / 10):
        facemovie = True
    else:
        facemovie = False


    if movingframes > (framestoanalyze * 0.66):
        liveaction = True
    else:
        liveaction = False

    return(facemovie, liveaction)


main()
