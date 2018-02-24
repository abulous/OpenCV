import time
import threading

class TommysThread(threading.Thread):
  '''This class inherets from threading class.
  This must be done in Python3 to create thread objects
  There is also a depreciated form : _thread
  it is very easy to use, very simple, no classes,
  but far less powerful, and is only offered because Python2 uses it
  '''
  def __init__(self, numPrints):
    '''Thread object
    when run, will print its name, and a counter value.
    @param numPrints the size of the counter
    '''
    threading.Thread.__init__(self)
    self.numPrints = numPrints
    
  def run(self):
    '''Overwrite method
    ------SHOULD NOT BE CALLING THIS DIRECTLY------
    should call yourThreadName.start() NOT yourThreadName.run()

    This function is used to call other functions which do whatever
    you want your thread to be doing.
    '''
    print("Starting" + self.name)
    self.fn()
    print("Exiting" + self.name)

  def fn(self):
    '''HELPER. Tommy just randomly made...
    A silly function to just print values from a for loop.
    also prints the thread name, so that user can distinguish
    between various instantiations of the thread object
    '''
    for i in range(self.numPrints):
      print("%s %d\n" % (self.name, i))
      time.sleep(0.2)


t1 = TommysThread(15)
t2 = TommysThread(10)
t3 = TommysThread(20)


## Mess around with the order of start and end (threadName.join()) 
t1.start()
t2.start() #t2 should finish first, then t1

t1.join() #then t1 closes
#Above line will stop wait until thread t1 has finished running
#before allowing the code to progress on.

t3.start() #then t3 starts

t2.join() #then t2 closes
t3.join() #then t3 closes


print("FIN")
