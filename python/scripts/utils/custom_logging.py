#!/usr/bin/python3

""" Create custom console and rotating file handler loggers. """
import logging
import logging.handlers
import os
from typing import Optional, Union
from pathlib import Path
from utils.constants import DEFAULT_LOG_FORMAT
from utils.navigation import make_directory

DEBUG_MODE: bool = True
LOG_LEVEL: int = logging.DEBUG if DEBUG_MODE else logging.INFO

def add_handler_to_logger(logger:logging.Logger, new_handler, log_level:int=logging.DEBUG, format:Union[str, logging.Formatter]=DEFAULT_LOG_FORMAT):
    log_format = logging.Formatter(format) if isinstance(format, str) else format
    new_handler.setLevel(log_level)
    new_handler.setFormatter(log_format)
    logger.addHandler(new_handler)
    return logger

def create_console_logger(name:Optional[str]=None, level:int=LOG_LEVEL, format:Union[str, logging.Formatter]=DEFAULT_LOG_FORMAT) -> logging.Logger:
    """
    Return a custom logger with stream (console) handler.
    """
    log_format = logging.Formatter(format) if isinstance(format, str) else format
    logger = logging.getLogger(name)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)
    logger.setLevel(level)
    return logger

def create_logger(name:str, level:int=LOG_LEVEL, log_dir:Union[str,Path]=None, max_byte_size:int=10*1024*1024, backup_count:int=5, format:Union[str, logging.Formatter]=DEFAULT_LOG_FORMAT) -> logging.Logger:
    """
    Return logger with Stream and RotatingFile handlers.
    Creates log directory if one does not exist, and initializes a master_logger file.

    Keyword arguments:
    name -- name of logger
    level -- logger level value defaults to logging.DEBUG (default 10)
    max_byte_size  -- max number of bytes for size of log file, defaults to 10 mb (default 10*1024*1024)
    backup_count -- number of backup files to keep in rotation (default 5)
    format -- logger format
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    log_format = logging.Formatter(format) if isinstance(format, str) else format
    if log_dir is not None:
        log_dir = log_dir if isinstance(log_dir, Path) else Path(log_dir)
        log_dir = make_directory(log_dir)

        # Master logger (holds all logs)
        master_location = os.path.join(log_dir, f"{name}.log")
        #max_byte_size_50 = 50*1024*1024 # ~52mb
        master_file_handler = logging.handlers.RotatingFileHandler(master_location, maxBytes=max_byte_size, backupCount=backup_count)
        master_file_handler.setLevel(logging.DEBUG)
        master_file_handler.setFormatter(log_format)
        logger.addHandler(master_file_handler)

    # create console logger
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    return logger

# Testing purposes:
"""
if __name__ == '__main__':

    # Test Logger:
    logger = create_logger("test_logger", level=logging.INFO)
    logger.info("This is a test.")
    logger.debug("This is a debugging test -- only master_logger should see this.")

    logger2 = create_logger("test_logger2", level=logging.DEBUG)
    logger2.info("This is a test2.")
    logger2.debug("This is a debugging test2 -- all loggers should see this.")
"""
