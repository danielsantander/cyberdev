#!/usr/bin/env python
#!/usr/bin/python3

import datetime
import sys
import unittest
from pathlib import Path
from test_template import TestTemplate, clean_dir, API_DIR
sys.path.insert(0, API_DIR)
from api import APIBase

class TestAPIBasic(TestTemplate):
    def setUp(self):
        self.test_dir = self._test_dir / 'TestAPIBasic'
        args = {
            "logger": None,
            "save_dir": self.test_dir,
            "use_verbose": True
        }
        self.api_base = APIBase(**args)
        return

    def tearDown(self):
        if self.test_dir.exists() and self.test_dir.is_dir():
            clean_dir(self.test_dir)
        return

    def test_save_dir(self):
        self.assertTrue(self.api_base._save_dir.exists())
        self.assertTrue(self.api_base._save_dir.is_dir())
        self.assertEqual(self.api_base._save_dir.name, self.test_dir.name)

    def test_vars(self):
        from logging import Logger, DEBUG, INFO
        from requests import Session
        self.assertIsInstance(self.api_base._save_dir, Path)
        # self.assertIsInstance(self.api_base._now, datetime.datetime)
        self.assertIsInstance(self.api_base._now_str_long, str)
        self.assertIsInstance(self.api_base._now_str_short, str)
        self.assertIsInstance(self.api_base._session, Session)
        self.assertIsInstance(self.api_base._use_verbose, bool)
        self.assertIsInstance(self.api_base._logger, Logger)
        log_level = DEBUG if self.api_base._use_verbose else INFO
        self.assertEqual(self.api_base._logger.level, log_level)

if __name__ == '__main__':
    unittest.main()
