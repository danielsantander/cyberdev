#!/usr/bin/env python
#!/usr/bin/python3

import requests
import datetime
import logging
import os
import sys
from pathlib import Path
from typing import Optional

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.abspath(f"{os.path.dirname(CUR_DIR)}/scripts")
sys.path.insert(0, scripts_dir)
from utils.constants import DEFAULT_DATETIME_FMT_LONG, DEFAULT_DATETIME_FMT_SHORT
from utils.custom_logging import create_console_logger

class APIBase(object):
    def __init__(self, logger:logging.Logger=None, save_dir:Path=None, use_verbose:bool=False, **kwargs):
        self._use_verbose: bool = use_verbose

        # save directory
        if save_dir is None: save_dir = Path(CUR_DIR)
        self._save_dir = self._verify_or_create_directory(save_dir)

        # dates
        self._now = datetime.datetime.now(datetime.timezone.utc)
        self._now_str_long = self._now.strftime(DEFAULT_DATETIME_FMT_LONG)
        self._now_str_short = self._now.strftime(DEFAULT_DATETIME_FMT_SHORT)

        # logger
        log_level = logging.DEBUG if use_verbose else logging.INFO
        self._logger = logger if logger is not None else create_console_logger(name="API", level=log_level)
        self._logger.debug(f"APIBase init complete -- save dir: {self._save_dir.absolute()}")

        # init
        self._session = self.__setup_session()

    def __setup_session(self)->requests.Session:
        from urllib3.util.retry import Retry
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = requests.adapters.HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        # self._logger.debug('session setup complete')
        return session

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
