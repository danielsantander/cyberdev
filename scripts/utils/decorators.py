#!/usr/bin/python3

import logging

_LOGGER = logging.getLogger(__name__)

def timing_decorator(func):
    import time
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        name = func.__name__
        name += f"({', '.join([x for x in args])})" if args else "()"
        _LOGGER.debug(f"[TIMER] {name} executed in {end_time - start_time:.2f} seconds")
        return result
    return wrapper
