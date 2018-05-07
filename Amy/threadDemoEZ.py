#!/usr/local/bin/python3

import threading
import time
# threadDemoEZ.py  -- amy alexander 5/2018
# EZ thread demo
# This uses python3 threading module.  Different module/syntax for python2

# If you want multiprocessing instead of threading, use the multiprocessing module
# https://docs.python.org/3.6/library/multiprocessing.html
# 16.6.1.1. The Process class
# syntax should be almost identical
# https://pymotw.com/2/multiprocessing/basics.html


# Any code that launches a gui probably needs to stay
# in your main thread to keep from crashing python. At least on OSX.

# This script will use threads to walk and chew gum at the same time.

# Threads call functions. So make some functions.
def walk ():
    print ("Starting thread: walk")
    # replace the rest of the function with your real code.
    for i in range (15):
        print ("walking...")
        time.sleep (2)

# you can pass arguments to your threads too.
def chew_gum (brand):
    print ("Starting thread chew_gum.")
    # replace the rest of the function with your real code.
    for i in range (10):
        print ("chewing gum:", brand)
        time.sleep (3)


# main function:

if __name__ == '__main__':
    # your code here in place of sleep
    time.sleep (5)

    # start threads!
    threading.Thread(target=walk).start()
    # when only one argument, you must use trailing comma (i.e. "Trident",)
    threading.Thread(target=chew_gum, args=("Trident",)).start()

    print ("Main thread again!")
