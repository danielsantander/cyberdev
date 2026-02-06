#!/usr/bin/env python
#!/usr/bin/python3

import datetime
import requests
import sys
import unittest
from unittest import mock
from pathlib import Path
from test_template import TestTemplate, MockResponse, clean_dir, API_DIR

sys.path.insert(0, API_DIR)
from api import APIBase

def mocked_requests_get(*args, **kwargs):
    # print(f"\n\nINSIDE mocked_requests_get -- args:{args};kwargs:{kwargs}") # used for DEBUGGING
    url = args[0] if len(args) else kwargs.get('url')
    return MockResponse(json_data={}, status_code=200, url=url)

class TestAPIBasic(TestTemplate):

    def setUp(self):
        super().setUp()
        self.test_dir = self._test_dir / 'TestAPIBasic'
        args = {
            "logger": None,
            "save_dir_path": self.test_dir,
            # "use_verbose": True
            "use_verbose": False
        }
        self.api_base = APIBase(**args)

    def test_save_dir(self):
        self.assertTrue(self.api_base._save_dir_path.exists())
        self.assertTrue(self.api_base._save_dir_path.is_dir())
        self.assertEqual(self.api_base._save_dir_path.name, self.test_dir.name)

    def test_vars(self):
        from logging import Logger, DEBUG, INFO
        from requests import Session
        self.assertIsInstance(self.api_base._save_dir_path, Path)
        self.assertIsInstance(self.api_base._now, datetime.datetime)
        self.assertIsInstance(self.api_base._now_str_long, str)
        self.assertIsInstance(self.api_base._now_str_short, str)
        self.assertIsInstance(self.api_base._session, Session)
        self.assertIsInstance(self.api_base._use_verbose, bool)
        self.assertIsInstance(self.api_base._logger, Logger)
        log_level = DEBUG if self.api_base._use_verbose else INFO
        self.assertEqual(self.api_base._logger.level, log_level)

    @mock.patch('requests.Session.get', side_effect=mocked_requests_get)
    def test_send_request(self, mock_get):
        test_url:str = 'https://test.local/api/'
        expected_status_code = 200

        resp = self.api_base.send_request(url=test_url, method='GET')
        self.assertEqual(resp.status_code, expected_status_code)
        self.assertEqual(resp.url, test_url)
        return

    def tearDown(self) -> None:
        return super().tearDown()

if __name__ == '__main__':
    unittest.main()
