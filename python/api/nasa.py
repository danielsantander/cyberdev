#!/usr/bin/env python
#!/usr/bin/python3
"""
usage: ./nasa.py --noinput --debug
"""

import argparse
import datetime
import os
import re
import requests
import sys
from pathlib import Path
from typing import Union
from logging import DEBUG, INFO

DEBUG_MODE = False
NO_INPUT = False
API_DIR = os.path.dirname(os.path.abspath(__file__)) # ./python/api
PY_DIR = os.path.dirname(API_DIR)                    # ./python
SCRIPTS_DIR = os.path.abspath(f"{PY_DIR}/scripts")   # ./python/scripts
sys.path.insert(0, SCRIPTS_DIR)
from utils import constants, custom_exceptions, custom_logging, file_helper, image_helper, navigation, script_helper, validation

def get_args():
    parser = script_helper.get_args(description="NASA API", debug_mode=DEBUG_MODE)
    parser.add_argument('--noinput',
                        dest='noinput',
                        action='store_true',
                        default=False,
                        help="Prevent input prompt and use default values.")
    return vars(parser.parse_args())

class EPIC(object):
    def __init__(self, save_dir: Union[str, Path]=None, debug_mode: bool=DEBUG_MODE) -> None:
        self.base_url = "https://epic.gsfc.nasa.gov"
        self.api_url = f"{self.base_url}/api/"
        self.save_dir:Path = self._verify_save_dir(save_dir)
        self._logger = custom_logging.create_logger(name="EPIC", level=DEBUG if debug_mode else INFO , format=constants.DEFAULT_LOG_FORMAT, log_dir=self.save_dir/'logs')
        self._now = datetime.datetime.utcnow()
        self._now_str = self._now.strftime(constants.DEFAULT_DATETIME_FMT_SHORT)

    def _verify_save_dir(self, dir_path: Union[str, Path]=None)->Path:
        default_path = Path(os.path.abspath(os.path.dirname(__file__))) # api/
        verified_path: Path = default_path
        if dir_path is not None and isinstance(dir_path, Path) and dir_path.is_dir(): verified_path = dir_path
        if isinstance(dir_path, str):
            new_path = Path(dir_path)
            if new_path.is_dir(): verified_path = new_path
        if not verified_path.is_dir(): raise custom_exceptions.InvalidDirectory()
        return verified_path

    def get_epic_images(self, use_enhanced: bool=False, use_png: bool=False):
        gif_dir: Path = navigation.make_directory(self.save_dir/'nasa'/'gifs')
        images_dir: Path = navigation.make_directory(self.save_dir/'nasa'/'images')
        data_dir: Path=navigation.make_directory(self.save_dir/'nasa'/'data')
        sub_save_dir:Path = None # directory to save this iteration of images
        assert gif_dir.is_dir() and images_dir.is_dir() and data_dir.is_dir()

        chunk_size = 256
        isSuccess = True

        # Get image data
        url = f"{self.api_url}"
        url = f"{self.api_url}enhanced/" if use_enhanced else f"{self.api_url}natural/"
        resp = requests.get(url)
        assert resp.status_code == 200
        self._logger.debug(f"media extraction request ({resp.status_code}) -- {resp.url}")
        data_list = resp.json()

        # save data
        if len(data_list) == 0:
            self._logger.info("No data retrieved, exiting.")
            return
        identifier_date = datetime.datetime.strptime(data_list[0].get('identifier'), constants.DEFAULT_DATETIME_FMT_LONG).strftime(constants.DEFAULT_DATETIME_FMT_SHORT)
        file_path = data_dir/f'{identifier_date}.json'
        proceed = True
        if file_path.exists():
            input_msg = f"Image data file {file_path.name} already exists, overwrite (Y/N)? [N]: "
            raw_input = "N" if NO_INPUT else input(input_msg) or "N"
            proceed = validation.str2bool(raw_input)
        if file_path.exists() is False or proceed:
            file_helper.write_json_to_file(file_path, data_list)

        # iterate data to get images
        for idx, data in enumerate(data_list):
            # retrieve image date YYYYMMDD
            m = re.search(constants.RE_NASA_IMG_DATES, data.get('date', ''))
            if m is None:
                self._logger.warning("NO dates found for data, skipping...")
                continue
            year = m.group('year')
            month = m.group('month')
            date = m.group('date')
            if sub_save_dir is None: sub_save_dir = navigation.make_directory(images_dir / str(f"{year}{month}{date}"))

            # setup save destination
            collection = "enhanced" if use_enhanced else "natural"
            image_type = "png" if use_png else "jpg"
            image_name = data.get('image', '')
            image_filename = f"{str(idx).zfill(2)}_{image_name}"
            image_filename += f".{image_type}"
            save_dest:Path = sub_save_dir / image_filename
            if save_dest.exists() and save_dest.is_file() and save_dest.name.endswith(image_type):
                self._logger.warning(f'image file ({save_dest.name}) already exists.')
                input_msg = f"Image file ({save_dest.name}) already exists, overwrite (Y/N)? [N]: "
                raw_input = "N" if NO_INPUT else input(input_msg) or "N"
                proceed = validation.str2bool(raw_input)
                if proceed is False: continue

            # retrieve image from API
            try:
                url = f"{self.base_url}/archive/{collection}/{year}/{month}/{date}/{image_type}/{data.get('image', '')}.{image_type}"
                resp = requests.get(url, stream=True)
                self._logger.debug(f"image extraction request ({resp.status_code}): {resp.url}")
                resp.raise_for_status()
                with open(save_dest.absolute(), 'wb') as save_file:
                    for chunk in resp.iter_content(chunk_size=chunk_size):
                        save_file.write(chunk)
                if save_dest.exists() and resp.ok:
                    # isSuccess = True
                    continue
                else:
                    isSuccess = False
                    self.__logger.warning(f'unable to save media {save_dest.name} from {url}, skipping')
                    continue
            except requests.exceptions.HTTPError as err:
                err_msg = err.__str__()
                self._logger.exception(f"error retrieving image ({resp.url}): {err_msg}")
                continue

        if isSuccess:
            gif_path = gif_dir / f"{sub_save_dir.stem}.gif"
            if gif_path.exists() is False: image_helper.jpg_to_gif(sub_save_dir, gif_dir, gif_name=f"{sub_save_dir.stem}.gif")

        return isSuccess

class NASA(EPIC):
    def __str__(self) -> str:
        print("NASA API")


if __name__ == '__main__':
    args = get_args()
    NO_INPUT = args.get('noinput', False)
    DEBUG_MODE = args.get('debug', DEBUG_MODE)
    nasa = NASA()
    nasa.get_epic_images() # only use_enhanced=False and use_png=False are working
