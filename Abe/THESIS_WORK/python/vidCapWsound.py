# boot, then run sc first, then run python second

import argparse
import random
import time

from pythonosc import osc_message_builder
from pythonosc import udp_client


import numpy as np
import cv2

cap = cv2.VideoCapture('vidOnly.mp4')
cap1 = cv2.VideoCapture(0)

cap1.set(3, 640)
cap1.set(4, 480)
cap1.set(5, 24)
##print("video", cap.get(3), cap.get(4), cap.get(5))
print("capture", cap1.get(3), cap1.get(4), cap1.get(5))





frame_counter = 0
oscSender = 1
gate = 1


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default="127.0.0.1",
      help="The ip of the OSC server")
  parser.add_argument("--port", type=int, default=57120,
      help="The port the OSC server is listening on")
  args = parser.parse_args()

  client = udp_client.SimpleUDPClient(args.ip, args.port)

time.sleep(1)
client.send_message("/toggler", gate)

print(gate)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    ret1, frame1 = cap1.read()
    frame_counter += 1
    oscSender += 1

    client.send_message("/filter", oscSender)

    if frame_counter == cap.get(7):
        frame_counter = 0 
        oscSender = 0
        cap.set(1, 0) 

    blend= cv2.addWeighted(frame, 0.5, frame1, 0.5, 0)
    cv2.imshow('frame',blend)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()




##for x in range(12872):
###    client.send_message("/filter", random.random())
##    client.send_message("/filter", x)
##    time.sleep(0.1)
####    time.sleep(0.0333)
