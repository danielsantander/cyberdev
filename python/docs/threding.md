Utilize threading in python to run programs concurrently.

- [Threads](#threads)
  - [Daemon Threads](#daemon-threads)
  - [Joining Threads](#joining-threads)
- [Multiple Threads](#multiple-threads)

# Threads
```python
import logging
import threading
import time

def some_function(name: str):
    logging.info(f'Thread {name}: starting')
    time.sleep(3)
    logging.info(f'Thread {name}: finishing')

if __name__ == '__main__':
    format = '%(asctime)s: %(message)s'
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.info('MAIN\t: before creating thread')

    t = threading.Thread(target=some_function, args=(1,))

    logging.info('MAIN\t: before running thread')

    t.start()

    # Despite start() not finishing, the main program will continue to run
    logging.info('MAIN\t: wait for the thread to finish')

    # join() to wait for thread to complete before proceeding
    #t.join()
    logging.info('MAIN\t: all done')
```

**Output**:
```shell
15:21:13: MAIN  : before creating thread
15:21:13: MAIN  : before running thread
15:21:13: Thread 1: starting
15:21:13: MAIN  : wait for the thread to finish
15:21:13: MAIN  : all done
15:21:16: Thread 1: finishing
```

Notice `Thread 1` is running on it's own thread and finishes even after the main program exits. `Thread 1` is not a daemon thread, meaning the main program does not have to wait for it to finish in order for itself to complete.

## Daemon Threads
Daemon threads will shut down immediately when the main program completes. If threads are running that are not daemon, the main program will wait for those threads to complete before exiting. However, uncompleted threads that *are* daemons will be terminated once the main program exits.

When a python program exits, part of the shutdown process is cleaning up threading routines. `threading._shutdown()` iterates through all running threads and calls `.join()` on each that do not have a daemon flag set as True. 

**Example**: Run the program again, this time as a daemon thread:
```python
# Daemon threads shut down immediately when the main program exits
t = threading.Thread(target=some_function, args=(1,), daemon=True)
```

**Output**: `Thread 1` is terminated once the main program completes.
```shell
19:34:18: MAIN  : before creating thread
19:34:18: MAIN  : before running thread
19:34:18: Thread 1: starting
19:34:18: MAIN  : wait for the thread to finish
19:34:18: MAIN  : all done
```

## Joining Threads
Joining threads will ensure the program to wait for the joined thread(s) to finish before proceeding.

Uncomment `t.join()` to join the thread and run the program again:

**Example**: Utilize `join()` to wait for the thread to complete before proceeding.
``` python
t.join()
```

**Output**: Main program waits for the joined thread to finish before continuing.
```shell
19:34:18: MAIN  : before creating thread
19:34:18: MAIN  : before running thread
19:34:18: Thread 1: starting
19:34:18: MAIN  : wait for the thread to finish
19:34:21: Thread 1: finishing
19:34:21: MAIN  : all done
```

# Multiple Threads

**Example**: Run multiple threads.
```python
import logging
import threading
import time

def some_function(name: str):
    """ Arbitrary example function to pass into a thread. Will sleep for 3 seconds.

    Keyword arguments:
    name (str) - name of thread function is passed to
    """
    logging.info(f'Thread {name}: starting')
    time.sleep(3)
    logging.info(f'Thread {name}: finishing')

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO, datefmt="%H:%M:%S")
    start = time.time()
    use_join = False  
    thread_list = []

    logging.info('MAIN\t: before creating multi-threads')
    for i in range(5):
        t = threading.Thread(target=some_function, name=f'multi-thread-{i}', args=(i,))
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
```

**Output**: Notice since the threads are not set as daemon and they are not joined, the main program does not wait for them before proceeding.
```shell
18:27:17: MAIN  : before creating multi-threads
18:27:17: Thread 0: starting
18:27:17: Thread 1: starting
18:27:17: Thread 2: starting
18:27:17: Thread 3: starting
18:27:17: Thread 4: starting
18:27:17: MAIN  : wait for multi-threads to finish
18:27:17: MAIN  : all done (0.0015888214111328125 seconds taken)
18:27:20: Thread 0: finishing
18:27:20: Thread 1: finishing
18:27:20: Thread 3: finishing
18:27:20: Thread 4: finishing
18:27:20: Thread 2: finishing
```

**Example**: Run the same multi-thread program, but this time set the threads as daemon. From within the for loop, update the line:
```python
t = threading.Thread(target=some_function, name=f'multi-thread-{i}', args=(i,), daemon=True)
```

**Output**: Notice the daemon threads are terminated and do not finish executing once the main program completes.
```shell
18:30:38: MAIN  : before creating multi-threads
18:30:38: Thread 0: starting
18:30:38: Thread 1: starting
18:30:38: Thread 2: starting
18:30:38: Thread 3: starting
18:30:38: Thread 4: starting
18:30:38: MAIN  : wait for multi-threads to finish
18:30:38: MAIN  : all done (0.001123189926147461 seconds taken)
```

**Example**: Set the `use_join` flag to `True`, enabling the block of code that joins the threads.
```python
use_join = True
```

**Output**: Now regardless of the fact that these may be daemon threads, the Main program is blocked from exiting until each thread is finished.
```shell
18:31:01: Thread 0: starting
18:31:01: Thread 1: starting
18:31:01: Thread 2: starting
18:31:01: Thread 3: starting
18:31:01: Thread 4: starting
18:31:01: MAIN  : wait for multi-threads to finish
18:31:01: Main    : before joining thread 0.
18:31:04: Thread 0: finishing
18:31:04: Thread 1: finishing
18:31:04: Main    : thread 0 done
18:31:04: Main    : before joining thread 1.
18:31:04: Main    : thread 1 done
18:31:04: Main    : before joining thread 2.
18:31:04: Thread 2: finishing
18:31:04: Thread 3: finishing
18:31:04: Main    : thread 2 done
18:31:04: Main    : before joining thread 3.
18:31:04: Main    : thread 3 done
18:31:04: Main    : before joining thread 4.
18:31:04: Thread 4: finishing
18:31:04: Main    : thread 4 done
18:31:04: MAIN  : all done (3.0071310997009277 seconds taken)
```