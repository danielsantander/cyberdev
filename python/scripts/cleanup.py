#!/usr/bin/env python
#!/usr/bin/python3

"""
Script to clean up a given directory. Will consolidate files into their own directories, such as:
    - screenshots/
    - PDF/
    - JPEG/
    - PNG/
    - etc

Usage: $ ./cleanup.py <source directory path> <destination directory path [OPTIONAL]>

Results: Files consolidated into their own directories.

"""

# TODO items
# 1. pass lgr=logger into main() instead of debug_mode
# 2. also move directories in the given src_directory
# 3. add optional arguments:
    # to accept files to ignore
    # option for verbose mode
# 4. add a 'random/' sub-directory for images without a category


import argparse
import logging
import os
import re
from pathlib import Path
from typing import List, TypedDict
from utils import constants, custom_logging, file_helper, navigation

DEBUG_MODE = True
CURRENT_DIR_PATH = Path(os.path.dirname(os.path.realpath(__file__))) # script executed here


class MovedResults(TypedDict):
    moved_files_list: List[Path]
    failed_moved_files_list: List[Path]


def get_args():
    """
    Setup and return program arguments.

    Returns a key/value type all program arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', '-d',
        action='store_true',
        help="Debug mode. [False]")
    parser.add_argument('src',
        nargs="?",
        metavar="src_path",
        type=str,
        default=CURRENT_DIR_PATH.absolute(),
        help="Enter source path of directory containing files. [defaults to current working directory]")
    parser.add_argument('dst',
        nargs="?",
        metavar="dst_path",
        type=str,
        help="Enter destination path of directory to move files into. [defaults to source path]")
    return vars(parser.parse_args())


def main(src_directory:Path, dst_directory:Path, debug_mode:bool=True)->MovedResults:
    results:MovedResults = {
        "moved_files_list": [],
        "failed_moved_files_list": []
    }

    # iterate directory
    dir_items: List[Path] = file_helper.iterate_directory(src_directory, excludeHiddenFiles=True)
    destination = dst_directory
    for item in dir_items:
        if not item.is_file():
            results['failed_moved_files_list'].append(item)
            continue

        filename = item.name
        apple_screenshot_regex = re.compile(constants.RE_APPLE_SCREEN_SHOT)
        apple_screenshot_match = apple_screenshot_regex.search(filename)
        extension_match = re.compile(constants.RE_FILE_EXTENSION).search(filename)

        if apple_screenshot_match is not None:
            match_group = apple_screenshot_match.groupdict()
            file_extension = match_group.get('extension')
            destination = dst_directory / 'screenshots'
            category = match_group.get('category')
            if category is not None: destination = destination / str(category)
            if match_group.get('phone_screenshot'): logger.debug(f'match found -- Apple iPhone screenshot: {filename}')
            elif match_group.get('mac_screenshot'): logger.debug(f'match found -- MacOS screenshot: {filename}')

        elif extension_match is not None:
            match_group = extension_match.groupdict()
            extension = match_group.get("extension", "")
            if extension in ["", None]:
                logger.debug(f"Unknown extension '{extension}'.")
                continue
            else:
                logger.debug(f'match found -- with extension: {extension.upper()}')
                destination = dst_directory / str(extension.upper())
        else:
            logger.warning(f'match not found -- unknown file type, skipping file: {filename}')
            results['failed_moved_files_list'].append(item)
            continue

        new_filepath = None if debug_mode else navigation.move_file(file_src=item, dst_dir=destination)
        if new_filepath is None: results['failed_moved_files_list'].append(item)
        else: results['moved_files_list'].append(item)
    return results

if __name__ =="__main__":

    # get args
    args = get_args()
    debug_mode = args.get('debug', DEBUG_MODE)
    src_directory = Path(args.get('src') or CURRENT_DIR_PATH)
    dst_directory = Path(args.get('dst') or src_directory)

    # setup logger
    log_level = logging.DEBUG if debug_mode else logging.INFO
    logger = custom_logging.create_console_logger(name=str(__name__),level=log_level)
    logger.debug(f'args:\t{args}')

    # run
    results = main(src_directory, dst_directory, debug_mode)
    moved_files_list =  results['moved_files_list'] or []
    failed_moved_files_list = results['failed_moved_files_list'] or []

    # print results
    print(f"\nRESULTS:\n{'-------'*15}")
    # moved_filenames = '\n\t'.join([x.name for x in moved_files_list])
    # unmoved_filenames = '\n\t'.join([x.name for x in failed_moved_files_list])
    # print(f"Moved Files:\n\t{moved_filenames}")
    # print(f"Unmoved Files:\n\t{unmoved_filenames}")
    print(f"moved count: {len(moved_files_list)}\nunmoved count: {len(failed_moved_files_list)}")
    print("-------"*15)
