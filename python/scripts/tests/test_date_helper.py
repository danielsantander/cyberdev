#!/usr/bin/python3
'''
Unit testing for date helper.

RUN:
$ python3 -m coverage run --source="." -m unittest python/scripts/tests/test_date_helper.py --verbose
$ coverage report
$ coverage annotate -d coverage_files/
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
from utils import date_helper

class TestDateHelper(unittest.TestCase):
    def setUp(self) -> None:
        self.now = datetime.datetime.utcnow()
        self.now_timestamp = self.now.timestamp()
        self.str_format = '%Y%m%d%H%M%S'
        self.now_str = self.now.strftime(self.str_format)

    def test_timestamp_to_str(self):
        results = date_helper.timestamp_to_date_string(self.now_timestamp)  # 20220117041520
        format_regex = re.compile(r'^\d{4}\d{2}\d{2}\d{2}\d{2}\d{2}$') # YYYYMMDDHHMMSS
        self.assertTrue(isinstance(results, str))
        self.assertEqual(results, self.now_str)
        self.assertTrue(format_regex.match(results) is not None)

    def test_current_iso_time(self):
        results = date_helper.current_iso_time()    # 2022-01-17T04:15:20.696565+00:00
        self.assertTrue(isinstance(results, str))
        format_regex = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d*\+\d{2}:\d{2}$')
        self.assertTrue(format_regex.match(results) is not None)

if __name__ == '__main__': unittest.main()