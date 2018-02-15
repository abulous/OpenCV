from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

#initialize camera and get reference to the raw camera capture
camera = PiCamera()
camera.resolution=(640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera,size=(640, 480))

#allow process to warm up
time.sleep(0.1)

#get image from camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	#get raw Numpy array(the image) the initialize time stamp
	#and occupied/unoccupied text 
	image = frame.array

	#show the fram
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF

	#clear the stream in preperation for the next frame
	rawCapture.truncate(0)

	#if the q key was pressed, break
	if key == ord("q"):
		break 
