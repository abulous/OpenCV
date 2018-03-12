import os
import sys
import time
import cv2
from mpi4py import MPI
import subprocess


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
os.environ['DISPLAY'] = ':0.0'

comm.Barrier()

if rank == 0:
    cap = cv2.VideoCapture(0)

while(True):
    if rank == 0:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        comm.send(gray, dest=1, tag=11)
        comm.send(frame, dest=1, tag=10)
    if rank == 1:
        gray = comm.recv(source=0, tag=11)
        frame = comm.recv(source=0, tag=10)
        cv2.imshow('frame', gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.DestroyAllWindows()

