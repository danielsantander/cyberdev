#!/usr/bin/python3
"""
Threading examples and demos. 

usage:
    - single thread: python3 threads.py 
    - single daemon thread: python3 threads.py daemon
    - single thread joined: python3 threads. join
    - multi threads: python3 threads.py multi
    - multi daemon threads: python3 threads.py multi daemon
    - multi thread joined: python3 threads.py multi join

"""
import logging
import threading
import time
import sys

def print_usage(): 
    print ("""
    usage:
    - single thread: python3 threads.py 
    - single daemon thread: python3 threads.py daemon
    - single thread joined: python3 threads. join
    - multi threads: python3 threads.py multi
    - multi daemon threads: python3 threads.py multi daemon
    - multi thread joined: python3 threads.py multi join
    """)
    sys.exit()


def some_function(name: str):
    """ Arbitrary example function to pass into a thread. Will sleep for 3 seconds.

    Keyword arguments:
    name (str) - name of thread function is passed to
    """
    logging.info(f'Thread {name}: starting')
    time.sleep(3)
    logging.info(f'Thread {name}: finishing')

if __name__ == '__main__':
    # python3 threads.py arg1 arg2 arg3 ...
    arg0 = sys.argv[0]
    arg1 = (sys.argv[1]) if len(sys.argv) >=2 else ''
    arg2 = (sys.argv[2]) if len(sys.argv) >=3 else ''
    arg3 = (sys.argv[3]) if len(sys.argv) >=4 else ''
    arg_list = [arg0,arg1,arg2,arg3]

    if arg1 == 'usage': print_usage()

    logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO, datefmt="%H:%M:%S")

    use_single_thread = True if (arg1 != 'multi') else False
    is_daemon: bool = ('daemon' in arg_list)
    use_join: bool = ('join' in arg_list)
    logging.info(f'MAIN\t: running {"single " if use_single_thread else "multi-"}thread {"(daemon) " if is_daemon else ""}{"(joined)" if use_join else ""}')

    start = time.time()
    if use_single_thread:
        logging.info('MAIN\t: before creating single thread')
        t = threading.Thread(target=some_function, args=(1,), daemon=is_daemon)
        logging.info('MAIN\t: before running single thread')
        t.start()

        # Despite start() not finishing, the main program will continue to run
        logging.info('MAIN\t: wait for single thread to finish')

        # join() to wait for thread to complete before proceeding
        if use_join: t.join()

    # multi-threading
    else:
        thread_list = []
        
        logging.info('MAIN\t: before creating multi-threads')

        for i in range(5):
            t = threading.Thread(target=some_function, name=f'multi-thread-{i}', args=(i,), daemon=is_daemon)
            thread_list.append(t)
            t.start()

        logging.info('MAIN\t: wait for multi-threads to finish')    

        if (use_join):
            for index, t in enumerate(thread_list):
                logging.info(f"Main    : before joining thread {index}.")
                t.join()
                logging.info(f"Main    : thread {index} done")

    end = time.time()
    logging.info(f'MAIN\t: all done ({end-start} seconds taken)')
    
