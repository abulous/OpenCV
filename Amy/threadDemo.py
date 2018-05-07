#!/usr/local/bin/python3

import threading
import time
# threadDemo.py  -- amy alexander 5/2018
# simple demo showing how you might use two separate threads, e.g. to download
# videos and analyze in opencv in a parallel thread
# This uses python3 threading module.  Different module/syntax for python2

# If you want multiprocessing instead of threading, use the multiprocessing module
# https://docs.python.org/3.6/library/multiprocessing.html
# 16.6.1.1. The Process class
# syntax should be almost identical
# https://pymotw.com/2/multiprocessing/basics.html


# Any code that launches a gui probably needs to stay
# in your main thread to keep from crashing python. At least on OSX.

def download (threadname):
    print ("Starting thread " + threadname)
    # code to download one video here


def analyze (threadname, mysearchresponse):
    print ("Starting thread " + threadname)
    print ("Now analyzing " + mysearchresponse)
    # your analyze code here


# main function

if __name__ == '__main__':
# calling threads in a loop for demo:
print ("Ctrl-C to exit script\n")
for i in range(10):
    # let's pretend I'm downloading and analyzing 10 videos
    # start threads. In this case, I'm starting a new thread for each video.
    # notice how if there's only one argument, you have to put a trailing comma!
    threading.Thread(target=download, args=("download",)).start()
    threading.Thread(target=analyze, args=("analyze","searchresult")).start()

    # I'm just putting this sleep in so demo doesn't fly by so fast
    time.sleep (2)
