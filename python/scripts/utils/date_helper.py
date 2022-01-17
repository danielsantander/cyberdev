#!/usr/bin/python3
'''
Unique methods to handle dates and times.
'''
import datetime
import pytz
from pytz.tzinfo import DstTzInfo

def timestamp_to_date_string(timestamp:int) -> str:
    ''' Takes epoch timestamp (integer value) and converts into date string format YYYYMMDDHHMMSS (year month date hour min sec)  '''
    timestamp = int(str(timestamp).split(".")[0])
    date = datetime.datetime.fromtimestamp(timestamp)
    return date.strftime("%Y%m%d%H%M%S")

def current_iso_time(tz:DstTzInfo=pytz.timezone('UTC')) -> str:
    ''' Return current iso time as str in format YYYY-MM-DDTHH:mm:ssZ '''
    return datetime.datetime.now(tz=tz).isoformat()