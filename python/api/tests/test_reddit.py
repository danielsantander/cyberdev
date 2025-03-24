#!/usr/bin/env python
#!/usr/bin/python3

import datetime
import logging
import sys
import unittest
from unittest.mock import MagicMock, patch
from requests import Session
from test_template import TestTemplate, clean_dir, API_DIR

sys.path.insert(0, API_DIR)
from reddit import RedditAPI

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class TestRedditAPI(TestTemplate):
    @patch.object(Session, 'post')
    def setUp(self, mock_post)->None:
        self.now = datetime.datetime.utcnow()
        self.test_dir = self._test_dir / 'TestRedditAPI'
        self.token_data = mock_resp_data = { "access_token": "TOKEN", "token_type": "bearer", "expires_in": 86400, "scope": "*" }
        params = {
            # RedditAPI args
            "client_id": "1234567890",
            "client_secret": "shh!",
            "username": "Batman",
            "password": "password123!",
            # APIBase args:
            "logger": logger,
            "save_dir": self.test_dir,
            "use_verbose": True,
        }
        self.reddit = RedditAPI(**params)

        # mock api token validation
        mock_resp = MagicMock()
        mock_resp.json.return_value = self.token_data
        mock_resp.status_code.return_value = 201
        mock_resp.url.return_value = 'test.com'
        mock_resp.raise_for_status.return_value = None
        mock_post.return_value = mock_resp
        self.reddit.update_token()

    def tearDown(self) -> None:
        if self.test_dir.exists() and self.test_dir.is_dir():
            clean_dir(self.test_dir)

    def test_token(self):
        self.assertTrue(self.reddit.token.is_valid)
        expected_expire_date = self.now + datetime.timedelta(seconds=self.token_data.get('expires_in'))
        self.assertTrue(self.reddit.token.is_valid)
        self.assertEqual(self.reddit.token.access_token, self.token_data.get('access_token'))
        self.assertGreaterEqual(self.reddit.token.expire_date.replace(microsecond=0), expected_expire_date.replace(microsecond=0))

    @patch.object(Session, 'get')
    def test_send_request(self, mock_get):
        test_url = 'https://www.somefakeurl.com/api/v1/test'
        test_resp = {"KeyOne": "ValueOne", "KeyTwo": "ValueTwo"}
        mock_resp = MagicMock()
        mock_resp.json.return_value = test_resp
        mock_resp.status_code.return_value = 200
        mock_resp.raise_for_status.return_value = None
        mock_resp.url.return_value = test_url
        mock_get.return_value = mock_resp
        data = self.reddit.send_request(url=test_url, method='GET')
        self.assertDictEqual(test_resp, data)

    #TODO: write tests for other methods, such as:
    # - RedditAPI.get_files_to_exclude()
    # - RedditAPI.get_saved_data()
    # - RedditAPI.unsave_post()
    # - RedditAPI.consolidated_saved_files()
    # - RedditAPI.parse_filename()
    # - RedditAPI.process_saved_data()
    # - RedditAPI.retrieve_last_saved()
    # - RedditAPI.sanitize()

if __name__ == '__main__':
    unittest.main()
