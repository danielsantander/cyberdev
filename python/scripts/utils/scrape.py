#!/usr/bin/python3

""" Methods to help parse HTML data. """
from venv import create
import requests
from lxml import html
from utils.custom_logging import create_logger

LOGGER_NAME = 'Scrape'
LOGGER_LEVEL = logging.DEBUG
LOGGER = create_logger(LOGGER_NAME, LOGGER_LEVEL)

def get_src(url:str, src_type:str="video"|"image") -> str:
    """Parses HTML page for src attribute from either vid or img tags.
    
    Keyword arguments:
    url -- URL to retrieve and parse
    src_type -- type of src to extract, options are 'vid', 'img'. (default vid)
    """
    LOGGER.debug(f'Parsing source type \'{src_type}\' from url {url}')
    try:
        resp = request.get(url, timeout=30)
        resp.raise_for_status()
        tree = html.fromstring(resp.content)
                
        xpaths = {
            "vid": [
                "video"
                "video/source[@src and @type='video/mp4']",
                "//video/source[@src and @type='video/mp4']",
                "//video/source[@src]",
                "//video/source",
                "//video/source[@type='video/mp4']",
            ],
            "img": [
                "image"
            ]
        }
    except requests.exceptions.HTTPError as err:
        if '403' in str(err):
            err_msg = "ERROR - 403 request error"
            LOGGER.error(err_msg)
    return None