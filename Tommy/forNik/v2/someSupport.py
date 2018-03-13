import threading
import cv2
import numpy as np
import sys, os, time

path_to_mpi = 'mpi/'
fourcc = cv2.VideoWriter_fourcc(*'XVID')

reader1 = cv2.VideoCapture('vid1.avi')
reader2 = cv2.VideoCapture('vid2.avi')

writer1 = cv2.VideoWriter(path_to_mpi+'vid1.avi', fourcc, 20, (640,480), True)
writer2 = cv2.VideoWriter(path_to_mpi+'vid2.avi', fourcc, 20, (640,480), True)

class HaarThread(threading.Thread):
    def __init__(self, faceCL, noface_counter, frame):
        '''Overwriting super'''
        threading.Thread.__init__(self)
        self.breakNow = False
        self.started = False
        self.noFace = False

        self.faceCL = faceCL
        self.noface_counter = noface_counter
        self.frame = frame

    def run(self):
        '''Overwriting super'''
        print(self.name, "started")
        self.started = True
        self.searchForFaces()
        print(self.name, "closed")

    def release(self):
        self.breakNow = True
        
    def searchForFaces(self):
        '''
        Grab global frame read from camera
        search it for faces
        using haar cascades.
        '''
        while True:
            #print("ima thread")
            faces = self.faceCL.detectMultiScale(self.frame, 1.3, 5)
            if len(faces) > 0:
##                x,y = (faces[0][0], faces[0][1])
##                w,h = (faces[0][2], faces[0][3])
##                cv2.rectangle(self.frame, (x,y), (x+w,y+h), (255,0,0))

                self.noface_counter = 0
                self.noFace = False
            else:
                self.noface_counter += 1
                #print("no face for %d frames" %self.noface_counter)

            if self.breakNow:
                break

            #cv2.imshow('HT', self.frame)
            #cv2.moveWindow('HT', 800,10)





#### HELPER FUNCTIONS ####

def read1_write2(frame_capture):
    '''Read from vid1.avi and write passed frame to vid2.avi'''
    global reader1, reader2, writer1, writer2

##    if not reader1.isOpened():
##        print("ERROR - reader1 not open")
##    if not writer2.isOpened():
##        print("ERROR - writer2 not open")
##
##    if not reader2.isOpened():
##        print("\tr2 closed. Check.")
##    if not writer1.isOpened():
##        print("\tw1 closed. Check.")
        
    ret, frame_read = reader1.read()
    
    writer2.write(frame_capture)
    if ret:
        return frame_read
    else:
        return frame_capture
    
def read2_write1(frame_capture):
    '''Read from vid2.avi and write passed frame to vid1.avi'''
    global reader1, reader2, writer1, writer2

##    if not reader2.isOpened():
##        print("ERROR - reader2 not open")
##    if not writer1.isOpened():
##        print("ERROR - writer1 not open")
##
##    if not reader1.isOpened():
##        print("\tr1 closed. Check.")
##    if not writer2.isOpened():
##        print("\tw2 closed. Check.")
        
    ret, frame_read = reader2.read()
    
    writer1.write(frame_capture)
    if ret:
        return frame_read
    else:
        return frame_capture

def close(reader, writer):
    reader.release()
    writer.release()

def init_read2_write1():
    '''Stop reading from vid1.avi
    Stop writing to vid2.avi
    then start reading from vid2.avi
    and start writing to vid1.avi
    '''
    global fourcc, reader1, reader2, writer1, writer2
    
    print("\tclosing: r1, w2")
    reader1.release()
    writer2.release()

    print("\topening: r2, w1")
    writer1 = cv2.VideoWriter(path_to_mpi+'vid1.avi', fourcc, 20, (640,480), True)
    reader2 = cv2.VideoCapture(path_to_mpi+'vid2.avi')

def init_read1_write2():
    '''Stop reading from vid2.avi
    Stop writing to vid1.avi
    then start reading from vid1.avi
    and start writing to vid2.avi
    '''
    global fourcc, reader1, reader2, writer1, writer2

    print("\tclosing: r2, w1")
    reader2.release()
    writer1.release()

    print("\topening: r1, w2")
    writer2 = cv2.VideoWriter(path_to_mpi+'vid2.avi', fourcc, 20, (640,480), True)
    reader1 = cv2.VideoCapture(path_to_mpi+'vid1.avi')
