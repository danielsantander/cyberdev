#!/usr/bin/env python
#!/usr/bin/python3

import requests
import datetime
import logging
import os
import sys
from pathlib import Path
from typing import Optional, Union

API_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.dirname(API_DIR)
sys.path.insert(0, SCRIPTS_DIR)
from utils.constants import DEFAULT_API_SAVE_DIRECTORY, DEFAULT_DATETIME_FMT_LONG, DEFAULT_DATETIME_FMT_SHORT
from utils.custom_logging import create_logger


class APIBase(object):
    def __init__(self, logger:logging.Logger=None, save_dir:Path=None, use_verbose:bool=False, **kwargs):
        self._use_verbose: bool = use_verbose

        # dates
        self._now = datetime.datetime.now(datetime.timezone.utc)
        self._now_str_long = self._now.strftime(DEFAULT_DATETIME_FMT_LONG)      # YYYYMMDDHHMMSS
        self._now_str_short = self._now.strftime(DEFAULT_DATETIME_FMT_SHORT)    # YYYYMMDD

        # save directory
        if save_dir is None:
            self._logger.debug('No save directory provided, using current directory path.')
            save_dir = Path(DEFAULT_API_SAVE_DIRECTORY) / 'APIBaseDirectory'
        self._save_dir = self._verify_or_create_directory(save_dir)

        # logger
        log_level = logging.DEBUG if self._use_verbose else logging.INFO
        if logger and isinstance(logger, logging.Logger):
            self._logger = logger
        # elif logger and isinstance(logger, str):
        #     self._logger = logging.getLogger(logger)
        else: self._logger = logging.getLogger("APIBase")
        self._logger.setLevel(log_level)
        self._logger.debug(f"APIBase init complete -- _save_dir: {self._save_dir.absolute()}")

        # init
        self._session = self.__setup_session()

    def _create_logger(self, log_name:str, log_level=None, log_dir:Union[Path, str, None]=None)->logging.Logger:
        if log_level is None: log_level = logging.DEBUG if self._use_verbose else logging.INFO
        self._logger = create_logger(name=log_name, level=log_level, log_dir=log_dir)
        return self._logger

    def __setup_session(self)->requests.Session:
        from urllib3.util.retry import Retry
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = requests.adapters.HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        # self._logger.debug('session setup complete')
        return session

    def send_request(self, url:str, method:str='GET', **kwargs)->Optional[requests.Response]:
        default_timeout = kwargs.pop('timeout', 300)
        try:
            if method.upper() == 'POST':
                # TODO: continue here
                pass
            else:
                resp = self._session.get(url, timeout=default_timeout, **kwargs)
                self._logger.debug('send_request -- {0} {1} {2}'.format(method.upper(), resp.status_code, resp.url))
                resp.raise_for_status()
                return resp
        except requests.exceptions.HTTPError as err:
            if '403 Client Error' in err.__str__(): self._logger.error("403 Client Error for {0}".format(resp.url))
            raise
        except Exception as err:
            self._logger.error(f"send_request error - {err.__str__()}")
            raise
        return requests.Response()

    def _verify_or_create_directory(self, dir_path:Path)->Optional[Path]:
        """
        Verifies the given dir_path is a valid directory.
        Returns Path if exists or created, returns None otherwise.
        """
        if dir_path is None: return None
        if dir_path.exists() and dir_path.is_dir(): return dir_path
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path

    # TODO: create class methods for API requests
