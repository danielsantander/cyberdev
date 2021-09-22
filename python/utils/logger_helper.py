
import errno
import logging
import logging.handlers
import os
from typing import Optional
from settings import DEBUG_MODE

CUR_DIR = os.path.abspath(os.path.dirname(__file__))        # python/utils/
LOG_DIR = os.path.join(CUR_DIR, "logs", "")                 # python/utils/logs/
LOG_LEVEL = logging.DEBUG if DEBUG_MODE else logging.INFO
LOG_FORMAT = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')


def create_console_logger(name:Optional[str]=None, level:int=LOG_LEVEL) -> logging.Logger:
    """
    Create and return a custom console handler logger.
    """
    logger = logging.getLogger(name)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(LOG_FORMAT)
    logger.addHandler(console_handler)
    logger.setLevel(level)
    return logger


def create_logger(name:str, level:int=LOG_LEVEL, log_dir:str=LOG_DIR, max_size:int=10*1024*1024, backup_count:int=5):
    """
    Create and return a logger with a StreamHandler and a RotatingFileHandler added.
    Creates log directory if one does not exist, and intializes a "master_logger" log file.
        INPUTS:
            name (str):         name of logger
            level (bool):       log level value
            max_size (int):     max number of bytes bytes for log file before file rotation begins (Default ~10mb)
            backup_count (int): number of backup files to keep in rotation. (Default 5) 
        OUTPUT: returns RotatingFileHandler logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    create_dir(LOG_DIR)

    # Master logger (holds all logs)
    master_location = os.path.join(LOG_DIR, "master_logger.log")
    #max_size_50 = 50*1024*1024 # ~52mb
    master_file_handler = logging.handlers.RotatingFileHandler(master_location, maxBytes=max_size, backupCount=backup_count)
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


def create_dir(dir_path:str):
    """
    Create a directory if one does not exist for the given directory path.
    """
    try:
        os.makedirs(dir_path)
    except OSError as err:
        if err.errno == errno.EEXIST and os.path.isdir(dir_path):
            pass    # Directory still created
        else:
            raise   # Error creating directory
    return


if __name__ == '__main__':

    # Test Logger:
    logger = create_logger("test_logger", level=logging.INFO)
    logger.info("This is a test.")
    logger.debug("This is a debugging test -- only master_logger should see this.")

    logger2 = create_logger("test_logger2", level=logging.DEBUG)
    logger2.info("This is a test2.")
    logger2.debug("This is a debugging test2 -- all loggers should see this.")
