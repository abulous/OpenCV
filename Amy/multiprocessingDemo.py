#!/usr/local/bin/python3

import multiprocessing
import time, os
# multiprocessingDemo.py  -- amy alexander 5/2018
# simple demo showing how you might use two separate processes

# With multiprocessing, it's good to be careful not to start too many processes
# Cause you can fill the process table and crash the system! 
# So I'm not starting processes in a loop as I did in the threads demo.
# But my functions (processes) have loops within them.

# References:
# https://docs.python.org/3.6/library/multiprocessing.html
# https://pymotw.com/2/multiprocessing/basics.html


# I'll have the processes print out some info, including their pid
# You can run "ps -aef | grep python" in another shell and see each process
# listed with its pid.
# (On OSX, you can do the same with Activity Monitor -- plug in a search for 'python')

def firstThing ():
    procname = multiprocessing.current_process().name
    print ('starting', procname, '. process id:', os.getpid())
    time.sleep(3)

    for i in range (10):
        # your  code here.
        print ("firstThing: " + procname + ": " + str(i) + "\n")

        time.sleep (2)


def secondThing (someargument):
    procname = multiprocessing.current_process().name
    print ('starting', procname, '. process id:', os.getpid())
    time.sleep(3)

    for i in range (14):
        # your code here.

        print ("secondThing: " + procname + ": " + str(i) + " with argument " + someargument + "\n")
        time.sleep(3)


# main function:
procname = multiprocessing.current_process().name
print ('starting', procname, '. process id:', os.getpid())

# start the child processes.
multiprocessing.Process(name="firstThing1", target=firstThing).start()
multiprocessing.Process(name="firstThing2", target=firstThing).start()

# notice how if there's only one argument, you have to put a trailing comma!
multiprocessing.Process(name="secondThing1", args=("howdy",), target=secondThing).start()

print ("Ctrl-C to exit script\n")
