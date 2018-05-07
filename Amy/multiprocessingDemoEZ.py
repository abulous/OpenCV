#!/usr/local/bin/python3

import multiprocessing
import time, os
# multiprocessingDemoEZ.py  -- amy alexander 5/2018
# EZ multiprocessing demo
# Written for python3, but multiprocessing appears to be the same in python2


# Any code that launches a gui probably needs to stay
# in your main thread to keep from crashing python. At least on OSX.

# This script will use mulitprocessing to walk and chew gum at the same time.

# Multiprocessing processes call functions. So make some functions.
def walk ():
    print ("Starting process: walk. My process ID is", os.getpid())

    # replace the rest of the function with your real code.
    for i in range (15):
        print ("walking...")
        time.sleep (2)

# you can pass arguments to your threads too.
def chew_gum (brand):
    print ("Starting process chew_gum. My process ID is", os.getpid())

    # replace the rest of the function with your real code.
    for i in range (10):
        print ("chewing gum:", brand)
        time.sleep (3)


# main function:
if __name__ == '__main__':
    # your code here in place of sleep
    print ("Main process: My process ID is", os.getpid())
    time.sleep(5)

    # start threads!
    multiprocessing.Process(target=walk).start()
    # when only one argument, you must use trailing comma (i.e. "Trident",)
    multiprocessing.Process (target=chew_gum, args=("Trident",)).start()

    print ("Main process again!  My process ID is still", os.getpid())
