# see https://stackoverflow.com/questions/8403768/parallelism-in-python-isnt-working-right

import multiprocessing as mp
import datetime as dt
def work():
    t = dt.datetime.now()
    print (mp.current_process().name, t)
    i = 0
    while i < 100000000:
        i+=1
    t2 = dt.datetime.now()
    print (mp.current_process().name, t2, t2-t)

if __name__ == '__main__':
    print ("single process:")
    t1 = mp.Process(target=work)
    t1.start()
    t1.join()

    print ("multi process:")
    t1 = mp.Process(target=work)
    t1.start()
    t2 = mp.Process(target=work)
    t2.start()

    # t3 = mp.Process(target=work)
    # t3.start()

    t1.join()
    t2.join()
    # t3.join()
