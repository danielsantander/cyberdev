#!/usr/bin/env python
#!/usr/bin/python3

"""
usage: ./nasa.py epic
usage: ./nasa.py curiosity
"""

import datetime
import json
import logging
import os
import re
import requests
import sys
from pathlib import Path
from typing import Union, Optional

# TODO:
# - Allow NASA class to inherit from APIBase (inherit session and request methods)
# - Remove inheritance from EPIC & CuriosityAPI classes in order to begin using APIBase, instead
# - use argparse to get more use input
    # - gif duration for EPIC images
    # - save directory location
    # - use file log rotation


DEBUG_MODE = False
DEFAULT_DURATION = 2.5
NO_INPUT = False
CUR_DIR = os.path.dirname(os.path.abspath(__file__))     # ./python/api
DEFAULT_NASA_SAVE_DIR = Path(CUR_DIR) / 'api_data' / 'nasa'
SCRIPTS_DIR = os.path.abspath(f"{os.path.dirname(CUR_DIR)}/scripts")   # ./python/scripts

sys.path.insert(0, SCRIPTS_DIR)
from utils.constants import DEFAULT_DATETIME_FMT_SHORT, DEFAULT_DATETIME_FMT_LONG, RE_NASA_IMG_DATES
from utils.custom_logging import create_console_logger, create_logger
from utils.file_helper import write_json_to_file
from utils.image_helper import jpg_to_gif
from utils.navigation import make_directory
from utils.validation import str2bool
from utils.webutils import extract_media_from_url


class NASA:
    def __init__(self, api_key:str, save_dir:Path=DEFAULT_NASA_SAVE_DIR, verbose_mode:bool=False, logger:logging.Logger=None):
        self._save_dir = self._verify_or_get_save_directory(dir_path=save_dir)
        self.session = requests.session()
        self._now = datetime.datetime.utcnow()
        self._now_str_long = self._now.strftime(DEFAULT_DATETIME_FMT_LONG)   # %Y%m%d%H%M%S
        self._now_str_short = self._now.strftime(DEFAULT_DATETIME_FMT_SHORT) # '%Y%m%d'
        self._logger = logger if logger else create_logger(name="NASA", level=logging.DEBUG, log_dir=self._save_dir/'logs')
        self.api_key = self._verify_api_key(api_key) if api_key is not None else None
        self._logger.info(f"NASA init complete, using _save_dir: {self._save_dir.absolute()}")

    def _verify_or_get_save_directory(self, dir_path:Path):
        """
        Verifies the given dir_path is a valid directory.
        Returns path if valid, else returns current directory.
        """
        default_dir = Path(os.path.abspath(os.path.dirname(__file__)))
        if dir_path is None: return default_dir
        if dir_path.exists() and dir_path.is_dir(): return dir_path
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path

    def _verify_api_key(self, api_key:str, local_storage:bool=True):
        """
        Retrieves NASA api token based on provided api key. Returns api_key if valid, else None.

        Keyword arguments:
        - api_key (str): api key to use for verification
        - local_storage (bool): save to JSOn file in save directory (defaults to True)
        """
        url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
        resp = self.send_request(url=url)
        if resp.ok:
            data = resp.json()
            filename = self._save_dir / f'{self._now_str_short}--verify_api_key_response.json'
            write_json_to_file(filename, data)
            return api_key
        return None

    def send_request(self, url:str, params:dict={}, headers:Optional[dict]=None, method:str="GET", **kwargs):
        try:
            self._logger.debug(f"sending {method} request to \'{url}\' with params: {params}")
            if method == "GET":
                resp = self.session.get(url, params=params)
            else:
                # TODO: implement other methods if needed
                self._logger.error(f"need to implement {method} method for sending requests")
                return None
            self._logger.debug(f"send_request resp ({resp.status_code}): {resp.url}")
            resp.raise_for_status()
        except Exception as err:
            self._logger.error(f"send_request error ({resp.status_code}) to \'{resp.url}\': {err.__str__()}")
            return resp
        return resp

class EPIC(NASA):
    def __init__(self, logger:logging.Logger=None, **kwargs)->None:
        api_key = kwargs.get('api_key')
        save_dir = kwargs.get('save_dir', DEFAULT_NASA_SAVE_DIR)
        verbose_mode = kwargs.get('verbose_mode', False)
        super().__init__(api_key=api_key, save_dir=save_dir, verbose_mode=verbose_mode, logger=logger)
        self._logger.name = 'EPIC'

        self.base_url = "https://epic.gsfc.nasa.gov"
        self.api_url = f"{self.base_url}/api/"

        # dirs
        self.save_dir :Path = make_directory(self._save_dir / 'epic')
        self.gif_dir :Path = make_directory(self.save_dir / 'gifs')
        self.images_dir :Path = make_directory(self.save_dir / 'images')
        self.api_data_dir :Path = make_directory(self.save_dir / 'api_data')

        self._logger.info(f"EPIC init complete -- save_dir: {self.save_dir.absolute()}")

    def get_epic_images(self, use_enhanced: bool=False, use_png: bool=False):
        sub_save_dir:Path = None # directory to save this iteration of images
        chunk_size = 256
        isSuccess = True

        # Get image data
        url = f"{self.api_url}enhanced/" if use_enhanced else f"{self.api_url}natural/"
        resp = requests.get(url)
        assert resp.ok and resp.status_code == 200
        self._logger.debug(f"media extraction request ({resp.status_code}) -- {resp.url}")
        data_list = resp.json()

        # save data
        if len(data_list) == 0:
            self._logger.info("No data retrieved, exiting.")
            return
        identifier_date = datetime.datetime.strptime(data_list[0].get('identifier'), DEFAULT_DATETIME_FMT_LONG).strftime(DEFAULT_DATETIME_FMT_SHORT)
        file_path:Path = self.api_data_dir / f'{identifier_date}.json'
        proceed = True
        if file_path.exists():
            input_msg = f"Image data file {file_path.name} already exists, overwrite (Y/N)? [N]: "
            raw_input = "N" if NO_INPUT else input(input_msg) or "N"
            proceed = str2bool(raw_input)
        if file_path.exists() is False or proceed:
            write_json_to_file(file_path, data_list)

        # iterate data to get images
        for idx, data in enumerate(data_list):
            # retrieve image date YYYYMMDD
            m = re.search(RE_NASA_IMG_DATES, data.get('date', ''))
            if m is None:
                self._logger.warning("NO dates found for data, skipping...")
                continue
            year = m.group('year')
            month = m.group('month')
            date = m.group('date')
            if sub_save_dir is None: sub_save_dir = make_directory(self.images_dir / str(f"{year}{month}{date}"))

            # setup save destination
            collection = "enhanced" if use_enhanced else "natural"
            image_type = "png" if use_png else "jpg"
            image_name = data.get('image', '')
            image_filename = f"{str(idx).zfill(2)}_{image_name}--{collection}"
            image_filename += f".{image_type}"
            save_dest:Path = sub_save_dir / image_filename
            if save_dest.exists() and save_dest.is_file() and save_dest.name.endswith(image_type):
                self._logger.warning(f'image file ({save_dest.name}) already exists.')
                input_msg = f"Image file ({save_dest.name}) already exists, overwrite (Y/N)? [N]: "
                raw_input = "N" if NO_INPUT else input(input_msg) or "N"
                proceed = str2bool(raw_input)
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
            gif_filename = f"{sub_save_dir.stem}--enhanced.gif" if use_enhanced else f"{sub_save_dir.stem}--natural.gif"
            gif_path = self.gif_dir / gif_filename
            duration = None  # TODO: retrieve input from user for duration?
            if duration is None:
                duration = DEFAULT_DURATION
            if gif_path.exists() is False: jpg_to_gif(sub_save_dir, self.gif_dir, gif_name=f"{gif_path.stem}.gif", duration=duration)

        return isSuccess

class CuriosityAPI(NASA):
    # https://api.nasa.gov/
    """ Example queries:
    https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key=DEMO_KEY

    https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&camera=fhaz&api_key=DEMO_KEY

    https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&page=2&api_key=DEMO_KEY

    Query by Martian Sol
    -----------------------

    | Param   | Type | Default  | Desc                                         |
    |---------|------|----------|----------------------------------------------|
    | sol     | int  | none     | sol (ranges from 0 to max found in endpoint) |
    | camera  | str  | all      | see table above for abbreviations            |
    | page    | int  | 1        | 25 items per page returned by                |
    | api_key | str  | DEMO_KEY | api.nasa.gov.key for expanded usage          |
    """

    def __init__(self, api_key:str, logger:logging.Logger, **kwargs):
        if api_key is None: raise Exception("API Key is required for Curiosity.")
        api_key = api_key
        save_dir = kwargs.get('save_dir')
        verbose_mode = kwargs.get('verbose_mode', False)
        super().__init__(api_key=api_key, save_dir=save_dir, verbose_mode=verbose_mode, logger=logger)
        self._logger.name = 'CuriosityAPI'

        self.base_url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"

        # dirs
        self.save_dir :Path = make_directory(self._save_dir / 'curiosity')
        self.api_dir :Path = make_directory(self.save_dir / 'api_data')
        self.images_dir :Path = make_directory(self.save_dir / 'images')\

        self._logger.info(f"Curiosity init complete -- save_dir: {self.save_dir.absolute()}")

    def get_images(self, query_by:str='sol', params:dict=None):
        """Query and save images from NASA Curiosity rover."""
        default_params = {'sol': 1000, 'camera': 'all', 'page': 1} if query_by == 'sol' else {'earth_date': self._now.strftime("%Y-%m-%d"), 'camera': 'all', 'page': 1}

        params = default_params if params is None else params
        params['api_key']  = self.api_key
        resp = self.send_request(url=self.base_url, params=params)

        filename = f"{self._now_str_long}--curiosity"
        if params.get('earth_date'): filename += f"--earth_date--{params.get('earth_date')}"
        filename += ".json"
        self.process_data(resp.json(), filename)
        return

    def process_data(self, data:dict, filename:str):
        """
        Process API response data and save both JSON & images files.
        Iterate through data to retrieve and save photos from their image source url.

        Files are (formatted and) saved in the following directory:
        "sol_{sol_date}/sol_{sol_date}_{image_id}_{earth_date}_{camera_name}.jpg"

        """
        # write data to file
        num_photos = len(data.get('photos', []))
        if not num_photos:
            self._logger.warning("no photo data returned, will not create save file.")
            return
        self._logger.debug(f'processing {num_photos} photos')

        # write api data to file
        filename = filename if filename.endswith('.json') else f"{filename}.json"
        api_data_file :Path = self.api_dir / filename
        self._logger.info(f"writing response JSON to file: {api_data_file.absolute()}")
        write_json_to_file(api_data_file, data)

        # generate media file to save photos to
        sol = data.get('photos', [])[-1].get('sol')
        img_save_dir = self.images_dir / f"sol_{sol}"
        if img_save_dir.exists():
            user_resp = input(f"Images for sol {sol} already exist, would you like to overwrite them (Y/N)? ") or "N"
            if user_resp.lower() in ['y', 'yes']:
                self._logger.warning(f"overwriting curiosity images for sol {sol}")
            else:
                self._logger.info(f"photos for sol {sol} already exist, exiting...")
                return
        else:
            img_save_dir.mkdir(parents=True, exist_ok=True)

        # iterate photos
        self._logger.info(f"iterating through {len(data.get('photos', []))} photo entries")
        for photo in data.get('photos', []):
            img_id = photo.get('id')
            img_sol = photo.get('sol')
            img_src = photo.get('img_src')
            img_earth_date = photo.get('earth_date').replace("-", "")    # YYYY-MM-DD -> YYYYMMDD
            camera_name = photo.get('camera', {}).get('name')

            img_ext = img_src.split(".")[-1].lower() or "jpg"
            img_filename = img_save_dir / f"sol_{img_sol}_{img_id}_{img_earth_date}_{camera_name}.{img_ext}"
            is_extracted, file_stat_info = extract_media_from_url(url=img_src, save_path=img_filename, lgr=self._logger)
        return


if __name__ == '__main__':

    # args
    valid_actions = ['curiosity', 'epic']
    num_args = len(sys.argv)
    if num_args < 2:
        print (f"\tUsage: ./{__file__.split('/')[-1]} [data]\n\tExample: ./{__file__.split('/')[-1]} epic\n")
        sys.exit()
    action = sys.argv[1]
    api_key:str = sys.argv[2] if len(sys.argv) >= 3 else os.environ.get('NASA_API_KEY')

    now = datetime.datetime.utcnow()
    now_str = now.strftime(DEFAULT_DATETIME_FMT_LONG)

    logger = create_console_logger(name="NASA", level=logging.DEBUG)

    # actions
    logger.info(f"performing action: {action}")
    if action.lower() in ['mars', 'mars_rover', 'marsrover', 'mars_rover', 'curiosity']:

        # assert api_key exists
        if api_key is None:
            api_key = input("Enter api key: ") or None
        if api_key is None:
            print("Need api key, exiting...")
            sys.exit()

        curiosity = CuriosityAPI(api_key, logger, save_dir=DEFAULT_NASA_SAVE_DIR)
        query = input('Query by \'martian_sol\' or \'earth_date\': ').lower() or 'earth_date'
        if query not in ['martian_sol', 'earth_date', 'earth', 'sol']:
            raise BaseException("Invalid query input: {0}".format(query))
        if 'earth' in query:
            now_str = now.strftime('%Y-%m-%d')
            earth_date = input('Enter Earth date ({0}): '.format(now_str)) or now_str
            logger.debug(f"using earth_date: {earth_date}")
            if earth_date is None: raise BaseException("Invalid Input")
            params = {'earth_date': earth_date}
            curiosity.get_images(query_by='earth', params=params)
        else:
            sol_date = input('Enter Sol date [1000]: ') or 1000
            logger.debug(f"using sol_date: {sol_date}")
            params = {'sol': sol_date}
            curiosity.get_images(query_by='sol', params=params)
        sys.exit()

    # epic & default:
    elif action.lower() in ['epic']:
        epic = EPIC(logger=logger)
        user_resp = input('Use enhanced images (Y/N)?: ') or 'N'
        use_enhanced: bool = True if user_resp.lower() in ['y', 'yes'] else False
        epic.get_epic_images(use_enhanced=use_enhanced) # only use_enhanced=False and use_png=False are working
    else:
        print (f"unknown action, valid choices are: {valid_actions}")
    sys.exit()
