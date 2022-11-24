#!/usr/bin/python3
'''
Unit testing for constants.

RUN TESTS:
$ python -m unittest python/scripts/tests/test_constants.py --verbose

RUN TESTS WITH COVERAGE:
$ python -m coverage run --source="." -m unittest python/scripts/tests/test_constants.py --verbose
$ coverage report
$ coverage annotate -d coverage_files
'''
import datetime
import unittest
import os
import re
import sys
from pathlib import Path

CURRENT_DIR_NAME = os.path.dirname(os.path.realpath(__file__))
CURRENT_DIR_PATH = Path(CURRENT_DIR_NAME)
PARENT_DIR_NAME = os.path.dirname(CURRENT_DIR_NAME)
# UTILS_DIR = Path(PARENT_DIR_NAME) / 'utils'

sys.path.insert(0, PARENT_DIR_NAME)
from utils import constants



class TestDefaultDatetimeFormat(unittest.TestCase):
    def setUp(self) -> None:
        self.now = datetime.datetime.utcnow()

    def test_default_datetime_format(self):
        pattern = re.compile("^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.?\d*$")    # 2022-11-16 03:13:53.434047
        isMatch = pattern.match(self.now.__str__())
        self.assertTrue(isMatch is not None)

        # convert into default datetime format (YYYYMMDDHHMMSS)
        now_str = self.now.strftime(constants.DEFAULT_DATETIME_FMT)             # 20221116031656
        pattern = re.compile("^\d{14}$")
        isMatch = pattern.match(now_str)
        self.assertTrue(isMatch is not None)

    def tearDown(self) -> None:
        return super().tearDown()


if __name__ == '__main__': unittest.main()