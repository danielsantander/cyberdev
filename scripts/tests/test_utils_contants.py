#!/usr/bin/env python
#!/usr/bin/python3

import datetime
import unittest
import os
import re
import sys
from pathlib import Path
from test_template import TestTemplate, SCRIPTS_DIR

sys.path.insert(0, SCRIPTS_DIR)
from utils import constants


class TestDefaultDatetimeFormat(TestTemplate):
    def setUp(self) -> None:
        super().setUp()
        self.now = datetime.datetime.utcnow()

    def test_default_directories(self):
        # default save directory
        default_save_dir_path = Path(constants.DEFAULT_SAVE_DIRECTORY)
        expected_save_dir_path = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) / 'data'
        self.assertEqual(default_save_dir_path.absolute(), expected_save_dir_path.absolute())

        # default api directory
        default_api_save_directory_path = Path(constants.DEFAULT_API_SAVE_DIRECTORY)
        expected_api_save_dir_path = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) / 'data' / 'api'
        self.assertEqual(default_api_save_directory_path.absolute(), expected_api_save_dir_path.absolute())


    def test_default_datetime_format(self):
        pattern = re.compile("^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.?\d*$")    # 2022-11-16 03:13:53.434047
        isMatch = pattern.match(self.now.__str__())
        self.assertTrue(isMatch is not None)

        # convert into default format short -- YYYYMMDD
        now_str = self.now.strftime(constants.DEFAULT_DATETIME_FMT_SHORT)
        pattern = re.compile("^\d{8}$")
        isMatch = pattern.match(now_str)
        self.assertTrue(isMatch is not None)

        # convert into default format long -- YYYYMMDDHHMMSS
        now_str = self.now.strftime(constants.DEFAULT_DATETIME_FMT_LONG)
        pattern = re.compile("^\d{14}$")
        isMatch = pattern.match(now_str)
        self.assertTrue(isMatch is not None)

        # convert into default format -- YYYYMMDDHHMMSS
        now_str = self.now.strftime(constants.DEFAULT_DATETIME_FMT)
        pattern = re.compile("^\d{14}$")
        isMatch = pattern.match(now_str)
        self.assertTrue(isMatch is not None)


    def tearDown(self) -> None:
        return super().tearDown()


if __name__ == '__main__': unittest.main()