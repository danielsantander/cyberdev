#!/usr/bin/env python
#!/usr/bin/python3

"""
usage: youtube.py [-h] [-d] [-i PATH] [-o PATH] url
ex: ./youtube.py "youtube_video_url_link" -d -o /path/to/output/directory/
"""

import logging
import os
import sys
from pathlib import Path

# GLOBALS:
DEBUG_MODE = False
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_YT_SAVE_DIR = Path(CUR_DIR) / 'api_data' / 'youtube'
script_dir = os.path.abspath(f"{os.path.dirname(CUR_DIR)}/scripts")   # ./python/scripts
sys.path.insert(0, script_dir)
from utils.constants import DEFAULT_LOG_FORMAT
from utils.custom_logging import create_logger
from utils.image_helper import yt_download
from utils.script_helper import get_args

def get_args():
    parser = get_args(description='Youtube Downloader', debug_mode=DEBUG_MODE)
    parser.add_argument('url', type=str, action='store', help='Video URL')
    parser.add_argument('-t', '--title', type=str, nargs='?', default=None, help="Title downloaded video.")
    return vars(parser.parse_args())

def main():
    # args
    args = get_args()
    debug_mode = args.get('debug', False) or DEBUG_MODE
    output_dir_path = (DEFAULT_YT_SAVE_DIR) if args.get('output') is None else Path(args.get('output'))
    video_url = args.get('url')
    video_title = args.get('title')

    # logger
    log_dir = DEFAULT_YT_SAVE_DIR / 'logs'
    log_level = logging.DEBUG if debug_mode else logging.INFO
    logger = create_logger(name="YouTube", level=log_level, format=DEFAULT_LOG_FORMAT, log_dir=log_dir)
    logger.debug(f"args: {args}")

    # download video
    logger.info(f"retrieving video: {video_url}")
    video_file_path = yt_download(video_url=video_url, output_path=output_dir_path, title=video_title, lgr=logger)
    if video_file_path.exists(): logger.info(f"Successfully downloaded video: {video_url}")
    else: logger.error(f"Failed to download video: {video_url}")
    return

if __name__ == '__main__':
    main()