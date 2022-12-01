#!/usr/bin/python3
'''
Unit testing for custom logging.

RUN:
$ python3 -m coverage run --source="." -m unittest python/scripts/tests/test_custom_logging.py --verbose
$ coverage report
$ coverage annotate -d coverage_files/
'''
import unittest
import os
import sys
import logging
from pathlib import Path

CURRENT_DIR_NAME = os.path.dirname(os.path.realpath(__file__))
CURRENT_DIR_PATH = Path(CURRENT_DIR_NAME)
PARENT_DIR_NAME = os.path.dirname(CURRENT_DIR_NAME)
# UTILS_DIR = Path(PARENT_DIR_NAME) / 'utils'

sys.path.insert(0, PARENT_DIR_NAME)
from utils import custom_logging
from utils.navigation import clean_directory

class TestCustomLogging(unittest.TestCase):
    def setUp(self) -> None:
        self.log_dir:Path = CURRENT_DIR_PATH / 'TestCustomLogging'
        if not self.log_dir.exists(): self.log_dir.mkdir()

        self.log_level:int = logging.DEBUG

    def test_console_logger(self):
        console_logger = custom_logging.create_console_logger(level=self.log_level)
        self.assertEqual(isinstance(console_logger, logging.Logger), True)
        self.assertEqual(console_logger.level, self.log_level)
        self.assertTrue(console_logger.hasHandlers())

    def test_creating_rotational_logger(self):
        master_logger_path:Path = self.log_dir / 'master_logger.log'
        self.assertFalse(master_logger_path.exists())

        logger =  custom_logging.create_logger(name='TestLogger', level=self.log_level, log_dir=self.log_dir)
        self.assertTrue(master_logger_path.exists())
        self.assertTrue(master_logger_path.is_file())
        self.assertEqual(isinstance(logger, logging.Logger), True)
        self.assertEqual(logger.level, self.log_level)
        self.assertTrue(logger.hasHandlers())

    def tearDown(self) -> None:
        # delete (unlink) any test files or directories
        if self.log_dir.exists() and self.log_dir.is_dir(): clean_directory(self.log_dir, remove_directory=True)

if __name__ == '__main__': unittest.main()