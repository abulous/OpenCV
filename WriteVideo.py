
import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 640) # Change Width to 640. The 'set' function retrieves it from the camera you're using.
cap.set(4, 480) # Change Height to 480

fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v') # fourcc code for MPEG-4 Video, this works both for mac and pi
writer = cv2.VideoWriter('WriteTest.mov', fourcc, 20, (640, 480), True)
# cv2.VideoWriter(FileName, fourcc_code, FPS, frameSize, is_color=True)
# You'll notice I dropped the FPS to 20, this is because if it is at 30 the video that is written out is sped up for some reason.
# I haven't been able to figure out why, but I find through experimenting that 10-20 FPS is where I want it.


while True:
    ret, frame = cap.read()
    writer.write(frame)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
writer.release()
cv2.destroyAllWindows()







   



            
