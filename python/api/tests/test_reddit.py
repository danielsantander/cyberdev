#!/usr/bin/env python
#!/usr/bin/python3

import datetime
import logging
import re
import requests
import os
import sys
import unittest
from unittest import mock
from unittest.mock import MagicMock, patch
from pathlib import Path
from requests import Session
from test_template import TestTemplate, clean_dir, write_json_to_file, API_DIR

sys.path.insert(0, API_DIR)
from reddit import RedditAPI

PY_DIR = os.path.dirname(API_DIR)
SCRIPT_DIR = os.path.join(PY_DIR, 'scripts')
sys.path.insert(0, SCRIPT_DIR)
from utils import webutils
from utils.date_helper import timestamp_to_date_string
from utils.constants import DEFAULT_DATETIME_FMT_LONG

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

MOCK_POST = {
    "kind": "t3",
    "data": {
        "author": "Username123",
        "subreddit": "pics",
        "name": "t3_1fd79on",
        "created_utc": 1725934894.0,
        "post_hint": "image",
        "url_overridden_by_dest": "https://i.redd.it/9xrd20j56wnd1.png",
        "url": "https://i.redd.it/9xrd20j56wnd1.png",
        "domain": "i.redd.it",
        "media": None,
        "secure_media": None,
        "is_video": False,
        "over_18": False,

        "created": 1725934894.0,
        "title": "Empire State Building lit up with Darth Vader's colors on March 21, 2024. For James Earl Jones.",
        "upvote_ratio": 0.97,
        "ups": 126512,
        "score": 126512,
        "subreddit_id": "t5_2qh0u",
        "id": "1fd79on",
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

    def iter_content(self, chunk_size=256):
        """
        Used for extracting media from url.
        """
        return iter(()) # empty_iterator

def mocked_requests_post(*args, **kwargs):
    # print(f"\n\nINSIDE mocked_requests_post -- args:{args};kwargs:{kwargs}")
    url = args[0] if len(args) else kwargs.get('url')

    if 'api/unsave' in url:
        return MockResponse(json_data={}, status_code=201)
    print(f"UNKNOWN URL: {url}")
    return MockResponse(json_data={"ERROR": "UNKNOWN"}, status_code=429)

def mocked_requests_get(*args, **kwargs):
    # print(f"\n\nINSIDE mocked_requests_get -- args:{args};kwargs:{kwargs}")
    url = args[0] if len(args) else kwargs.get('url')
    approved_media_content_type_list = ["image/jpeg","video/mp4"]
    content_type = kwargs.get('Content-type')

    if search_results := re.search('^.*user\/(?P<username>[^\/]+)\/saved\/?$',url):
        url = search_results.group()
        username = search_results.groupdict('username')
        params = kwargs.get('params', {})

        # prevent infinite loop when iterating through paginated API calls
        if params.get('after') is not None:
            update_resp = MOCK_SAVED_DATA_RAW_RESP.copy()
            update_resp['data']['after']=None
            return MockResponse(json_data=update_resp)

        return MockResponse(json_data=MOCK_SAVED_DATA_RAW_RESP)

    # extract_media_from_url call
    elif search_results := re.search('^.*test_process_saved_data\.(?P<extension>.*)$',url) or content_type in approved_media_content_type_list:
        extension = search_results.groupdict().get('extension')
        return MockResponse(json_data={})

    print(f"UNKNOWN URL: {url}")
    return MockResponse(status_code=400)


class TestRedditAPI(TestTemplate):
    @patch.object(Session, 'post')
    def setUp(self, mock_post)->None:
        self.now = datetime.datetime.now(datetime.timezone.utc)
        self.test_dir = self._test_dir / 'TestRedditAPI'
        self.token_data = mock_resp_data = { "access_token": "TOKEN", "token_type": "bearer", "expires_in": 86400, "scope": "*" }
        params = {
            # RedditAPI args
            "client_id": "1234567890",
            "client_secret": "shh!",
            "username": "Batman",
            "password": "password123!",
            # APIBase args:
            # "logger": logger,
            "save_dir": self.test_dir,  # ensure in test_dir so tearDown removes any created data
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
        self.assertGreaterEqual(self.reddit.token.expire_date.replace(second=0,microsecond=0).timestamp(), expected_expire_date.replace(second=0,microsecond=0).timestamp())

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

    def test_consolidate_saved_files(self):
        api_data_dir = self.reddit.api_data_dir_path
        now = datetime.datetime.now(datetime.timezone.utc).strftime(DEFAULT_DATETIME_FMT_LONG)
        saved_data_files = [api_data_dir / f'{now[:-1]}{x}--saved_data.json' for x in range(0,5)]
        for f in saved_data_files:
            write_json_to_file(f, [MOCK_POST])
        resp = self.reddit.consolidated_saved_files()
        for f in saved_data_files: f.unlink()
        self.assertEqual(len(list(self.reddit.api_data_dir_path.iterdir())), 1)
        consolidated_file = [f for f in self.reddit.api_data_dir_path.iterdir()][0]
        search = re.search('^\d{14}--consolidated_saved_data.json$', consolidated_file.name)
        self.assertIsNotNone(search)
        self.assertEqual(search.group(), consolidated_file.name)

    def test_parse_filename(self):
        now = datetime.datetime.now(datetime.timezone.utc).strftime(DEFAULT_DATETIME_FMT_LONG)
        subreddit = "DogSubreddit"
        post_kind = "t3"
        post_id = "1randm1"
        extension = "jpeg"
        post_filename = f"{self.reddit.username}_{now}_{subreddit}_{post_kind}_{post_id}.{extension}"
        results = self.reddit.parse_filename(post_filename)
        expected_results = {
            'groups': (self.reddit.username, str(now), subreddit, post_kind, post_id, extension),
            'filename': post_filename,
            'username': self.reddit.username,
            'date': str(now),
            'subreddit': subreddit,
            'post_kind': post_kind,
            'post_id': post_id,
            'extension': extension
        }
        for k,v in expected_results.items():
            self.assertEqual(results[k], expected_results[k])

    @mock.patch('requests.Session.get', side_effect=mocked_requests_get)
    @mock.patch('requests.Session.post', side_effect=mocked_requests_post)
    def test_process_saved_data(self, mock_get, mock_post):
        post = MOCK_POST.copy()

        # save file so file already exists upon processing
        post_date_created_timestamp = int(MOCK_POST['data']['created_utc'])
        post_date_created_str = timestamp_to_date_string(post_date_created_timestamp)
        extension = "png"
        filename = f"{MOCK_POST['data']['author']}_{post_date_created_str}_{MOCK_POST['data']['subreddit']}_{MOCK_POST['data']['name']}.{extension}"
        filepath: Path = self.reddit.save_dir_path / 'subreddits' / MOCK_POST['data']['subreddit'] / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.touch()

        # image post -- already exists
        post['data'].update({"post_hint": "image", "url": "https://i.redd.it/test_process_saved_data.png"})
        results = self.reddit.process_saved_data([post])
        parsed_filename = self.reddit.parse_filename(results['already_exists'][0])
        self.assertEqual(parsed_filename.get('username'), MOCK_POST['data']['author'])
        self.assertEqual(parsed_filename.get('subreddit'), MOCK_POST['data']['subreddit'])
        self.assertEqual(parsed_filename.get('post_kind'), MOCK_POST['kind'])
        self.assertEqual(parsed_filename.get('post_id'), MOCK_POST['data']['id'])
        self.assertEqual(len(results['already_exists']), 1)
        self.assertEqual(len(results['already_exists']), results['already_exists_count'])

        # image post -- file in exclude_files list
        post['data'].update({"post_hint": "image", "url": "https://i.redd.it/test_process_saved_data.png"})
        results = self.reddit.process_saved_data([post], exclude_files=[filename])
        parsed_filename = self.reddit.parse_filename(results['excluded'][0])
        self.assertEqual(parsed_filename.get('username'), MOCK_POST['data']['author'])
        self.assertEqual(parsed_filename.get('subreddit'), MOCK_POST['data']['subreddit'])
        self.assertEqual(parsed_filename.get('post_kind'), MOCK_POST['kind'])
        self.assertEqual(parsed_filename.get('post_id'), MOCK_POST['data']['id'])
        self.assertEqual(len(results['excluded']), 1)
        self.assertEqual(len(results['excluded']), results['excluded_count'])

        # video post
        post['data'].update({"post_hint": "video", "url": "https://i.redd.it/test_process_saved_data.mp4", "is_video": True})
        results = self.reddit.process_saved_data([post])

        # case: already exists/extracted & do purge
        post['data'].update({"post_hint": "image", "url": "https://i.redd.it/test_process_saved_data.png"})
        results = self.reddit.process_saved_data([post], do_purge=True)     # already_exists
        parsed_filename = self.reddit.parse_filename(results['already_exists'][0])
        self.assertEqual(parsed_filename.get('username'), MOCK_POST['data']['author'])
        self.assertEqual(parsed_filename.get('subreddit'), MOCK_POST['data']['subreddit'])
        self.assertEqual(parsed_filename.get('post_kind'), MOCK_POST['kind'])
        self.assertEqual(parsed_filename.get('post_id'), MOCK_POST['data']['id'])
        self.assertEqual(len(results['already_exists']), 1)
        self.assertEqual(len(results['already_exists']), results['already_exists_count'])

    def test_retrieve_last_saved(self):
        now = datetime.datetime.now(datetime.timezone.utc)

        # last saved file is None
        results = self.reddit.retrieve_last_saved()
        self.assertEqual(len(results), 0)

        # creation date differs
        for idx in range(0,5):
            file_path = self.reddit.api_data_dir_path / f"{now.replace(hour=idx, minute=0, second=0, microsecond=0).strftime(DEFAULT_DATETIME_FMT_LONG)}--saved_data.json"
            write_json_to_file(filename=file_path, data={})
        results = self.reddit.retrieve_last_saved()
        self.assertIsNotNone(results)

        # base case
        now_str = now.strftime(DEFAULT_DATETIME_FMT_LONG)
        file_path = self.reddit.api_data_dir_path / f"{now_str}--saved_data.json" # YYYYMMDDSSSSSS--saved_data.json
        data = [MOCK_POST]
        write_json_to_file(filename=file_path, data=data)
        results = self.reddit.retrieve_last_saved()
        self.assertEqual(len(data), len(results))
        self.assertEqual(data[0]['data']['id'], results[0]['data']['id'])

    def test_sanitize(self):
        """
        Tests sanitizing directories based on blacklisted.
        Moves:
            - reddit/Batman/subreddits/blacklist/Username123_20240909212134_blacklist_t3_1fd79on.png
        To:
            - reddit/Batman/nsfw/Username123/Username123_20240909212134_blacklist_t3_1fd79on.png
        """

        # no directory -- empty results
        results = self.reddit.sanitize(subreddit_blacklist=[])
        self.assertIsInstance(results, dict)
        for k,v in results.items():
            self.assertIsInstance(v, list)
            self.assertEqual(len(v), 0)

        # pass in blacklist
        post = MOCK_POST.copy()
        post['data']['subreddit'] = 'blacklist'
        post_date_created_str = timestamp_to_date_string(int(post['data']['created_utc']))
        fname = f"{post['data']['author']}_{post_date_created_str}_{post['data']['subreddit']}_{post['data']['name']}.png"
        file_path: Path = self.reddit.save_dir_path / 'subreddits' / post['data']['subreddit'] / fname
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch()

        results = self.reddit.sanitize(subreddit_blacklist=['blacklist'])
        self.assertIsInstance(results, dict)
        for k,v in results.items():
            expected_count = 1 if k == 'posts_moved' else 0
            self.assertIsInstance(v, list)
            self.assertEqual(len(v), expected_count)
        moved_file_path = self.reddit.save_dir_path / 'nsfw' / post['data']['author'] / fname
        self.assertFalse(file_path.exists() and file_path.is_file())    # ensure file moved no longer exists in old path
        self.assertFalse(file_path.parent.exists())                     # ensure empty directory is removed
        self.assertTrue(moved_file_path.parent.exists())                # ensure parent directory of new file path exists
        self.assertTrue(moved_file_path.parent.is_dir())
        self.assertTrue(moved_file_path.exists())
        self.assertTrue(moved_file_path.is_file())

        # case -- already exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch()
        self.assertTrue(file_path.exists() and file_path.is_file())
        self.assertTrue(moved_file_path.exists())
        results = self.reddit.sanitize(subreddit_blacklist=['blacklist'])
        self.assertIsInstance(results, dict)
        for k,v in results.items():
            expected_count = 1 if k == 'already_exists' else 0
            self.assertIsInstance(v, list)
            self.assertEqual(len(v), expected_count)


if __name__ == '__main__':
    unittest.main()
