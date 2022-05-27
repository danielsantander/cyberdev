#!/usr/bin/python3
"""
Daemon threading example. 
"""
import logging
import threading
import time

def some_function(name: str):
    """ Arbitrary example function to pass into a thread. Will sleep for 3 seconds.

    Keyword arguments:
    name (str) - name of thread function is passed to
    """
    logging.info(f'Thread {name}: starting')
    while True: time.sleep(3)

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO, datefmt="%H:%M:%S")

    start = time.time()

    logging.info(f'MAIN: start')
    logging.info('MAIN\t: before creating single thread')
    t = threading.Thread(target=some_function, args=(1,), daemon=True)
    logging.info('MAIN\t: before running daemon thread')
    t.start()

    # Despite start() not finishing, the main program will continue to run
    logging.info('MAIN\t: wait for daemon thread to finish')
    
    end = time.time()
    logging.info(f'MAIN\t: all done ({end-start} seconds taken)')
    
