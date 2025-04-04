#!/usr/bin/env python
#!/usr/bin/python3

import datetime
import logging
import re
import requests
import sys
import unittest
from unittest import mock
from unittest.mock import MagicMock, patch
from requests import Session
from test_template import TestTemplate, clean_dir, write_json_to_file, API_DIR

sys.path.insert(0, API_DIR)
from reddit import RedditAPI

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

MOCK_POST = {
    "kind": "t3",
    "data": {
        "subreddit": "MortalKombat",
        "title": "FATALITY",
        "subreddit_name_prefixed": "r/MortalKombat",
        "name": "t3_1jctblb",
        "created": 1742152810.0,
        "id": "1jctblb",
        "created_utc": 1742152810.0,
        "media": {},
        "is_video": True
    }
}

MOCK_SAVED_DATA_RAW_RESP = {
    "kind": "Listing",
    "data": {
        "after": "t3_1i5tplv",
        "dist": 25,
        "modhash": None,
        "geo_filter": "",
        "children": [MOCK_POST],
        "before": None
    }
}

class MockResponse:
    def __init__(self, json_data={}, status_code=200, url=""):
        self.json_data = json_data
        self.status_code = status_code
        self.ok:bool = int(self.status_code) in [200, 201]
        self.url = url

    def json(self):
        return self.json_data

    def raise_for_status(self, status=None):
        do_raise = True if self.ok is False or status not in [None, False] else False
        if do_raise: raise requests.exceptions.HTTPError("{0} Client Error".format(self.status_code))
        return do_raise

def mocked_requests_post(*args, **kwargs):
    # print(f"\n\nINSIDE mocked_requests_post -- args:{args};kwargs:{kwargs}")
    if 'api/unsave' in args[0]:
        return MockResponse(json_data={}, status_code=201)
    print(f"UNKNOWN URL: {args[0]}")
    return MockResponse(json_data={"ERROR": "UNKNOWN"}, status_code=429)

def mocked_requests_get(*args, **kwargs):
    # print(f"\n\nINSIDE mocked_requests_get -- args:{args};kwargs:{kwargs}")
    if search_results := re.search('^.*user\/(?P<username>[^\/]+)\/saved\/?$',args[0]):
        url = search_results.group()
        username = search_results.group(1)
        params = kwargs.get('params', {})
        # prevent infinite loop when iterating through paginated API calls
        if params.get('after') is not None:
            update_resp = MOCK_SAVED_DATA_RAW_RESP.copy()
            update_resp['data']['after']=None
            return MockResponse(json_data=update_resp)
        return MockResponse(json_data=MOCK_SAVED_DATA_RAW_RESP)

    print(f"UNKNOWN URL: {args[0]}")
    return MockResponse(status_code=400)

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
        results_file = api_data_dir / '20250101010101--results.json'
        post_list = [f"username{num}_20250101010101_sub{num}_t3_1randm{num}.jpeg" for num in range(0,5)]
        data = {
            "extracted": post_list[:2],
            "already_exists": [post_list[2]],
            "excluded": post_list[3:]
        }
        write_json_to_file(filename=results_file, data=data)
        results_file_2 = api_data_dir / '00-EXCLUDE_FILES.json'
        data_2 = [f"username{num}_20250101010101_sub{num}_t3_1randm{num}.jpeg" for num in range(5,10)]
        write_json_to_file(filename=results_file_2, data=data_2)
        files_to_exclude = self.reddit.get_files_to_exclude()

        self.assertTrue(api_data_dir.exists() and api_data_dir.is_dir())
        self.assertTrue(results_file.exists() and results_file.is_file())
        self.assertNotEqual(len(files_to_exclude), 0)
        for post in post_list + data_2:
            search = re.search('.*(t\d_[\w\d]*)\.jpeg', post)
            self.assertIsNotNone(search)
            post_id = search.group(1)
            self.assertIn(post, files_to_exclude)
            self.assertIn(post_id, files_to_exclude)
        self.assertEqual(len(post_list + data_2), len(files_to_exclude)/2)

    @mock.patch('requests.Session.get', side_effect=mocked_requests_get)
    def test_get_saved_data(self, mock_get):
        """ Test retrieving user's saved post data via API. """
        raw_data = self.reddit.get_saved_data(raw=True)
        self.assertEqual(raw_data.get('kind'), MOCK_SAVED_DATA_RAW_RESP.get('kind'))
        self.assertEqual(len(raw_data['data'].get('children', [])), len(MOCK_SAVED_DATA_RAW_RESP['data'].get('children', [])))

        saved_data = self.reddit.get_saved_data(max_count=len(MOCK_SAVED_DATA_RAW_RESP['data'].get('children', [])))
        self.assertIsNotNone(saved_data)
        self.assertEqual(len(saved_data), len(MOCK_SAVED_DATA_RAW_RESP['data'].get('children', [])))

    @mock.patch('requests.Session.post', side_effect=mocked_requests_post)
    def test_unsave_post(self, mock_post):
        resp = self.reddit.unsave_post(MOCK_POST)
        self.assertIsNotNone(resp)


    #TODO: write tests for other methods, such as:
    # - RedditAPI.consolidated_saved_files()
    # - RedditAPI.parse_filename()
    # - RedditAPI.process_saved_data()
    # - RedditAPI.retrieve_last_saved()
    # - RedditAPI.sanitize()

if __name__ == '__main__':
    unittest.main()
