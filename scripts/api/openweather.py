#!/usr/bin/env python3
#!/usr/bin/python3

import json
import logging
import os
from api import APIBase
from pathlib import Path
from utils.constants import DEFAULT_API_SAVE_DIRECTORY
from utils.custom_logging import create_logger

DEFAULT_OW_SAVE_DIR = Path(DEFAULT_API_SAVE_DIRECTORY) / 'OpenWeather'
DEFAULT_LOG_DIR = DEFAULT_OW_SAVE_DIR / 'logs'
_LOGGER = create_logger('WeatherAPI',level=logging.DEBUG, log_dir=DEFAULT_LOG_DIR)

class WeatherAPI(APIBase):
    def __init__(self, api_key:str=None, save_dir_path:Path=DEFAULT_OW_SAVE_DIR, use_verbose:bool=False, **kwargs) -> None:
        super().__init__(save_dir_path=save_dir_path, logger=_LOGGER, use_verbose=use_verbose)
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.default_mode = None    # xml, html -> default is json (None)
        self.default_unit = 'metric'  # standard, metric, imperial
        self._logger.debug(f"WeatherAPI init complete -- _save_dir_path: {self._save_dir_path.absolute()}")
        """
        OpenWeather API Free Plan:
            - Hourly forecast: unavailable
            - Daily forecast: unavailable
            - Calls per minute: 60
            - 3 hour forecast: 5 days
        """

    def current_weather(self, **kwargs) -> dict:
        """
        Get current weather data for a specified city.

        Keyword arguments:
        city_name -- Name of the city to get weather data for.
        units -- Units of measurement. 'metric' for Celsius, 'imperial' for Fahrenheit. (default 'imperial')
        """

        endpoint = f"{self.base_url}/weather"
        params = {
            'appid': self.api_key,
            'units': kwargs.get('units', self.default_unit),
        }
        # if None, default is json
        if self.default_mode is not None:
            params['mode'] = self.default_mode

        if city_id := kwargs.get('id'):
            if isinstance(city_id, int) or isinstance(city_id, str):
                city_id = str(city_id)
            elif isinstance(city_id, list):
                city_id = ','.join([str(x) for x in city_id])
            else:
                raise ValueError("'id' must be an int, str, or list of ints/strs.")
            params['id'] = city_id
        elif city_name:= kwargs.get('city'):
            params['q'] = city_name
            if state_code := kwargs.get('state`'):
                params['q'] = f"{city_name},{state_code}"
                if country_code := kwargs.get('country'):
                    params['q'] = f"{city_name},{state_code},{country_code}"

        # geocoordinates
        elif kwargs.get('lat') and kwargs.get('lon'):
            params['lat'] = kwargs.get('lat')
            params['lon'] = kwargs.get('lon')

        # zipcode
        elif kwargs.get('zip'):
            params['zip'] = kwargs.get('zip')
        else:
            raise ValueError("Either 'city' or 'id', or 'zip', or 'lon/lat' must be provided.")
        response = self.send_request(endpoint, method='GET', params=params)
        return response

    def current_weather_bound_box(self, x1:int, x2:int, y1:int, y2:int, zoom:int, units:str='imperial') -> dict:
        """
        Get current weather data for a bounding box.

        Keyword arguments:
        x1, x2 -- Longitude of the bounding box corners.
        y1, y2 -- Latitude of the bounding box corners.
        zoom -- Number of cities to return within the bounding box.
        units -- Units of measurement. 'metric' for Celsius, 'imperial' for Fahrenheit. (default 'imperial')
        """

        endpoint = f"{self.base_url}/box/city"
        params = {
            'bbox': f"{x1},{y1},{x2},{y2},{zoom}",
            'appid': self.api_key,
            'units': units
        }
        response = self.send_request(endpoint, method='GET', params=params)
        return response


    def setup_params(self, in_params:dict={}) -> dict:
        # if None, default is json
        params = {}
        if self.default_mode is not None:
            params['mode'] = self.default_mode

        if city_id := in_params.get('id'):
            if isinstance(city_id, int) or isinstance(city_id, str):
                city_id = str(city_id)
            elif isinstance(city_id, list):
                city_id = ','.join([str(x) for x in city_id])
            else:
                raise ValueError("'id' must be an int, str, or list of ints/strs.")
            params['id'] = city_id
        elif city_name:= in_params.get('city'):
            params['q'] = city_name
            if state_code := in_params.get('state`'):
                params['q'] = f"{city_name},{state_code}"
                if country_code := in_params.get('country'):
                    params['q'] = f"{city_name},{state_code},{country_code}"

        # geocoordinates
        elif in_params.get('lat') and in_params.get('lon'):
            params['lat'] = in_params.get('lat')
            params['lon'] = in_params.get('lon')

        # zipcode
        elif in_params.get('zip'):
            params['zip'] = in_params.get('zip')
        else:
            raise ValueError("Either 'city' or 'id', or 'zip', or 'lon/lat' must be provided.")
        params['units'] = in_params.get('units', self.default_unit)
        params['appid'] = self.api_key
        return params


    def get_hourly_forecast(self, **kwargs) -> dict:
        """
        Get hourly weather forecast for a specified city.
        # UPDATE: Hourly forecast: unavailable for free users
        # UPDATE: Daily forecast: unavailable for free users
        """
        endpoint = f"{self.base_url}/forecast/hourly"
        params = self.setup_params(kwargs)
        response = self.send_request(endpoint, method='GET', params=params)
        return response

    def get_forecast(self, **kwargs) -> dict:
        """
        Get weather forecast for a specified city.
        """
        endpoint = f"{self.base_url}/forecast"
        params = self.setup_params(kwargs)
        response = self.send_request(endpoint, method='GET', params=params)
        return response

    def get_air_pollution(self, lat:float, lon:float, start:int=None, end:int=None) -> dict:
        """
        Get air pollution data for specified coordinates.
        Keyword arguments:
        lat -- Latitude of the location.
        lon -- Longitude of the location.
        start -- Start timestamp (optional). e.g.: start=1606488670
        end -- End timestamp (optional).    e.g.: end=1606747870
        Returns:
        dict -- Air pollution data.
        """
        endpoint = f"{self.base_url}/air_pollution"
        params = {
            'lat': lat,
            'lon': lon,
        }
        if start is not None and end is not None:
            params['start'] = start
            params['end'] = end
        params['appid'] = self.api_key
        response = self.send_request(endpoint, method='GET', params=params)
        return response

if __name__ == '__main__':
    weather = WeatherAPI(api_key=os.environ.get('OPEN_WEATHER_API'), use_verbose=True)
    # data = weather.current_weather("Los Angeles", state_code="CA", country_code="US")
    # data = weather.current_weather(city="Tucson", state_code="AZ", country_code="US")
    # data = weather.current_weather_bound_box(12,32,15,37,10)                              # BROKEN
    # data = weather.get_hourly_forecast(city="Tucson", state_code="AZ", country_code="US") # BROKEN
    # data = weather.get_forecast(city="Tucson", state_code="AZ", country_code="US")
    data = weather.get_air_pollution(lat=32.2217, lon=-110.9265)    # Tucson, AZ
    print (json.dumps(data.json(), indent=2))
