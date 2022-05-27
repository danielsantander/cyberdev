#!/usr/bin/python3
"""
Multithreading Example
Author: Daniel Santander
"""
import threading
import logging
import time

logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO, datefmt="%H:%M:%S")
total = 0

def task_one(x:int=10, sleep_time:int=1):
    global total
    for i in range(x):
        time.sleep(sleep_time)
        total += 1
        logging.info('TASK ONE: added to total')
    logging.info('TASK ONE: exiting')

def task_two(x:int=8, sleep_time:int=2):
    global total
    for i in range(x):
        time.sleep(sleep_time)
        total += 1
        logging.info('TASK TWO: added to total')
    logging.info('TASK TWO: exiting')

def limit_total(limit:int=5):
    """
    Limits the global total value with the given limit.
    """
    global total
    count = 0
    while True:
        count += 1
        logging.info(f'LIMIT: count is {count}')
        logging.info(f'LIMIT: total is {total}')
        if total > limit:
            logging.warning('OVERLOAD, subtracking 2')
            total -= 2
        else:
            time.sleep(1)
            logging.info('LIMIT: waiting...')

start = time.time()

logging.info('MAIN: creating tasks')
task1 = threading.Thread(target=task_one)
task2 = threading.Thread(target=task_two)

# limit_total method contains an infinite while loop, 
# set as  deamon thread to terminate when main program completes.
limitor = threading.Thread(target=limit_total, daemon=True)


logging.info('MAIN: starting threads')
task1.start()
task2.start()
limitor.start()

task1.join()
task2.join()
# note: do not join the limitor thread (contains infinite loop that will break program if joined)

end = time.time()

logging.info(f'MAIN: final total value is {total}')
logging.info(f'MAIN: end program ({end - start} seconds)')
# print (time.perf_counter())
