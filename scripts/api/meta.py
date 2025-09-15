#!/usr/bin/env python
#!/usr/bin/python3

"""
Retrieve media from Meta's social media Thread posts given URLs.
"""

import logging
import json
import re
import os
import sys
from api import APIBase
from pathlib import Path

API_DIR = os.path.dirname(os.path.abspath(__file__))     # scripts/api
SCRIPTS_DIR = os.path.dirname(API_DIR)
sys.path.insert(0, SCRIPTS_DIR)
from utils.constants import DEFAULT_API_SAVE_DIRECTORY
from utils.custom_logging import create_logger
from utils.webutils import extract_media_from_url

class Threads(APIBase):
    def __init__(self, use_verbose:bool=True):
        self._use_verbose = use_verbose
        log_level = logging.DEBUG if use_verbose else logging.INFO
        log_dir = None  # None for console logging only
        self._logger = self._create_logger(log_name="MetaThreads", log_level=log_level, log_dir=log_dir)
        self._logger.info("Threads init finished.")

    def get_thread_posts(self, url_list:list[str]):
        from selenium.webdriver.chrome.options import Options
        from selenium import webdriver
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By

        if len(url_list) < 1:
            self._logger.error("Need list of URLs, exiting...")
            sys.exit()

        self._logger.info(f"inside get_thread_posts() -- iterating {len(url_list)} threads ...")
        selenium_options = Options()
        selenium_options.add_argument("--headless")  # Add the headless argument

        # Initialize the WebDriver (e.g., Chrome)
        driver = webdriver.Chrome(options=selenium_options) # Or webdriver.Firefox(), etc.

        results = {}
        try:
            for url in url_list:
                username_match = re.search(r'https:\/\/[^@]*@(?P<username>[^\/]*)\/post\/(?P<post_id>[^?\/]*)', url)
                if username_match:
                    username = username_match.group(1)
                    post_id = username_match.group(2)
                else:
                    print(f'skipping url ({url}), no username or post ID ...')
                    continue
                print (f"username--post id: {username}--{post_id}")

                # Navigate to the URL
                driver.get(url)

                # Wait for the video element to be visible and have a 'src' attribute
                # You can use CSS_SELECTOR or XPATH to locate the video element
                video_element = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.TAG_NAME, "video"))
                )
                WebDriverWait(driver, 20).until(
                    lambda driver: video_element.get_attribute("src") is not None and video_element.get_attribute("src") != ""
                )

                time_element = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.TAG_NAME, "time"))
                )
                WebDriverWait(driver, 20).until(
                    lambda driver: time_element.get_attribute("datetime") is not None and time_element.get_attribute("datetime") != ""
                )

                # Get the 'src' attribute
                video_src = video_element.get_attribute("src")
                datetime_str = time_element.get_attribute("datetime").split('.')[0].replace('-', '').replace('T', '').replace(':','')   # 2025-06-28T16:04:25.000Z
                filename = f"{username}--{datetime_str}--{post_id}.mp4"

                save_file_path = Path(f"{DEFAULT_API_SAVE_DIRECTORY}/threads/{filename}")
                if save_file_path.exists():
                    print (f"file ({save_file_path}) already exists, skipping...")
                    continue
                print(f"Video Source: {video_src}")
                print (f"filename: {filename}")
                print (f"save_file: {save_file_path.absolute()}")
                print ("...extracting video from url...")
                extract_media_from_url(url=video_src, save_path=save_file_path)
        finally:
            # Close the browser
            driver.quit()

        return results

if __name__ == '__main__':

    # TODO: get user input for lists -- file and/or single url input
    url_list = []
    thread = Threads()
    results = thread.get_thread_posts(url_list)


# TODO: add unit testing
