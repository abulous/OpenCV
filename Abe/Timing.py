import numpy as np
import cv2
import random
import datetime

cap = cv2.VideoCapture(0)
#cap_1 = cv2.VideoCapture('Testerzzz.mov')

cap.set(3, 640)
cap.set(4, 480)
cap.set(5, 30)
print(cap.get(3))
print(cap.get(4))
print(cap.get(5))


can_count = 0
gauss_count = 0


can_low = 1
can_high = 2
g_low = 1
g_high = 3

w_0 = 0.5
w_1 = 0.5
w_2 = 0.5
w_3 = 0.5
w_4 = 0.5
w_5 = 0.5
w_6 = 0.5
w_7 = 0.5

val = random.choice([0.01, 0.02, 0.03])
val_1 = random.choice([0.01, 0.01, 0.01, 2, 5])
count = 1

up = 0
down = 0

p_count = 1.00

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    can_count += 2
    gauss_count += 2

    up += 1
    count += 1

    p_count += 1
 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
##    gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    
    can = cv2.Canny(frame, can_low, can_high)
    can = cv2.cvtColor(can, cv2.COLOR_GRAY2BGR)
 


#    gauss = cv2.GaussianBlur(can, (g_low, g_high), 0)

    hot = cv2.applyColorMap(gray, cv2.COLORMAP_HOT)

    ocean = cv2.applyColorMap(gray, cv2.COLORMAP_OCEAN)
    rainbow = cv2.applyColorMap(gray, cv2.COLORMAP_RAINBOW)
    jet = cv2.applyColorMap(gray, cv2.COLORMAP_JET)

    if count == 10:
        val = random.choice([0.01, 0.02, 0.03])
        val_1 = random.choice([0.001, 0.001, 1, 2, 5])
        up += random.choice([1, 2, 5])

        count = 0
#        print(val)

   
    if up < 100:
        w_0 -= val
        w_1 += val

        w_2 -= val*0.5
        w_3 += val*0.5

##        w_4 -= val*3
##        w_5 += val*3
##        w_6 -= val/3
##        w_7 += val/3

        can_high += val_1
        
##        print('down')
        
    if up >= 100 and up < 200:
        w_0 += val
        w_1 -= val

        w_2 += val*3
        w_3 -= val*3

##        w_4 += val*3
##        w_5 -= val*3
##        w_6 += val/3
##        w_7 -= val/3

        can_high -= val_1
##        print('up')

    if up >= 200:
        up = 0
##        print('zero')

    if w_0 < 0:
        w_0 = 0
##        w_0 = w_0 *(-1)
    if w_1 < 0:
        w_1 = 0
##        w_1 = w_1 *(-1)
    if w_2 < 0:
        w_2 = 0
##        w_2 = w_2*(-1)
    if w_3 < 0:
        w_3 = 0
##        w_3 = w_3*(-1)
        
    
    if w_0 > 1:
##        w_0 = (w_0*0.1) + 0.5
        w_0 = 1
    if w_1 > 1:
##        w_1 = (w_1*0.1) + 0.5
        w_1 = 1
    if w_2 > 1:
##        w_2 = (w_2*0.1) + 0.5
        w_2 = 1
    if w_3 > 1:
##        w_3 = (w_3*0.1) + 0.5
        w_3 = 1

    if p_count == 30:
        p_count = 0
        

    if can_high < 0:
        can_high = can_high*(-1)

    if can_high > 300:
        can_high = 3



    # Display the resulting frame

    dst_0 = cv2.addWeighted(hot, w_0, ocean, w_1, 0)
    dst_1 = cv2.addWeighted(hot, w_0, rainbow, w_1, 0)

##    dst_2 = cv2.addWeighted(dst_0, w_4, dst_1, w_5, 0)

    dst_3 = cv2.addWeighted(dst_1, w_2, can, w_3, 0)


    cv2.imshow('yea', dst_3)      
    if  cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

