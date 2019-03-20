from CirFrameBuf import CirFrameBuf
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

#initialize camera and get reference to the raw camera capture
camera = PiCamera()
#camera.resolution=(640, 480)
camera.resolution=(1280, 720)
#camera.resolution=(1920, 1080)
camera.framerate = 30
#rawCapture = PiRGBArray(camera,size=(640, 480))
rawCapture = PiRGBArray(camera,size=(1280, 720))
#rawCapture = PiRGBArray(camera,size=(1920, 1080))
size = 40

#cfbuf = CirFrameBuf(size+1, height, width, pixdepth)
#cfbuf = CirFrameBuf(size+1, 1080, 1920, 3)
cfbuf = CirFrameBuf(size+1, 720, 1280, 3)
#cfbuf = CirFrameBuf(size+1, 480, 640, 3)
#allow process to warm up
time.sleep(0.1)

#variables for delay line
dframe = None
nfback = 1
inc = 1

#get image from camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    #get raw Numpy array(the image) the initialize time stamp
    #and occupied/unoccupied text 
    image = frame.array
#ABE'S CODE INCOMING
# Write out to the circular buffer
    cfbuf.write(image)
# This is to modulate the delay, so the buffer gets either bigger or smaller
#depending on where it is.
    if nfback >= size: 
        inc = -1
    elif nfback <= 1:
        inc = 2
        nfback += inc

    dframe = cfbuf.readback(nfback)
# Blend the two images: real time and delay time. Must be the same pix depth
    blend = cv2.addWeighted(image, 0.5, dframe, 0.5, 0)
#show the frame
    cv2.imshow("Frame", blend)
    key = cv2.waitKey(1) & 0xFF
#clear the stream in preperation for the next frame
    rawCapture.truncate(0)
#if the q key was pressed, break
    if key == ord("q"):
        break 
