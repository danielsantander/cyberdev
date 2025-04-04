#!/usr/bin/env python
#!/usr/bin/python3

import datetime
import logging
import re
import sys
import unittest
from unittest.mock import MagicMock, patch
from requests import Session
from test_template import TestTemplate, clean_dir, write_json_to_file, API_DIR

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

    def test_get_files_to_exclude(self):
        api_data_dir = self.test_dir / 'reddit' / f'{self.reddit.username}' / 'api_data'
        clean_dir(api_data_dir)
        api_data_dir.mkdir(parents=True, exist_ok=True)

        results_file = api_data_dir / '20250101010101--results.json'
        post_list = [f"username{num}_20250101010101_sub{num}_t3_1randm{num}.jpeg" for num in range(0,5)]
        data = {
            "extracted": post_list[:2],
            "already_exists": [post_list[2]],
            "excluded": post_list[3:]
        }
        write_json_to_file(filename=results_file, data=data)
        files_to_exclude = self.reddit.get_files_to_exclude()

        self.assertTrue(api_data_dir.exists() and api_data_dir.is_dir())
        self.assertTrue(results_file.exists() and results_file.is_file())
        self.assertNotEqual(len(files_to_exclude), 0)
        for post in post_list:
            search = re.search('.*(t\d_[\w\d]*)\.jpeg', post)
            self.assertIsNotNone(search)
            post_id = search.group(1)
            self.assertIn(post, files_to_exclude)
            self.assertIn(post_id, files_to_exclude)
        self.assertEqual(len(post_list), len(files_to_exclude)/2)

    #TODO: write tests for other methods, such as:
    # - RedditAPI.get_saved_data()
    # - RedditAPI.unsave_post()
    # - RedditAPI.consolidated_saved_files()
    # - RedditAPI.parse_filename()
    # - RedditAPI.process_saved_data()
    # - RedditAPI.retrieve_last_saved()
    # - RedditAPI.sanitize()

if __name__ == '__main__':
    unittest.main()
