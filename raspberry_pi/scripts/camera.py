#!/usr/bin/env python
#!/usr/bin/python3

import argparse
import datetime
import logging
import sys

from picamera import PiCamera
from pathlib import Path
from subprocess  import call
from time import sleep


try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

DEBUG_MODE: bool = False
DEFAULT_SLEEP_TIME_IN_SECONDS: int = 10
DEFAULT_DATETIME_FMT_SHORT = '%Y%m%d'
DEFAULT_DATETIME_FMT_SHORT = '%Y%m%d%H%M%S' # 20240315202119
CUR_DIR: Path = Path(__file__).parent       # current parent directory of script
VID_DIR: Path = Path('/home/pi/Videos/')
PIC_DIR: Path = Path('/home/pi/Pictures/')
assert VID_DIR.exists() and VID_DIR.is_dir() and PIC_DIR.exists() and PIC_DIR.is_dir()

log_format = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
log_level: int = logging.DEBUG if DEBUG_MODE else logging.INFO
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
# console_handler.setLevel(log_level)
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)
logger.setLevel(log_level)

now = datetime.datetime.now()   # current locale
now_str = now.strftime(DEFAULT_DATETIME_FMT_SHORT)

# TODO:
# - add parse argument inputs:
#     - debug
#     - output filename/path
#     - sleeptime for recordings
#     - actions
#       - take pic
#       - take recording

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--debug',
        dest='debug',
        action='store_true',
        default=DEBUG_MODE,
        help=f'Debug mode. [{DEBUG_MODE}]')
    parser.add_argument('-t', '--time',
        dest='sleeptime',
        metavar='SECONDS',
        action='store',
        type=int,
        default=10,
        help='Enter a time in seconds for capture length [defaults to 10 seconds].')
    parser.add_argument('-f', '--filename',
        dest='filename',
        action="store",
        type=str,
        help='Provide a filename.')
    # list of actions to use
    cat_list = ['capture', 'record']
    parser.add_argument('action',
            choices=cat_list,
            metavar=f'actions: {cat_list}',
            action='store',
            type=str,
            help='Action to perform.')
    return vars(parser.parse_args())

def capture(filename:str=None, img_fmt:Literal['jpeg','jpg']='jpeg', shutter_speed:int=1000, scale_shutter:float=1)->bool:
    """
    Capture images.
    Keyword Arguments:
    - filename: filename of images
    - img_fmt: image format
    - shutter_speed: defaults to 1000 (1ms)
    """
    shutter_speed = 1000000 # 1000 milliseconds / 1 second
    # shutter_speed *= 2
    # shutter_speed *= 3
    try:
        # TODO: enhance this with some regex (check for dot notation)
        if filename is not None and filename.endswith(img_fmt) is False: filename += f'.{img_fmt}'

        outfile: Path = PIC_DIR / f"{now_str}-image.{img_fmt}" if filename is None else PIC_DIR / filename
        logger.debug(f'capturing {outfile.name}')
        with PiCamera() as camera:
            # check camera exposure on last capture
            logger.debug(f"exposure_mode: {camera.exposure_mode}")
            initial_shutter_speed = camera.shutter_speed
            # logger.debug(f'updating shutter speed from {initial_shutter_speed} to {shutter_speed}')
            # camera.shutter_speed = shutter_speed
            camera.start_preview()
            camera.capture_sequence([str(outfile.absolute())], use_video_port=True)
            camera.stop_preview()
    except Exception as err:
        logger.exception(f"issue converting h264 to mp4 -- {err.__str__}")
        return False
    return True

def record(filename:str=None, time_in_seconds:int=DEFAULT_SLEEP_TIME_IN_SECONDS, convert_mp4:bool=True)->bool:
    outfile: Path = VID_DIR / f"{now_str}-video.h264" if filename is None else VID_DIR / filename
    mp4_outfile: Path = outfile.parent / f"{outfile.stem}.mp4"


    try:
        with PiCamera() as camera:
            logger.debug(f'recording {outfile.name}')
            camera.start_preview()
            camera.start_recording(str(outfile.absolute()))
            sleep(time_in_seconds)
            camera.stop_recording()
            camera.stop_preview()

        # try converting to mp4 file
        if convert_mp4:
            logger.debug('tying to convert video to mp4 format')
            command = f"MP4Box -add {outfile.absolute()} {mp4_outfile.absolute()}"
            retcode = call([command], shell=True)
            logger.debug(f"vid converted with return code: {retcode}")
    except Exception as err:
        logger.exception(f"issue converting h264 to mp4 -- {err.__str__}")
        return False
    return True

def main():
    # setup args
    args = get_args()
    debug_mode = args.get('debug', False) or DEBUG_MODE
    sleeptime:int = args.get('sleeptime', DEFAULT_SLEEP_TIME_IN_SECONDS)
    filename:str = args.get('filename')
    action = args.get('action')

    log_level:int = logging.DEBUG if debug_mode else logging.INFO
    logger.setLevel(log_level)
    logger.info(f"args: {args}")
    logger.debug("IN DEBUG MODE")
    logger.debug(f"sleeptime: {sleeptime}")
    logger.debug(f"filename: {filename}")

    # TODO: get action to perform

    if action == 'record':
        record(filename, sleeptime)
    elif action == 'capture':
        capture(filename)
    else:
        pass

    sys.exit(0)

if __name__ == '__main__':
    main()