# see https://stackoverflow.com/questions/8403768/parallelism-in-python-isnt-working-right

import threading
import datetime as dt

def work():
    t = dt.datetime.now()
    print (threading.currentThread(), t)
    i = 0
    while i < 100000000:
        i+=1
    t2 = dt.datetime.now()
    print (threading.currentThread(), t2, t2-t)

if __name__ == '__main__':
    print ("single threaded:")
    t1 = threading.Thread(target=work)
    t1.start()
    t1.join()

    print ("multi threaded:")
    t1 = threading.Thread(target=work)
    t1.start()
    t2 = threading.Thread(target=work)
    t2.start()
    t1.join()
    t2.join()
