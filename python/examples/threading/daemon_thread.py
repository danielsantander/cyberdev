#!/usr/bin/python3
"""
Daemon threading example.
"""
import logging
import threading
import time

def some_function(name: str):
    """
    Arbitrary example function to pass into a thread. Will sleep for 3 seconds.

    Keyword arguments:
    name (str) - name of thread function is passed to
    """
    start = time.time()
    logging.info(f'{name} THREAD: starting')
    time.sleep(3)
    end = time.time()
    logging.info(f'{name} THREAD: finished in {end-start} seconds')

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO, datefmt="%H:%M:%S")

    start = time.time()

    logging.info(f'MAIN: start')
    logging.info('MAIN: before creating single thread')
    t = threading.Thread(target=some_function, args=('DAEMON',), daemon=True)
    logging.info('MAIN: before running daemon thread')
    t.start()

    # Despite start() not finishing, the main program will continue to run
    logging.info('MAIN: continues to run after starting thread')

    end = time.time()
    logging.info(f'MAIN: all done, finished in {end-start} seconds')
