#!/usr/bin/python3
'''
Unique methods to handle dates and times.
'''
import datetime
from os import times
import pytz
from pytz.tzinfo import DstTzInfo

def timestamp_to_date_string(timestamp:int=None) -> str:
    ''' Takes epoch timestamp (integer value) and converts into date string format YYYYMMDDHHMMSS (year month date hour min sec)  '''
    timestamp = timestamp if timestamp else datetime.datetime.utcnow().timestamp()
    ts = int(str(timestamp).split(".")[0])
    date = datetime.datetime.fromtimestamp(ts)
    return date.strftime("%Y%m%d%H%M%S")

def current_iso_time(tz:DstTzInfo=pytz.timezone('UTC')) -> str:
    ''' Return current iso time as str in format YYYY-MM-DDTHH:mm:ssZ '''
    return datetime.datetime.now(tz=tz).isoformat()