#!/usr/bin/env python
#!/usr/bin/python3

import datetime
import re
import sys
import unittest
from unittest import mock
from pathlib import Path
from test_template import TestTemplate, clean_dir, API_DIR, MockResponse

sys.path.insert(0, API_DIR)
from nasa import NASA, EPIC, CuriosityAPI

MOCK_IMG_DATA = [
    {
        "identifier": "20250417000830",
        "caption": "This image was taken by NASA's EPIC camera onboard the NOAA DSCOVR spacecraft",
        "image": "epic_RGB_20250417000830",
        "version": "03",
        "centroid_coordinates": {},
        "dscovr_j2000_position": {},
        "lunar_j2000_position": {},
        "sun_j2000_position": {},
        "attitude_quaternions": {},
        "date": "2025-04-17 00:03:42",
        "coords": {
            "centroid_coordinates": {},
            "dscovr_j2000_position": {},
            "lunar_j2000_position": {},
            "sun_j2000_position": {},
            "attitude_quaternions": {}
        }
    }
]

def mocked_requests_get(*args, **kwargs):
    # print(f"\n\nINSIDE mocked_requests_get -- args:{args};kwargs:{kwargs}")
    url = args[0] if len(args) else kwargs.get('url')
    content_type = kwargs.get('Content-type')
    params = kwargs.get('params', {})

    if search_results := re.search('^https://epic.gsfc.nasa.gov/api/(?P<image_type>[^\/]+)\/?$', url): # image_type: [natural, enhanced]
        image_type = search_results.groupdict().get('image_type')
        return MockResponse(json_data=MOCK_IMG_DATA, status_code=200, url=url)

    elif search_results := re.search('^https://epic.gsfc.nasa.gov/archive/(?P<image_type>[^\/]+)\/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<img_ext>\w{3})/(?P<img_name>[^\.]+)\.jpg', url):
        image_type = search_results.groupdict().get('image_type')
        year = search_results.groupdict().get('year')
        month = search_results.groupdict().get('month')
        day = search_results.groupdict().get('day')
        img_ext = search_results.groupdict().get('img_ext')
        img_name = search_results.groupdict().get('img_name')
        return MockResponse(json_data={}, status_code=200, url=url)

    # NASA validate api key
    elif search_results := re.search('^https:\/\/api\.nasa\.gov\/planetary\/apod\?api_key=(?P<api_key>.*)$', url):
        api_key = search_results.groupdict().get('api_key')
        data = {
            "date": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d'), # "2025-04-19",
            "explanation": "In digital brush strokes, Jupiter's signature atmospheric bands and vortices were used to form this interplanetary post-impressionist work of art. The creative image from citizen scientist Rick Lundh uses data from the Juno spacecraft's JunoCam. To paint on the digital canvas, a JunoCam image with contrasting light and dark tones was chosen for processing and an oil-painting software filter applied. The image data was captured during perijove 10. That was Juno's December 16, 2017 close encounter with the solar system's ruling gas giant. At the time the spacecraft was cruising about 13,000 kilometers above northern Jovian cloud tops. Now in an extended mission, Juno has explored Jupiter and its moons since entering orbit around Jupiter in July of 2016.",
            "hdurl": "https://apod.nasa.gov/apod/image/2504/PIA21983JupiterLundh.jpg",
            "media_type": "image",
            "service_version": "v1",
            "title": "Painting with Jupiter",
            "url": "https://apod.nasa.gov/apod/image/2504/PIA21983JupiterLundh1024.jpg"
        }
        return MockResponse(json_data=data, status_code=200, url=url)

    # curiosity get_images()
    # https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos
    elif search_results := re.search('https:\/\/api.nasa.gov\/mars-photos\/api\/v1\/rovers\/curiosity\/photos', url):
        return MockResponse(json_data={"photos": []}, status_code=200, url=url)

    print(f"UNKNOWN URL: {url}")
    return MockResponse(status_code=400)

class TestNASA(TestTemplate):
    def setUp(self)->None:
        super.setUp()
        self.test_dir = self._test_dir / 'TestNASA'
        if not self.test_dir.exists(): self.test_dir.mkdir(parents=True, exist_ok=True)
        self.nasa = NASA(save_dir_path=self.test_dir)

    def tearDown(self) -> None:
        super().tearDown()


class TestEpic(TestTemplate):
    def setUp(self):
        self.test_dir = self._test_dir / 'TestEpic'
        self.epic = EPIC(save_dir_path=self.test_dir)

    def test_init(self):
        epic_dir: Path = self.test_dir / 'epic'
        data_dir:  Path = epic_dir / 'api_data'
        gif_dir: Path = epic_dir / 'gifs'
        images_dir: Path = epic_dir / 'images'
        self.assertTrue(epic_dir.exists() and epic_dir.is_dir())
        self.assertTrue(data_dir.exists() and data_dir.is_dir())
        self.assertTrue(gif_dir.exists() and gif_dir.is_dir())
        self.assertTrue(images_dir.exists() and images_dir.is_dir())

    @mock.patch('requests.Session.get', side_effect=mocked_requests_get)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_epic_images(self, mock_session_get, mock_get):
        results = self.epic.get_epic_images()
        self.assertTrue(results)

    def tearDown(self):
        super().tearDown()

class TestCuriosity(TestTemplate):
    def setUp(self, ):
        self.test_dir = self._test_dir / 'TestCuriosity'
        self.api_key = 'FAKE_API_KEY'

    @mock.patch('requests.Session.get', side_effect=mocked_requests_get)
    def test_init(self, mock_session_get):
        curiosity = CuriosityAPI(api_key=self.api_key, save_dir_path=self.test_dir, use_verbose=False)
        curiosity_dir: Path = self.test_dir / 'curiosity'
        data_dir:  Path = curiosity_dir / 'api_data'
        images_dir: Path = curiosity_dir / 'images'
        self.assertTrue(curiosity_dir.exists() and curiosity_dir.is_dir())
        self.assertTrue(data_dir.exists() and data_dir.is_dir())
        self.assertTrue(images_dir.exists() and images_dir.is_dir())

    @mock.patch('requests.Session.get', side_effect=mocked_requests_get)
    def test_get_images_earth(self, mock_get):
        curiosity = CuriosityAPI(api_key=self.api_key, save_dir_path=self.test_dir, use_verbose=False)
        params = {"earth_date": self._now.strftime('%Y-%m-%d')}
        results = curiosity.get_images(query_by='earth', params=params)

    @mock.patch('requests.Session.get', side_effect=mocked_requests_get)
    def test_get_images_sol(self, mock_get):
        curiosity = CuriosityAPI(api_key=self.api_key, save_dir_path=self.test_dir, use_verbose=False)
        params = {"sol": 1000 }
        curiosity.get_images(query_by='sol', params=params)

    @mock.patch('requests.Session.get', side_effect=mocked_requests_get)
    def test_process_data(self, mock_get):
        curiosity = CuriosityAPI(api_key=self.api_key, save_dir_path=self.test_dir, use_verbose=False)
        image_data = {"photos": []}
        filename = f"{self._now.strftime('%Y%m%d%H%M%S') }--curiosity.json"
        results = curiosity.process_data(data=image_data, filename=filename)
        # TODO: handle `extract_media_from_url()` when called from `process_data()` -- when adding data in image_data

    def tearDown(self) -> None:
        return super().tearDown()

if __name__ == '__main__':
    unittest.main()
