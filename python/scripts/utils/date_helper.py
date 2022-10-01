#!/usr/bin/python3

""" Unique methods to handle dates and times. """
import datetime
from os import times
import pytz
from pytz.tzinfo import DstTzInfo

def timestamp_to_date_string(timestamp:int=datetime.datetime.utcnow().timestamp(), str_format:str="%Y%m%d%H%M%S") -> str:
    """ Returns datetime string representation of given timestamp with format 'YYYYMMDDHHMMSS'.

    Keyword arguments:
    timestamp -- integer value representing the timestamp to convert (default datetime utcnow timestamp)
    """
    ts = int(str(timestamp).split(".")[0])
    date = datetime.datetime.fromtimestamp(ts)
    return date.strftime(str_format)

def current_iso_time(tz:DstTzInfo=pytz.timezone('UTC')) -> str:
    """ Return current iso time as str in format YYYY-MM-DDTHH:mm:ssZ """
    return datetime.datetime.now(tz=tz).isoformat()