#camera.py

import cv2
import time

class VideoCamera(object):
    def __init__(self):
        #capture from device 0
        self.video = cv2.VideoCapture(0)
        time.sleep(2.0)
        
    def __del__(self):
        self.video.release()
        
    def get_frame(self):
        success, image = self.video.read()
        # we are using Motion JPEG, but opencv defaults to raw images,
        # so we must encode it to JPEG to correctly display the video stream
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()