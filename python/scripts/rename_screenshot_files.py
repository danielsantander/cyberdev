#!/usr/bin/python3

""" Script to rename screenshot files into a more informative title. """
import argparse
import datetime
import logging
import re
from pathlib import Path
from utils.validation import str2bool
DEFAULT_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %I:%M:%S"
RE_SCREENSHOT_FILENAME = r'Screen Shot (?P<date>\d{4}-\d{2}-\d{2}) at (?P<time>\d{1,2}\.\d{1,2}\.\d{1,2})\s?(?P<meridiem>\w{2})\.\w{3}$'

# logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
# logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', level=logging.DEBUG)

def get_args():
    parser = argparse.ArgumentParser(description="Rename screenshot files")
    parser.add_argument('path', action='store', help='Path of screenshot file or directory containing screenshot files.')
    parser.add_argument('-d','--debug', dest='debug', action='store_true', help='logging.DEBUG level logs output to stdout')
    parser.add_argument("--nice", type=str2bool, nargs='?', const=True, default=False, help="Activate nice mode.")
    return vars(parser.parse_args())

if __name__ == '__main__':
    import sys
    args = get_args()
    path = Path(args.get('path'))
    debug = args.get('debug')

    # temp:
    # print (f'\ndebug:\t{str(debug).upper()}')
    # is_nice = args.get('nice', False)
    # print (f'\nis_nice:\t{str(is_nice).upper()}')
    # sys.exit()
    
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=log_level, format='%(asctime)s %(message)s', datefmt=DEFAULT_DATE_FORMAT)

    logging.debug("starting...")
    logging.info(f"path:\t{path.absolute()}")
    logging.info(f"debug:\t{debug}") 

    if path.is_dir():
        dirname = path.name if path.name.endswith('_') else f'{path.name}_'
        for file in path.iterdir():
            # filename: "Screen Shot 2022-06-25 at 5.30.26 PM.png"
            new_filename = dirname
            file_ext = file.suffix  # .png
            match_date = re.search(RE_SCREENSHOT_FILENAME, file.name)   # match_date.group(): Screen Shot 2022-06-25 at 5.30.26 PM.png
            if match_date is None or len(match_date.groups()) < 3: 
                logging.warning(f'skipping, no date matched for file: {file.name}')
                continue

            combined_date = f"{match_date.group('date')} {match_date.group('time')} {match_date.group('meridiem')}"    # "2022-06-25 5.30.26 PM"
            date_obj = datetime.datetime.strptime(combined_date, '%Y-%m-%d %I.%M.%S %p')
            posix_timestamp = int(date_obj.timestamp())
            new_filename += str(posix_timestamp) + file_ext    # dir-name_posix-timestamp.extension

            logging.info(f'dirname:\t{dirname}')
            logging.info(f'filename:\t{file.name}')
            logging.info(f'match_date:\t{match_date}')
            logging.info(f"new_filename: {new_filename}")
            rename = path / (new_filename)
            file.rename(rename)
            # break
