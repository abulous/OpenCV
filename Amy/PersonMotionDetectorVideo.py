import numpy as np
import cv2
from imutils.video import FPS
import imutils
import time

# amy alexander 4/18 -- script for analyzing videos to determine if they
# a) have people (faces) in them and b) are primarily moving video (not slide shows)

def main ():
    # just for testing
    for i in range (1, 4):
        name = "video" + str(i) + ".mp4"
        print (name)
        (foundfaces, foundmovement) = videoproc(name)
        print ("Faces: " + str(foundfaces))
        print ("Live action: " + str(foundmovement))
        if (foundfaces and foundmovement):
            print ("Decision: OK\n")
        else:
            print ("Decision: No Good\n")

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
    # cv2.imshow("frame", oneframe)
    return myfacecount

def motiondetect(mycurframe, myprevframe, mywidth):
    # quick n dirty frame differencing to decide if there's movement
    diff_frames = cv2.absdiff(mycurframe, myprevframe)
    movement = cv2.countNonZero(diff_frames)
    if movement > mywidth: # TODO ... rough figure that represents reasonable movement after quartering.
        return 1
    else:
        return 0

def videoproc (filename):
    # main video capture / processing loop.

    fps = FPS().start()
    cap = cv2.VideoCapture(filename)
    # width = cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)   # float
    analyzewidth = 320

    procframes = 0
    framestoanalyze = 600 # analyze first x frames of video.
    fcount = 0
    movingframes = 0

    step = 1 # analyze every step frames.
    # On MP4's, doesn't seem to work right except with step 1.

    for procframes in range (0, framestoanalyze, step):
        grabbed, frame = cap.read()

        if not grabbed:
            break

        # imutils resize seems faster
        frame = imutils.resize(frame, width=analyzewidth)
        # frame = cv2.resize(frame, None, fx=0.25, fy=0.25,interpolation=cv2.INTER_CUBIC)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cur_frame = gray

        fcount = fcount + facesearch (gray)

        if procframes > 0:
                movingframes = movingframes + motiondetect(cur_frame, prev_frame, analyzewidth * 4)


        # once we get enough frames of faces and motion, we don't need to finish analyzing the frames
        if (fcount > ((framestoanalyze/step) / 10)) and (movingframes > ((framestoanalyze/step) * 0.66)):
            facemovie = True
            liveaction = True
            print ("finishing analysis early at frame " + str(procframes))
            break


        prev_frame = cur_frame


        # can comment out next lines if not displaying
        # key = cv2.waitKey(25) & 0xFF
        # if key == ord("q"):
        #     break

        fps.update()


        # stop the timer and display FPS information
    fps.stop()
    print ("Last analyzed frame is " + str(procframes))
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # Are there faces in at least 10% of the frames? (to limit false positives)
    print ("there were " + str(fcount) + " frames with faces")
    print ("there were " + str(movingframes) + " moving frames")

    if fcount > ((framestoanalyze/step) / 10):
        facemovie = True
    else:
        facemovie = False


    if movingframes > ((framestoanalyze/step) * 0.66):
        liveaction = True
    else:
        liveaction = False

    return(facemovie, liveaction)


main()
