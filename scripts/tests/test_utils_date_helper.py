#!/usr/bin/env python
#!/usr/bin/python3

import unittest
import re
import sys
from test_template import SCRIPTS_DIR, TestTemplate

sys.path.insert(0, SCRIPTS_DIR)
from utils import date_helper
from utils import constants

class TestDateHelper(TestTemplate):
    def setUp(self):
        super().setUp()
        self.now_timestamp = self._now.timestamp()
        self.now_str = self._now.strftime(constants.DEFAULT_DATETIME_FMT_LONG)

    def test_timestamp_to_str(self):
        results = date_helper.timestamp_to_date_string(self.now_timestamp)  # YYYYMMDDHHMMSS
        format_regex = re.compile(r'^\d{4}\d{2}\d{2}\d{2}\d{2}\d{2}$')
        self.assertTrue(isinstance(results, str))
        self.assertEqual(results, self.now_str)
        self.assertTrue(format_regex.match(results) is not None)

    def test_current_iso_time(self):
        results = date_helper.current_iso_time()    # 2022-01-17T04:15:20.696565+00:00
        self.assertTrue(isinstance(results, str))
        format_regex = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d*\+\d{2}:\d{2}$')
        self.assertTrue(format_regex.match(results) is not None)

    def tearDown(self):
        return super().tearDown()

if __name__ == '__main__': unittest.main()