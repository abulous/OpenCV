# boot, then run sc first, then run python second

import argparse
import random
import time

from pythonosc import osc_message_builder
from pythonosc import udp_client


import numpy as np
import cv2

cap = cv2.VideoCapture('vidOnly.mp4')
print(cap.get(5))


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

client.send_message("/toggler", gate)

print(gate)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame_counter += 1
    oscSender += 1

    client.send_message("/filter", oscSender)

    if frame_counter == cap.get(7):
        frame_counter = 0 
        oscSender = 0
        cap.set(1, 0) 
    
    cv2.imshow('frame',frame)
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
