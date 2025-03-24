#!/usr/bin/env python
#!/usr/bin/python3

import argparse
import datetime
import logging
import json
import re
import requests
import os
import sys
from api import APIBase
from html import unescape
from pathlib import Path
from typing import Union

# TODO:
# - can probably improve get_files_to_exclude() method

# REG_EX:
RE_REDDIT_FILE_FORMAT = r'^(?P<username>.*)_(?P<date>\d{14})_(?P<subreddit>.*)_(?P<post_kind>.*)_(?P<post_id>.*).(?P<extension>\w{3})$'    # <username>_YYYYMMDDSSSSSS_<subreddit>_<post_kind>_<post_id>.<ext>
RE_OLD_REDDIT_SAVE_FILE_FORMAT = r'^(?P<username>.*)_saved_data_(?P<year>\d{4})(?P<month>\d{2})(?P<date>\d{1,2})(?P<seconds>\d*)(\.json)?' # username_saved_data_YYYYMMDDSS.json
RE_REDDIT_SAVE_FILE_FORMAT = r'^(?P<year>\d{4})(?P<month>\d{2})(?P<date>\d{1,2})(?P<seconds>\d*)?\-\-saved_data(\.json)?'                  # YYYYMMDDSSSSSS--saved_data.json
RE_RESULTS_FILE_FORMAT = r'^(?P<year>\d{4})(?P<month>\d{2})(?P<date>\d{1,2})(?P<seconds>\d*)?\-\-results\.json'                            # YYYYMMDDSSSSSS--results.json

# GLOBALS:
ACTION_CHOICES: list[str] = ['get_saved', 'consolidate', 'sanitize']
DEBUG_MODE: bool = False
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_REDDIT_SAVE_DIR = Path(CUR_DIR) / 'api_data' / 'reddit'

# OS ENV
SUBREDDIT_BLACK_LIST = json.loads(os.environ.get('SUBREDDIT_BLACK_LIST', '[]')) or []
VID_DOMAIN_WHITE_LIST = json.loads(os.environ.get('VID_DOMAIN_WHITE_LIST', '[]')) or []
XPATH_LIST = json.loads(os.environ.get('XPATH_LIST', '[]')) or []

# Post Type Prefixes
TYPE_PREFACE_MAPPER = {
    "t1": "comment",
    "t2": "account",
    "t3": "link",
    "t4": "message",
    "t5": "subreddit",
    "t6": "award",
}

# import utils library
script_dir = os.path.abspath(f"{os.path.dirname(CUR_DIR)}/scripts")
sys.path.insert(0, script_dir)
from utils.constants import DEFAULT_LOG_FORMAT, IMAGE_EXTENSION, IMAGE_EXTENSION_LIST, VIDEO_EXTENSION, VIDEO_EXTENSION_LIST
from utils.custom_exceptions import UnauthorizedError
from utils.custom_logging import add_handler_to_logger
from utils.date_helper import timestamp_to_date_string
from utils.file_helper import get_file_creation_date, open_json_from_file, write_json_to_file
from utils.image_helper import yt_download  # TODO: remove, this may not be working properly
from utils.navigation import make_directory
from utils.webutils import extract_media_from_url, get_video_source_url

class Token(object):
    def __init__(self):
        self.access_token = None
        self.expire_date = datetime.datetime=datetime.datetime.utcnow()
        self.is_valid = False

    def __str__(self):
        return self.access_token if self.access_token is not None else "NO ACCESS TOKEN PROVIDED."


class RedditAPI(APIBase):
    token = Token()
    reddit_url = "https://www.reddit.com"
    oauth_url = "https://oauth.reddit.com"
    base_api_url = f"{reddit_url}/api/v1"

    def __init__(self, client_id:str, client_secret:str, username:str, password:str, logger:logging.Logger=None, save_dir:Path=None, use_verbose:bool=False, **kwargs):
        super().__init__(logger=logger, save_dir=save_dir, use_verbose=use_verbose)
        self._logger.name = 'RedditAPI'

        if None in [client_id, client_secret, username, password]:
            raise ValueError("Need credentials.")

        # creds
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password

        # dirs
        if 'reddit' not in self._save_dir.name: self._save_dir = self._save_dir / 'reddit'
        self.save_dir_path: Path = make_directory(self._save_dir / f'{self.username}')
        self.api_data_dir_path: Path = make_directory(self.save_dir_path / 'api_data')

        # if no logger provided, create file handler and add to logger
        if logger is None:
            import logging.handlers
            log_dir = make_directory(directory_path=self.save_dir_path / 'logs')
            log_filename =  os.path.join(log_dir, "RedditAPI.log")
            max_byte_size_50 = 50*1024*1024 # ~52mb
            file_handler = logging.handlers.RotatingFileHandler(log_filename, maxBytes=max_byte_size_50, backupCount=5)
            self._logger = add_handler_to_logger(self._logger, file_handler)

        # session
        self._session.headers.update({"User-Agent": f"{self.username}_App/0.1 by {self.username}"})

    def __str__(self) -> str:
        return self.username

    #--------------------------
    # API methods
    #--------------------------
    def get_token(self):
        """
        Returns the JSON response for retrieving an access token.
        Updates the token object with the retrieved access token calculates the expire_date.
        """
        self._logger.debug(f"retrieving access token for {self.username}")
        auth_data = None
        url = f"{self.base_api_url}/access_token"
        client_auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)
        cred_data = {"grant_type": "password", "username": self.username, "password": self.password}
        try:
            resp = self._session.post(url=url, auth=client_auth, data=cred_data, timeout=300)
            self._logger.info(f"POST ({resp.status_code}) - {resp.url}")
            if resp.status_code == 401:
                raise UnauthorizedError("Invalid credentials.")
            resp.raise_for_status()
            self.token.is_valid = True
            auth_data = dict(resp.json())
            # self._logger.debug(f"get_token response: {json.dumps(auth_data, indent=2)}") # debugging purposes only, otherwise it becomes spammy
            if 'error' in auth_data: # case: {'error': 'invalid_grant'}
                self._logger.error(f"Unable to retrieve token: {auth_data.get('error')}")
                sys.exit()
            expires_in = float(auth_data.get('expires_in', 0))
            expire_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
            self.token.expire_date = expire_date
            self.token.access_token = auth_data.get('access_token')
            self._logger.info(f"get_token retrieved token {self.token.access_token}, expires in {expires_in}")
        except UnauthorizedError as err:
            self._logger.error(f"get_token UnauthorizedError - {err.__str__()}")
        except requests.exceptions.HTTPError as err:
            self._logger.error(f"get_token HTTPError - {err.__str__()}")
        except Exception as err:
            self._logger.error(f"get_token Exception - {err.__str__()}")
            raise err
        return auth_data if auth_data is not None else sys.exit()

    def update_token(self)->bool:
        """
        Checks access token's expire date & generates new token if necessary.
        Returns true if token is expired and get_token() is executed, otherwise returns False.
        """
        if self.token.expire_date < datetime.datetime.utcnow() or self.token.is_valid is False:
            self._logger.debug(f"generating new access token...")
            self.get_token()
            return True
        return False

    def send_request(self, url:str, method:str="GET", **kwargs):
        """
        Send request to API for given url. Returns JSON response.
        """
        self.update_token()
        self._session.headers.update({'Authorization': f"bearer {self.token}"})
        default_timeout = kwargs.pop('timeout', 300)
        data = {}
        try:
            if method.upper() == "POST":
                resp = self._session.post(url, timeout=default_timeout, **kwargs)
            else:
                resp = self._session.get(url, timeout=default_timeout, **kwargs)
            self._logger.info(f"{method.upper()} ({resp.status_code}) - {resp.url}")
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.HTTPError as err:
            # 429 Client Error -- too many requests
            if "429 Client Error" in err.__str__():
                self.logger.warning(f"429 Client Error -- too many requests: {err.__str__()}")
                return {}
            self._logger.exception(f"send_request error - {err.__str__()}")
            raise
        return data

    def get_files_to_exclude(self)->list[str]:
        """
        Return list of file names that were already extracted, exist, or listed in an 'results' file.
        """
        exclude_files_list:list[str] = []
        exclude_file_re = re.compile(r'^\d{0,2}-?EXCLUDE_FILES\.json$')
        save_file_re = re.compile(RE_RESULTS_FILE_FORMAT)
        for file in self.api_data_dir_path.iterdir():

            # get excluded files from previously saved files
            saved_file_match = save_file_re.search(file.name)
            if saved_file_match:
                data = open_json_from_file(file)
                exclude_files_list.extend(data.get("extracted", []))
                exclude_files_list.extend(data.get("already_exists", []))
                exclude_files_list.extend(data.get("excluded", []))

            # get excluded files from 'exclude' file
            exclude_match = exclude_file_re.search(file.name)
            if exclude_match:
                data = open_json_from_file(file)
                exclude_files_list.extend(data)

        exclude_files_list = list(set(exclude_files_list)) or []
        self._logger.debug(f"excluded files count: {len(exclude_files_list)}")

        # extract post name (kind_id) and append to list for better matching:
        for f in exclude_files_list:
            reddit_file_re = re.compile(RE_REDDIT_FILE_FORMAT)
            file_match = reddit_file_re.search(f)
            if file_match:
                match_group = file_match.groupdict()
                post_kind = match_group.get('post_kind')
                post_id = match_group.get('post_id')
                exclude_files_list.append(f"{post_kind}_{post_id}")

        self._logger.debug(f"UPDATED excluded files count: {len(exclude_files_list)}")
        return exclude_files_list

    def get_saved_data(self, limit:int=25, max_count:int=None, raw:bool=False)->list:
        """
        Get user's saved posts data via API. If raw parameter is True, returns raw response from request, else returns list of all saved post data.

        Keyword arguments:
            - limit     (int):  Max num of items desired to pull per request (default: 25, maximum: 100)
            - max_count (int):  Total max number of saved submissions to pull
            - raw       (bool): If True, returns raw response from the API request, else returns dictionary of all post data processed from the raw data.
        """
        url = f"{self.oauth_url}/user/{self.username}/saved"
        payload = {"limit": limit}
        self._logger.info(f"retrieving user's ({self.username}) saved data...")
        raw_data = self.send_request(url=url, params=payload)
        if raw:
            self._logger.debug(f"returning raw data, num saved items retrieved: {len(raw_data.get('data', {}).get('children', []))}")
            return raw_data
        data = raw_data.get('data', {})
        all_data = data.get('children', [])
        while (data.get('after') is not None):
            payload = {"limit": limit}
            payload["after"] = data.get('after')
            raw_data = self.send_request(url, params=payload)
            data = raw_data.get('data', {})
            all_data.extend(data.get('children', []))
            self._logger.debug(f"current num items retrieved: {len(all_data)}")

            # break if exceeds max_count:
            if max_count is not None and len(all_data) >= max_count:
                self._logger.warning(f"max_count ({max_count}) exceeded, breaking request loop...")
                break
        self._logger.info(f"total num of items retrieved:\t{len(all_data)}")
        return all_data

    def unsave_post(self, post:dict):
        """
        Remove post from user's saved. Returns json response from POST request.

        Keyword Arguments
        - post (dict): saved post to unsave
        """
        fullname = post.get('data', {}).get("name")
        self._logger.info(f"unsaving post: {fullname}")
        url = f"{self.oauth_url}/api/unsave"
        return self.send_request(url=url, method="POST", params={"id":fullname})

    #--------------------------
    # Utility Methods
    #--------------------------
    def consolidated_saved_files(self)->list[dict]:
        """
        Consolidate saved json files from the api data directory. Writes a consolidated JSON file to same directory.
        """
        self._logger.debug(f"consolidating saved files from directory: {self.api_data_dir_path.absolute()}")
        save_file_list: list[Path] = []
        consolidated_saved_data: list[dict]= []
        for path in self.api_data_dir_path.iterdir():
            if not path.is_file() or path.name.startswith('.'): continue
            re_list = [RE_OLD_REDDIT_SAVE_FILE_FORMAT, RE_REDDIT_SAVE_FILE_FORMAT]
            for regex in re_list:
                m = re.search(regex, path.stem)
                if m is None: continue
                m_year = int(m.group('year'))        # 2023
                m_month = int(m.group('month'))      # 11
                m_date = int(m.group('date'))        # 19
                m_seconds = int(m.group('seconds')) if m.group('seconds') else 0  # 220815
                save_file_list.append(path)

        for save_file in save_file_list:
            save_file_json = open_json_from_file(save_file)
            # TODO: optimize/reduce list by removing duplicates? using a set()?
            consolidated_saved_data.extend(save_file_json)

        # write to output file
        file_path = self.api_data_dir_path / f"{self._now_str_long}--consolidated_saved_data.json"
        self._logger.debug(f"saving consolidated saved data ({len(consolidated_saved_data)}) to file: {file_path.absolute()}")
        write_json_to_file(file_path, consolidated_saved_data)
        return consolidated_saved_data

    def parse_filename(self, post:Union[str,Path])->dict:
        """
        Parses post filename with regex, returns dictionary results for each group found.
        """
        filename: str = post if isinstance(post, str) else post.name
        m = re.search(RE_REDDIT_FILE_FORMAT, filename)
        if m is None: return None
        return {
            "groups": m.groups(),
            "filename": m.group(0),
            "username": m.group('username'),
            "date": m.group('date'),
            "subreddit": m.group('subreddit'),
            "post_kind": m.group('post_kind'),
            "post_id": m.group('post_id'),
            "extension": m.group('extension'),
        }

    def process_saved_data(self, saved_data: list[dict], exclude_files: list[str]=[], do_purge:bool=False):
        """
        Iterates through saved_data list to extract media.

        Keyword arguments:
            - saved_data: list of saved posts
            - exclude_files: list of files to exclude from processing
            - do_purge (bool): Defaults to False, remove (unsave) post if successfully retrieved.
        """
        results = dict(extracted=[], failed=[], already_exists=[], excluded=[])
        updated_header = {
            # TODO: update headers?
            'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }

        # iterate saved posts
        self._logger.info(f'processing saved data ({len(saved_data)} posts) ...')
        sub_dir_list :list[Path] = []   # keep track of subreddit directories created
        for idx, post in enumerate(saved_data):
            already_exists = False
            is_extracted = False

            post_kind = post['kind']
            post_kind_type = TYPE_PREFACE_MAPPER.get(post_kind, 'unknown')
            post_data = post['data']
            post_author = post_data['author']
            post_subreddit = post_data['subreddit']
            post_name = post_data.get('name', 'post_name_unavailable')
            post_date_created_timestamp = int(post_data.get('created_utc', 0))
            post_date_created_str = timestamp_to_date_string(post_date_created_timestamp)
            post_hint:str = post_data.get('post_hint', '')
            post_link_url:str = post_data.get('link_url', '')
            post_url_overridden_by_dest = post_data.get('url_overridden_by_dest', post_link_url)
            post_url:str = post_data.get('url', post_url_overridden_by_dest)
            post_domain:str = post_data.get('domain', '')
            post_ext = post_url.split(".")[-1]
            post_media = post_data.get('media') or {}
            post_secure_media = post_data.get('secure_media') or post_media
            post_secure_media_type = post_secure_media.get('type')
            post_is_video = post_data.get('is_video', False)
            is_nsfw = post_data.get('over_18', False) or post_subreddit in SUBREDDIT_BLACK_LIST
            is_gallery = post_data.get('is_gallery', False)

            # NOTE: temporarily commenting out,  fallback_url does not include sound
            # post_reddit_video = post_secure_media.get('reddit_video', {})
            # fallback_url = post_reddit_video.get('fallback_url')
            fallback_url = None

            # TODO: figure out new way to retrieve video url

            # TODO: handle gallery posts, skip for now
            if is_gallery:
                self._logger.debug(f"skipping, post ({post_name}) is a gallery...")
                continue

            # setup directory & filename to save post media
            dst_media_dir_path =  self.save_dir_path / 'nsfw' / post_author if is_nsfw else self.save_dir_path / 'subreddits' / post_subreddit
            dst_media_dir_path = make_directory(dst_media_dir_path)
            sub_dir_list.append(dst_media_dir_path)
            media_filename = f'{post_author}_{post_date_created_str}_{post_subreddit}_{post_name}'

            # ----------------------------------------
            # Retrieve media source URL by post type
            # ----------------------------------------

            # TODO: handle saved comments, skip for now
            #   - save post body as text file?
            #   - scrape text for media src url?
            if post_kind_type == 'comment':
                self._logger.debug(f"identified post ({post_name}) as a comment, skipping for now...")
                media_ext = 'json'
                continue

            # -------------------
            # IMAGE MEDIA TYPE
            # -------------------
            elif (
                (post_ext not in VIDEO_EXTENSION_LIST) and
                (('image' in post_hint) or (post_ext in IMAGE_EXTENSION_LIST))
            ):
                self._logger.debug(f"identified post ({post_name}) as image, retrieving media source url...")
                updated_header.update({"Content-type": "image/jpeg"})
                media_ext = IMAGE_EXTENSION if not post_ext or post_ext not in IMAGE_EXTENSION_LIST else post_ext
                media_src_url = post_url

            # -------------------
            # VIDEO  MEDIA TYPE
            # -------------------
            elif (
                (post_is_video) or
                ('video' in post_hint) or   # rich:video | hosted:video
                (post_ext in VIDEO_EXTENSION_LIST) or
                (post_domain in VID_DOMAIN_WHITE_LIST) or
                (post_secure_media_type == "youtube.com")
            ):
                self._logger.debug(f"identified post ({post_name}) as video, retrieving media source url from {post_url}...")

                # ---------------------
                # Handle youtube video
                # ---------------------
                re_youtube = r'youtu\.?be'
                yt_search = re.search(re_youtube, post_url)
                if (yt_search is not None) or (post_secure_media_type == "youtube.com"):
                    author_tag = str(post_secure_media.get("oembed",{}).get("author_url", "")).split("https://www.youtube.com/", 1)[-1] # https://www.youtube.com/@USERNAME
                    title = unescape(post_secure_media.get("oembed", {}).get('title', "NO_TITLE"))
                    media_filename += f"--yt--{author_tag}--{title}.{VIDEO_EXTENSION}"
                    dst_media_file_path = dst_media_dir_path / str(media_filename)

                    # skip if excluding
                    if media_filename in exclude_files or post_name in exclude_files:
                        already_exists = True
                        self._logger.debug(f'skipping extraction, yt media in exclude_files list ({media_filename}).')
                        results['excluded'].append(media_filename)

                    # skip if file already exists
                    elif dst_media_file_path.exists():
                        already_exists = True
                        self._logger.debug(f"skipping extraction, yt media already exists - {media_filename}")
                        results['already_exists'].append(dst_media_file_path.name)

                    # download, assert video file exists (was extracted)
                    else:
                        already_exists = False
                        # TODO: remove yt_video method (pytube is not wokring), skip this block of "else" once removed
                        yt_video = yt_download(video_url=post_url, output_path=dst_media_dir_path, quality="highest", title=media_filename)
                        if yt_video.exists():
                            is_extracted = True
                            self._logger.debug(f"successfully extracted yt media - {yt_video.name}")
                            results['extracted'].append(yt_video.name)
                        else:
                            self._logger.warning(f"skipping extraction, unable to extract yt media - {post_url}")
                            results['failed'].append(dst_media_file_path.name)

                    # do before continuing
                    if (already_exists or is_extracted) and do_purge:
                        self.unsave_post(post=post)

                    # handled post, continue to next post.
                    continue
                # end handling youtube video post

                # continue processing regular video media post
                updated_header.update({"Content-type": "video/mp4"})
                video_extension_exception_list =  ['gif']
                media_ext = VIDEO_EXTENSION if not post_ext or post_ext not in video_extension_exception_list else post_ext
                if post_ext in ['gif']: media_src_url = post_url
                elif post_ext=="gifv": media_src_url = post_url.replace(".gifv", ".mp4")
                elif post_url.endswith(".mp4"): media_src_url = post_url
                elif fallback_url: media_src_url = fallback_url
                else: media_src_url = get_video_source_url(post_url, xpath_list=XPATH_LIST, lgr=self._logger)
                if media_src_url is None:
                    self._logger.warning(f"skipping extraction, no video source found.")
                    continue

            # -------------------
            # UNKNOWN MEDIA TYPE
            # -------------------
            else:
                self._logger.warning(f'skipping extraction, unknown media type ({post_hint}) for {post_name}')
                continue

            # ---------------
            # EXTRACT MEDIA
            # ---------------
            media_filename += f'.{media_ext}'
            dst_media_file_path = dst_media_dir_path / str(media_filename)
            if media_filename in exclude_files or post_name in exclude_files:
                already_exists = True # used to removed post if necessary
                self._logger.debug(f'skipping extraction, media in exclude files list ({media_filename}).')
                results['excluded'].append(media_filename)
            elif dst_media_file_path.exists():
                already_exists = True
                self._logger.debug(f"skipping extraction, media already exists - {media_filename}")
                results['already_exists'].append(dst_media_file_path.name)
            else:
                already_exists = False
                is_extracted, _ = extract_media_from_url(url=media_src_url, save_path=dst_media_file_path, headers=updated_header, lgr=self._logger)
                if is_extracted and dst_media_file_path.exists() and dst_media_file_path.is_file():
                    self._logger.debug(f'successfully extracted media - {media_filename}')
                    results['extracted'].append(dst_media_file_path.name)
                else:
                    self._logger.warning(f'unsuccessfully extracted media ({post_url})')
                    results['failed'].append(dst_media_file_path.name)
                    if any(dst_media_dir_path.iterdir()) is False: dst_media_dir_path.rmdir()

            if (already_exists or is_extracted) and do_purge:
                self.unsave_post(post=post)

        # cleanup: remove empty dirs
        for x in sub_dir_list:
            if x.exists() and next(x.iterdir(), None) is None: x.rmdir()

        results['excluded_count'] = len(results['excluded'])
        results['extracted_count'] = len(results['extracted'])
        results['failed_count'] = len(results['failed'])
        results['already_exists_count'] = len(results['already_exists'])
        return results

    def retrieve_last_saved(self)->list[dict]:
        """
        Iterates through saved api_data directory to retrieve and return latest saved file.
        Returns list of dictionaries if latest saved file was found, else returns an empty list.
        """
        latest_saved_file = None
        latest_saved_file_timestamp = None
        self._logger.info(f"Retrieving last save file. Iterating through api_data directory: \'{self.api_data_dir_path.absolute()}\'")
        for idx, x in enumerate(self.api_data_dir_path.iterdir()):
            if x.is_file():
                m = re.search(RE_REDDIT_SAVE_FILE_FORMAT, x.stem)
                if m is None: continue
                m_year = int(m.group('year'))
                m_month = int(m.group('month'))
                m_date = int(m.group('date'))
                m_seconds = int(m.group('seconds')) if m.group('seconds') else 0

                x_creation_date_timestamp = get_file_creation_date(x, use_timestamp=True)
                self._logger.debug(f"processing file num {idx}: {x.name} ({x_creation_date_timestamp})")
                if latest_saved_file is None or latest_saved_file_timestamp is None:
                    latest_saved_file = x
                    latest_saved_file_timestamp = x_creation_date_timestamp
                    continue
                if x_creation_date_timestamp >= latest_saved_file_timestamp:
                    latest_saved_file = x
                    latest_saved_file_timestamp = x_creation_date_timestamp
        if latest_saved_file is None:
            self._logger.warning(f"no last save file found within {self.api_data_dir_path.name}")
            return []
        self._logger.debug(f"returning last save file: {latest_saved_file.name}")
        return open_json_from_file(latest_saved_file)

    def sanitize(self, subreddit_blacklist:list[str]=[])->dict:
        """
        Sanitize subreddit media directory to remove and separate any posts from blacklisted subreddits.
        Returns dictionary of results for files either moved, failed to move, or already exist.

        Keyword Arguments:
        subreddit_blacklist (list[str]): list of subreddit names to blacklist
        """
        import shutil
        sanitize_dir_path = self.save_dir_path / 'subreddits'
        target_dir_path = self.save_dir_path / 'nsfw'
        target_dir_path = make_directory(target_dir_path)
        results = {
            "posts_moved": [],
            "failed": [],
            "already_exists": [],
        }

        self._logger.info(f"sanitizing, iterating through directory '{sanitize_dir_path.name}'")
        for sub_dir in sanitize_dir_path.iterdir():

            # skip if subreddit not blacklisted
            if sub_dir.name not in subreddit_blacklist: continue

            # iterate posts in blacklisted subreddit directory
            self._logger.debug(f"iterating through blacklisted subreddit {sub_dir.name}")
            for post in sub_dir.iterdir():

                # skip hidden files
                if post.name.startswith('.'): continue

                parsed_filename = self.parse_filename(post)
                if parsed_filename is None:
                    self._logger.warning(f'skipping unknown filename: {post.name}')
                    continue

                # skip post if already exists in target location
                username = parsed_filename.get("username")
                target_dst = target_dir_path / username / post.name
                if target_dst.exists() and target_dst.is_file():
                    self._logger.warning(f"skipping, post already exists {target_dst.absolute()}")
                    results["already_exists"].append(str(target_dst.absolute()))
                    post.unlink()
                    continue

                # move post to target location if DNE
                self._logger.info(f'moving file {target_dst.absolute()}')
                if (target_dst.parent.exists() and target_dst.parent.is_dir()) is False:
                    make_directory(target_dst.parent)
                moved_post_path = Path(shutil.move(post.absolute(), target_dst.absolute()))

                # assert file moved and exists to target location, update results
                try:
                    assert moved_post_path is not None and moved_post_path.exists() and moved_post_path.is_file()
                    results["posts_moved"].append(str(moved_post_path.absolute()))
                except AssertionError as err:
                    self._logger.error(f"failed to move file {target_dst.absolute()}")
                    results["failed"].append(str(target_dst.absolute()))

            # cleanup: remove subdirectory if empty
            if next(sub_dir.iterdir(), None) is None: sub_dir.rmdir()
        return results


def get_args()->dict:
    parser = argparse.ArgumentParser(description="Reddit API")
    parser.add_argument('-a', '--action',
                        dest='action',
                        action='store',
                        choices=ACTION_CHOICES,
                        help='Desired action.',
                        required=True)
    parser.add_argument('-d','-v', '--verbose','--debug',
                        dest='debug',
                        action='store_true',
                        default=DEBUG_MODE,
                        help=f'Debug/verbose mode. [{DEBUG_MODE}]')
    parser.add_argument('-u', '--update',
                        dest='update',
                        action='store_true',
                        default=False,
                        help='Default is False, and will not update save data.')
    parser.add_argument('-i','-o','--input','--output',
                        dest='input',
                        metavar='PATH',
                        action='store',
                        type=str,
                        default=DEFAULT_REDDIT_SAVE_DIR.absolute(),
                        help=f'Source path of input file/directory. [{DEFAULT_REDDIT_SAVE_DIR.absolute()}]')
    parser.add_argument('-f', '--file',
                        dest='file',
                        metavar='FILE_PATH',
                        action='store',
                        type=str,
                        help='Source of file to input.')
    return vars(parser.parse_args())

def main():
    from time import time
    results = {}

    # ARGS
    args = get_args()
    save_dir = Path(args.get('input')) if args.get('input') else DEFAULT_REDDIT_SAVE_DIR
    input_file = Path(args.get('file')) if args.get('file') else None
    desired_action = str(args.get('action', ""))
    do_update = args.get('update', False)
    debug_mode = args.get('debug')

    # LOGGER
    logger = logging.getLogger("reddit")
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(console_handler)
    log_level = logging.DEBUG if debug_mode else logging.INFO
    logger.setLevel(log_level)

    # validate action
    if desired_action not in ACTION_CHOICES:
        print("\nInvalid action specified: {0}.\nOne of the following actions are required: {1}\n".format(desired_action, ACTION_CHOICES))
        sys.exit()
    else: logger.info("Performing action -- '{0}'".format(desired_action))

    params = {
        "client_id": os.environ.get('REDDIT_CLIENT_ID'),
        "client_secret": os.environ.get('REDDIT_CLIENT_SECRET'),
        "username": os.environ.get('REDDIT_USERNAME'),
        "password": os.environ.get('REDDIT_PASSWORD'),
        # "logger": logger,     # exclude logger for now, to use FileHandler log rotation
        "save_dir": save_dir,
        "use_verbose": debug_mode,
    }
    reddit = RedditAPI(**params)
    logger = reddit._logger
    results: dict = {}

    # ACTION: get_saved -- retrieve and processes saved posts
    if desired_action == 'get_saved':
        t0 = time()
        saved_data:list[dict] = []
        exclude_files: list[str] = []

        # retrieve saved data from given input file
        if not do_update and input_file and input_file.exists() and input_file.is_file():
            saved_data = open_json_from_file(input_file)

        # retrieve saved data from last saved file
        elif not do_update:
            saved_data = reddit.retrieve_last_saved()

        # retrieve saved data via API
        if do_update or saved_data is None or not len(saved_data):
            saved_data = reddit.get_saved_data()
            filename = reddit.api_data_dir_path / f"{reddit._now_str_long}--saved_data.json"
            write_json_to_file(filename, saved_data)

        # process saved data
        do_purge: bool = not debug_mode
        if do_purge: logger.warning("do_purge is enabled")
        exclude_files = reddit.get_files_to_exclude()
        results = reddit.process_saved_data(saved_data=saved_data, exclude_files=exclude_files, do_purge=do_purge)
        t1 = time()
        logger.info("finished get_saved in {0} seconds".format(t1-t0))

    # ACTION: consolidate -- combine saved data into one JSON file
    if desired_action == 'consolidate':
        t0 = time()
        results = reddit.consolidated_saved_files()
        t1 = time()
        logger.info("finished consolidation in {0} seconds".format(t1-t0))
        return

    # ACTION: sanitize -- clean subreddit directories to remove and separate blacklisted subreddits
    if desired_action == 'sanitize':
        t0 = time()
        results = reddit.sanitize(subreddit_blacklist=SUBREDDIT_BLACK_LIST)
        t1 = time()
        logger.info("finished sanitizing in {0} seconds".format(t1-t0))

    if results and isinstance(results, dict):
        for k,v in results.items():
            if isinstance(v, list):
                results[k] = sorted(v, key=lambda x: x.lower())
        filename = reddit.api_data_dir_path / f"{reddit._now_str_long}--results.json"
        write_json_to_file(filename, results)
        logger.info(f"results for action '{desired_action}':\n{json.dumps(results, indent=2)}")
    else: logger.warning("no results returned")
    sys.exit()

if __name__ == '__main__':
    main()
