#!/usr/local/bin/python3

import threading
import time
# threadDemo.py  -- amy alexander 5/2018
# simple demo showing how you might use two separate threads, e.g. to download
# videos and analyze in opencv in a parallel thread
# This uses python3 threading module.  Different module/syntax for python2

# If you want multiprocessing instead of threading, use the Process module
# https://docs.python.org/2/library/multiprocessing.html
# 16.6.1.1. The Process class
# syntax should be almost identical

# Any code that launches a gui probably needs to stay
# in your main thread to keep from crashing python. At least on OSX.

def download (threadname):
    print ("Starting thread " + threadname)
    # your download code here.


def analyze (threadname, mysearchresponse):
    print ("Starting thread " + threadname)
    print ("Now analyzing " + mysearchresponse)
    # your analyze code here

# putting threads in an endless loop for demo. in reality, you would probably
# want something like
# for search_result in search_response.get("items", []):
while True:

    # start threads.
    # notice how if there's only one argument, you have to put a trailing comma!
    threading.Thread(target=download, args=("download",)).start()
    threading.Thread(target=analyze, args=("analyze","searchresult")).start()

    # code in your main thread
    print ("Ctrl-C to exit script\n")

    # I'm just putting this sleep in for the sake of the demo's endless loop.
    time.sleep (2)
