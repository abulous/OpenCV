import os
import cv2
import numpy as np
import sys
import time
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

os.environ['SDL_VIDEO_WINDOW_POS'] = "0.0"
os.environ['DISPLAY'] = ':0.0'

comm.Barrier()

folder = './'

haar_path = './'
faceCL = cv2.CascadeClassifier(haar_path+'haarcascade_frontalface_default.xml')

if rank == 0:
    cap = cv2.VideoCapture(0)
reader1 = cv2.VideoCapture('vid1.avi')
reader2 = cv2.VideoCapture('vid2.avi')
#ret, frame = cap.read()

fourcc = cv2.VideoWriter_fourcc(*'XVID')

writer1 = cv2.VideoWriter(folder+'vid1.avi', fourcc, 20, (640,480), True)
writer2 = cv2.VideoWriter(folder+'vid2.avi', fourcc, 20, (640,480), True)


def read1_write2(frame_capture):
    '''Read from vid1.avi and write passed frame to vid2.avi'''
    global reader1, writer2
    ret, frame_read = reader1.read()
    
    writer2.write(frame_capture)
    if ret:
        return frame_read
    else:
        return frame_capture

def read2_write1(frame_capture):
    '''Read from vid2.avi and write passed frame to vid1.avi'''
    global reader2, writer1
    ret, frame_read = reader2.read()

    writer1.write(frame_capture)
    if ret:
        return frame_read
    else:
        return frame_capture

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
    writer1 = cv2.VideoWriter(folder+'vid1.avi', fourcc, 20, (640,480), True)
    reader2 = cv2.VideoCapture(folder+'vid2.avi')

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
    writer2 = cv2.VideoWriter(folder+'vid2.avi', fourcc, 20, (640,480), True)
    reader1 = cv2.VideoCapture(folder+'vid1.avi')
    
    

switch = False
newFace = False
noface_counter = 0
noface_buffer = 20 #frames
faces = []

while True:
    #standard live capture
    if rank == 0:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_read = np.zeros_like(frame)

        faces = faceCL.detectMultiScale(gray, 1.3, 5)
        if len(faces) > 0:
            x,y = (faces[0][0], faces[0][1])
            w,h = (faces[0][2], faces[0][3])
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0))

            noface_counter = 0
            newFace = False
        else:
            noface_counter += 1
            print("no face for %d frames" %noface_counter)

    
        if noface_counter == noface_buffer:
            newFace = True


        if newFace: #this if decides WHEN to switch files
            print("switching")
            if switch:
                init_read2_write1()
            else:
                init_read1_write2()
            switch = not switch
            newFace = False

        if switch and not newFace:
            frame_read = read1_write2(frame)
        elif not switch and not newFace:
            frame_read = read2_write1(frame)

        frame_blend = cv2.addWeighted(frame, 0.5, frame_read, 0.5, 0)
        comm.send(frame_blend, dest=1, tag=10)
    if rank == 1:
        frame_blend = comm.recv(source=0, tag=10)
        cv2.imshow("Blended Video", frame_blend)
        cv2.moveWindow("Blended Video", 10,10)
        if cv2.waitKey(33) == 27:
            break



    
cap.release()
reader1.release()
reader2.release()
writer1.release()
writer2.release()

cv2.destroyAllWindows()
print("fin")
