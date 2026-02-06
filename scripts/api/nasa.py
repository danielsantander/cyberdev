#!/usr/bin/env python
#!/usr/bin/python3

"""
usage: ./nasa.py -a epic
usage: ./nasa.py -a curiosity
"""

import datetime
import json
import logging
import os
import re
import requests
import sys
from pathlib import Path
from api import APIBase
from typing import Optional, Union


DEBUG_MODE = False
VERBOSE_MODE = True
DEFAULT_DURATION_FAST = 2.5
DEFAULT_DURATION = 5.0
NO_INPUT = False
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.abspath(f"{os.path.dirname(CUR_DIR)}/scripts")

sys.path.insert(0, SCRIPTS_DIR)
from utils.constants import DEFAULT_API_SAVE_DIRECTORY, DEFAULT_DATETIME_FMT_SHORT, DEFAULT_DATETIME_FMT_LONG, RE_NASA_IMG_DATES
from utils.custom_logging import create_logger
from utils.file_helper import write_json_to_file
from utils.image_helper import jpg_to_gif
from utils.navigation import make_directory
from utils.validation import str2bool
from utils.webutils import extract_media_from_url

DEFAULT_NASA_SAVE_DIR_PATH = Path(DEFAULT_API_SAVE_DIRECTORY) / 'nasa'

class NASA(APIBase):
    def __init__(self, api_key:str=None, save_dir_path:Path=DEFAULT_NASA_SAVE_DIR_PATH, use_verbose:bool=False):
        super().__init__(save_dir_path=save_dir_path, use_verbose=use_verbose)
        self.api_key = self._verify_api_key(api_key)
        self._logger.debug(f"NASA init complete -- _save_dir_path: {self._save_dir_path.absolute()}")

    def _verify_api_key(self, api_key:str, local_storage:bool=True)->Optional[str]:
        """
        Retrieves NASA api key. Returns key if valid, else None.

        Keyword arguments:
        - api_key (str): api key to use for verification
        - local_storage (bool): save to JSON file in save directory (defaults to True)
        """
        if api_key is None: return None
        resp = self.send_request(url=f"https://api.nasa.gov/planetary/apod?api_key={api_key}", method="GET")
        if resp.ok is False: return None
        data = resp.json()
        filename = self._save_dir_path / f'{self._now_str_short}--verify_api_key_response.json'
        if not filename.exists() and local_storage: write_json_to_file(filename, data)
        return api_key


class EPIC(NASA):
    def __init__(self, **kwargs):
        save_dir_path = kwargs.get('save_dir_path', DEFAULT_NASA_SAVE_DIR_PATH)
        use_verbose = kwargs.get('user_verbose', VERBOSE_MODE)
        super().__init__(save_dir_path=save_dir_path, use_verbose=use_verbose)

        self.base_url = "https://epic.gsfc.nasa.gov"
        self.api_url = f"{self.base_url}/api/"

        # dirs
        self.log_dir: Path = make_directory(self._save_dir_path / 'logs') # nasa/logs/
        self.save_dir_path: Path = make_directory(self._save_dir_path / 'epic')
        self.gif_dir: Path = make_directory(self.save_dir_path / 'gifs')
        self.images_dir: Path = make_directory(self.save_dir_path / 'images')
        self.api_data_dir: Path = make_directory(self.save_dir_path / 'api_data')

        # logger
        log_level = logging.DEBUG if use_verbose else logging.INFO
        self._logger = self._create_logger(log_name='EPIC', log_level=log_level, log_dir=self.log_dir)

        self._logger.debug(f"EPIC init complete -- save_dir_path: {self.save_dir_path.absolute()}")

    def get_epic_images(self, use_enhanced: bool=False, use_png: bool=False)->bool:
        sub_save_dir:Path = None # directory to save this iteration of images
        chunk_size = 256
        isSuccess = False

        # Get image data
        url = f"{self.api_url}enhanced/" if use_enhanced else f"{self.api_url}natural/"
        resp = self.send_request(url=url, method="GET")
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
        overwrite: bool=False
        if file_path.exists() and overwrite is False:
            input_msg = f"Image data file {file_path.name} already exists, overwrite (Y/N)? [N]: "
            raw_input = "N" if NO_INPUT else input(input_msg) or "N"
            overwrite = str2bool(raw_input)
        if file_path.exists() is False or overwrite:
            write_json_to_file(file_path, data_list)

        # iterate data to get images
        success_count = 0
        # print (f"\n\ndata_list ({len(data_list)}):\n{data_list}\n\n") # for debugging
        for idx, data in enumerate(data_list):
            # retrieve image date YYYYMMDD
            m = re.search(RE_NASA_IMG_DATES, data.get('date', ''))
            if m is None:
                self._logger.warning("NO dates found for data, skipping...")
                continue
            year = m.group('year')
            month = m.group('month')
            date = m.group('date')

            # setup save destination
            collection = "enhanced" if use_enhanced else "natural"
            image_type = "png" if use_png else "jpg"
            image_name = data.get('image', '')
            image_filename = f"{str(idx).zfill(2)}_{image_name}--{collection}"
            image_filename += f".{image_type}"
            if sub_save_dir is None: sub_save_dir = make_directory(self.images_dir / str(f"{year}{month}{date}--{collection}"))
            save_dest:Path = sub_save_dir / image_filename
            overwrite = False
            if save_dest.exists() and save_dest.is_file() and save_dest.name.endswith(image_type) and overwrite is False:
                self._logger.warning(f'image file ({save_dest.name}) already exists.')
                input_msg = f"Image file ({save_dest.name}) already exists, overwrite (Y/N)? [N]: "
                raw_input = "N" if NO_INPUT else input(input_msg) or "N"
                overwrite = str2bool(raw_input)
                if overwrite is False: continue

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
                    success_count += 1
                    continue
                else:
                    self.__logger.warning(f'unable to save media {save_dest.name} from {url}, skipping')
                    continue
            except requests.exceptions.HTTPError as err:
                err_msg = err.__str__()
                self._logger.exception(f"error retrieving image ({resp.url}): {err_msg}")
                continue

        isSuccess = bool(len(data_list) == success_count)
        if isSuccess and success_count:
            gif_path = self.gif_dir / f"{sub_save_dir.stem}.gif"
            if gif_path.exists() is False and any(sub_save_dir.iterdir()): jpg_to_gif(sub_save_dir, self.gif_dir, gif_name=f"{gif_path.stem}.gif", duration=DEFAULT_DURATION)
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

    def __init__(self, api_key:str, **kwargs):
        if api_key is None: raise Exception("API Key is required for Curiosity.")
        save_dir_path = kwargs.get('save_dir_path', DEFAULT_NASA_SAVE_DIR_PATH)
        use_verbose = kwargs.get('use_verbose', VERBOSE_MODE)
        super().__init__(api_key=api_key, save_dir_path=save_dir_path, use_verbose=use_verbose)


        self.base_url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"

        # dirs
        self.log_dir: Path = make_directory(self._save_dir_path / 'logs') # nasa/logs/
        self.save_dir_path :Path = make_directory(self._save_dir_path / 'curiosity')
        self.api_dir :Path = make_directory(self.save_dir_path / 'api_data')
        self.images_dir :Path = make_directory(self.save_dir_path / 'images')

        # logger
        log_level = logging.DEBUG if use_verbose else logging.INFO
        self._logger = self._create_logger(log_name='CuriosityAPI', log_level=log_level, log_dir=self.log_dir)
        self._logger.debug(f"Curiosity init complete -- save_dir_path: {self.save_dir_path.absolute()}")

    def get_images(self, query_by:str='sol', params:dict=None):
        """
        Query and save images from NASA Curiosity rover.
        """
        default_params:dict = {'sol': 1000, 'camera': 'all', 'page': 1} if query_by == 'sol' else {'earth_date': self._now.strftime("%Y-%m-%d"), 'camera': 'all', 'page': 1}
        params = params if params else default_params
        params['api_key'] = self.api_key
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
    import argparse
    parser = argparse.ArgumentParser(description="NASA API")
    valid_action_choices = ['epic', 'curiosity']
    parser.add_argument('-a', '--action', dest='action', action='store', choices=valid_action_choices, help="Desired action. Defaults to {0}".format(valid_action_choices[0]), default=valid_action_choices[0])
    parser.add_argument('-d','-v', '--verbose','--debug', dest='debug', action='store_true', default=DEBUG_MODE, help="Debug mode [{0}]".format(DEBUG_MODE))
    parser.add_argument('-k', '--key', dest='api_key', action='store', type=str, help="NASA API Key", required=False)
    parser.add_argument('-f', '--file', dest='file', metavar='FILE_PATH', action='store', type=str, default=DEFAULT_NASA_SAVE_DIR_PATH, help="Directory to save api and media data. Defaults to: {0}".format(DEFAULT_NASA_SAVE_DIR_PATH.name), required=False)
    args = vars(parser.parse_args())
    action = args.get("action")
    api_key = args.get('api_key') or os.environ.get('NASA_API_KEY')
    output_dir = args.get("file")
    debug_mode = DEBUG_MODE or args.get("debug")

    # dates & logger
    now = datetime.datetime.now(datetime.timezone.utc)
    now_str = now.strftime(DEFAULT_DATETIME_FMT_LONG)
    log_level = logging.debug if debug_mode else logging.info
    logger = create_logger(name="NASA", level=logging.DEBUG)
    logger.info("args: {}".format(args))


    # actions
    logger.info(f"performing action: {action}")

    # CURIOSITY
    if action.lower() == 'curiosity':
        # assert api_key exists
        if api_key is None:
            api_key = input("Enter api key: ") or None
        if api_key is None:
            print("API key needed, exiting...")
            sys.exit()

        curiosity = CuriosityAPI(api_key=api_key, save_dir_path=DEFAULT_NASA_SAVE_DIR_PATH)
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

    # EPIC
    elif action.lower() in ['epic']:
        epic = EPIC()
        user_resp = input('Use enhanced images (Y/N)?: ') or 'N'
        use_enhanced: bool = True if user_resp.lower() in ['y', 'yes'] else False
        epic.get_epic_images(use_enhanced=use_enhanced) # only use_enhanced=False and use_png=False are working

    sys.exit()
