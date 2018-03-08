import cv2
import numpy as np
import sys
import time

cap = cv2.VideoCapture(1)
reader1 = cv2.VideoCapture('vid1.avi')
reader2 = cv2.VideoCapture('vid2.avi')
ret, frame = cap.read()

fourcc = cv2.VideoWriter_fourcc(*'XVID')

writer1 = cv2.VideoWriter('vid1.avi', fourcc, 20, (640,480), True)
writer2 = cv2.VideoWriter('vid2.avi', fourcc, 20, (640,480), True)


def read1_write2(frame_capture):
    '''Read from vid1.avi and write passed frame to vid2.avi'''
    global reader1, writer2
    ret, frame_read = reader1.read()
    
    writer2.write(frame_capture)
    if ret:
        cv2.imshow("vid1.avi Display", frame_read)
        cv2.moveWindow("vid1.avi Display", 700,10)

def read2_write1(frame_capture):
    '''Read from vid2.avi and write passed frame to vid1.avi'''
    global reader2, writer1
    ret, frame_read = reader2.read()

    writer1.write(frame_capture)
    if ret:
        cv2.imshow("vid2.avi Display", frame_read)
        cv2.moveWindow("vid2.avi Display", 700,500)

def init_read2_write1():
    '''Stop reading from vid1.avi
    Stop writing to vid2.avi
    then start reading from vid2.avi
    and start writing to vid1.avi
    '''
    global reader1, reader2, writer1, writer2
    
    print("\tclosing: r1, w2")
    reader1.release()
    writer2.release()

    print("\topening: r2, w1")
    writer1 = cv2.VideoWriter('vid1.avi', fourcc, 20, (640,480), True)
    reader2 = cv2.VideoCapture('vid2.avi')

def init_read1_write2():
    '''Stop reading from vid2.avi
    Stop writing to vid1.avi
    then start reading from vid1.avi
    and start writing to vid2.avi
    '''
    global reader1, reader2, writer1, writer2

    print("\tclosing: r2, w1")
    reader2.release()
    writer1.release()

    print("\topening: r1, w2")
    writer2 = cv2.VideoWriter('vid2.avi', fourcc, 20, (640,480), True)
    reader1 = cv2.VideoCapture('vid1.avi')
    
    

counter = 0
switch = False

while True:
    #standard live capture
    ret, frame = cap.read()
    cv2.imshow("LIVE CAPTURE - for reference", frame)
    cv2.moveWindow("LIVE CAPTURE - for reference", 10,10)
    if cv2.waitKey(33) == 27: #esc
        break
    
    #switch every 180 frames
    if counter%180 == 0: #this if decides WHEN to switch files
        print("switching")
        if switch:
            init_read2_write1()
        else:
            init_read1_write2()
        switch = not switch

    if switch:
        #read from vid1.avi and write live capture to vid2.avi
        read1_write2(frame)
    else:
        #read from vid2.avi and write live capture to vid1.avi
        read2_write1(frame)

    counter += 1


    
cap.release()
reader1.release()
reader2.release()
writer1.release()
writer2.release()

cv2.destroyAllWindows()
print("fin")
