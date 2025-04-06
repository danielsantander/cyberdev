import logging
import lxml
import requests
import os
from pathlib import Path
from typing import Any, Optional
from lxml import html
from utils.constants import XPATH_LIST
from utils.custom_logging import create_console_logger

DEBUG_MODE: bool = False
logger = create_console_logger(name='webutils', level=logging.DEBUG)

# TODO:
# - validate url with some regular expression, perhaps by passing verify method to type in parser.
# - write unittests

def get_video_source_url(url: str, request_timeout: int=120, xpath_list:list[str]=None, lgr:logging.Logger=logger)->Optional[str]:
    """
    Web scrape HTML page for video source links.
    Returns video source URL link if found, or else returns None.

    Keyword arguments:
    url -- url of page to search
    request_timeout -- time in seconds for request timeout [120]
    xpath_list -- list[str]: list of xpaths to iterate
    """
    assert url is not None
    video_src_url = None
    lgr.info(f"get_video_source_url -- retrieving source from: {url}")

    # get response
    try:
        resp = requests.get(url, timeout=request_timeout)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if "403 client error" in str(err).lower():
            lgr.error(f"get_video_source_url -- HTTP 403 forbidden error ({url}): {err.__str__()}")
        elif "404 client error" in str(err).lower():
            lgr.error(f"get_video_source_url -- HTTP 404 client error ({url}): {err.__str__()}")
        elif "429 client error" in str(err).lower():
            lgr.error(f"get_video_source_url -- HTTP 429 client error ({url}): {err.__str__()}")
        else:
            lgr.error(f"get_video_source_url -- Unknown error retrieving video source ({url}): {err.__str__()}")
        return None
    except requests.exceptions.ConnectionError as err:
        lgr.error(f"get_video_source_url -- ConnectionError retrieving video source ({url}): {err.__str__()}")
        return None
    except Exception as err:
        lgr.error(f"get_video_source_url -- UNKNOWN ERROR: {err.__str__()}")
        return None

    # search html content
    try:
        html_code = resp.content.strip()
        tree = html.fromstring(html_code)
        xpath_list = XPATH_LIST + xpath_list if xpath_list else XPATH_LIST
        for xpath in xpath_list:
            results = tree.xpath(xpath)
            for source in results:
                src_url = str(source.get('src', source.get('content', ""))).strip()
                if "-mobile" in src_url: continue
                if src_url:
                    lgr.debug(f"get_video_source_url -- video source found {src_url} from xpath {xpath}")
                    return src_url
    except lxml.etree.ParserError as err:
        lgr.error(f'get_video_source_url -- ParserError: {err.__str__}')
        video_src_url = None
    return video_src_url

def extract_media_from_url(url:str, save_path:Path=None, request_timeout:int=120, headers:dict={}, lgr:logging.Logger=logger)->tuple[bool, Any]:
    """
    Extract media from provided URL and save in given path.
    """
    assert save_path
    parent_dir = save_path.parent
    if not parent_dir.exists(): parent_dir.mkdir(parents=True, exist_ok=True)
    s = requests.Session()
    chuck_size = 256
    file_stat_info = None
    is_success = False
    try:
        resp = s.get(url=url, stream=True, timeout=request_timeout, headers=headers)
        lgr.debug(f"extract_media_from_url -- extraction request ({resp.status_code}): {resp.url}")
        resp.raise_for_status()
        with open(save_path.absolute(), 'wb') as save_file:
            for chunk in resp.iter_content(chunk_size=chuck_size):
                save_file.write(chunk)
        assert save_path.exists()
        is_success = bool(save_path.exists() and resp.ok)
        file_stat_info = os.stat(save_path.resolve()) if is_success else None
        if not is_success:
            lgr.error(f'extract_media_from_url -- unable to save media {save_path.name} from {url}')
            if any(parent_dir.iterdir()) is False: parent_dir.rmdir()
    except requests.exceptions.HTTPError as err:
        if '400 Client Error' in err.__str__():
            lgr.error(f'extract_media_from_url -- 400 Client Error -- {err.__str__()}')
        elif '403 Client Error' in err.__str__():
            lgr.error(f'extract_media_from_url -- Forbidden 403 Error -- {err.__str__()}')
        elif '404' in err.__str__():
            lgr.error(f"extract_media_from_url -- Media not found, does not exist -- {err}")
        elif '410 Client Error' in err.__str__():
            lgr.error(f'extract_media_from_url -- 410 Client Error -- {err.__str__()}')
        elif '429 Client Error' in err.__str__():
            lgr.error(f"extract_media_from_url -- 429 Client Error: {err.__str__()}")
        elif '502 Server Error' in err.__str__():
            lgr.error(f"extract_media_from_url -- 502 Server ERror: {err.__str__()}")
        else:
            lgr.error(f"extract_media_from_url -- UNKNOWN ERROR: {err.__str__()}")
        is_success = False
        file_stat_info = None
    return is_success, file_stat_info
