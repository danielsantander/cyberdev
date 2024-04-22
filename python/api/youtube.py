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
CUR_DIR = os.path.dirname(os.path.abspath(__file__))     # ./python/api
CUR_DIR_PATH = Path(CUR_DIR)
PARENT_DIR = os.path.dirname(CUR_DIR)                    # ./python
SCRIPTS_DIR = os.path.abspath(f"{PARENT_DIR}/scripts")   # ./python/scripts
sys.path.insert(0, SCRIPTS_DIR)
from utils import (
    constants,
    custom_logging,
    image_helper,
    script_helper,
)

def get_args():
    parser = script_helper.get_args(description='Youtube Downloader', debug_mode=DEBUG_MODE)
    parser.add_argument('url', type=str, action='store', help='Video URL')
    parser.add_argument('-t', '--title', type=str, nargs='?', default=None, help="Title downloaded video.")
    return vars(parser.parse_args())

def main():
    # args
    args = get_args()
    debug_mode = args.get('debug', False) or DEBUG_MODE
    output_dir_path = (CUR_DIR_PATH / 'youtube') if args.get('output') is None else Path(args.get('output'))
    video_url = args.get('url')
    video_title = args.get('title')

    # logger
    log_dir = CUR_DIR_PATH / 'logs'
    log_level = logging.DEBUG if debug_mode else logging.INFO
    logger = custom_logging.create_logger(name="YouTube", level=log_level, format=constants.DEFAULT_LOG_FORMAT, log_dir=log_dir)
    logger.debug(f"args: {args}")

    # download video
    logger.info(f"retrieving video: {video_url}")
    video_file_path = image_helper.yt_download(video_url=video_url, output_path=output_dir_path, title=video_title)
    if video_file_path.exists(): logger.info(f"Successfully downloaded video: {video_url}")
    else: logger.error(f"Failed to download video: {video_url}")
    return

if __name__ == '__main__':
    main()