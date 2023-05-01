#!/usr/bin/python3

""" Create custom console and rotating file handler loggers. """
import errno
import logging
import logging.handlers
import os
from typing import Optional, Union
from pathlib import Path
from utils import navigation

DEBUG_MODE: bool = True
CUR_DIR = os.path.abspath(os.path.dirname(__file__)) # utils/
# LOG_DIR = os.path.join(CUR_DIR, "logs", "") # utils/logs/
LOG_DIR = Path(CUR_DIR) / 'logs'    # utils/logs
LOG_LEVEL: int = logging.DEBUG if DEBUG_MODE else logging.INFO
LOG_FORMAT = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')


def create_console_logger(name:Optional[str]=None, level:int=LOG_LEVEL, format=LOG_FORMAT) -> logging.Logger:
    """
    Return a custom logger with stream (console) handler.
    """
    logger = logging.getLogger(name)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(format)
    logger.addHandler(console_handler)
    logger.setLevel(level)
    return logger

def create_logger(name:str, level:int=LOG_LEVEL, log_dir:Union[str,Path]=LOG_DIR, max_byte_size:int=10*1024*1024, backup_count:int=5) -> logging.Logger:
    """
    Return logger with Stream and RotatingFile handlers.
    Creates log directory if one does not exist, and initializes a master_logger file.

    Keyword arguments:
    name -- name of logger
    level -- logger level value defaults to logging.DEBUG (default 10)
    max_byte_size  -- max number of bytes for size of log file, defaults to 10 mb (default 10*1024*1024)
    backup_count -- number of backup files to keep in rotation (default 5)
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    log_dir = log_dir if isinstance(log_dir, Path) else Path(log_dir)
    log_dir = navigation.make_directory(log_dir)

    # Master logger (holds all logs)
    master_location = os.path.join(log_dir, "master_logger.log")
    #max_byte_size_50 = 50*1024*1024 # ~52mb
    master_file_handler = logging.handlers.RotatingFileHandler(master_location, maxBytes=max_byte_size, backupCount=backup_count)
    master_file_handler.setLevel(logging.DEBUG)
    master_file_handler.setFormatter(LOG_FORMAT)

    # create console logger
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(LOG_FORMAT)

    # return loggers with both logging handlers
    logger.addHandler(console_handler)
    logger.addHandler(master_file_handler)
    return logger

# Testing purposes:
""" if __name__ == '__main__':

    # Test Logger:
    logger = create_logger("test_logger", level=logging.INFO)
    logger.info("This is a test.")
    logger.debug("This is a debugging test -- only master_logger should see this.")

    logger2 = create_logger("test_logger2", level=logging.DEBUG)
    logger2.info("This is a test2.")
    logger2.debug("This is a debugging test2 -- all loggers should see this.") """
