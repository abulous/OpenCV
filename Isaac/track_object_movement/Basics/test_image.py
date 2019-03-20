#import the necessary packages 
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

#initialize camera and get reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)

#allow process to warm up
time.sleep(0.1)

#get image from camera
camera.capture(rawCapture, format="bgr")
image = rawCapture.array

#display capture on the screen and wait for key press
cv2.imshow("Image", image)
cv2.waitKey(0) 
