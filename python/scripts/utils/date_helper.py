#!/usr/bin/env python
#!/usr/bin/python3

""" Unique methods to handle dates and times. """
import datetime
from os import times
import pytz
from pytz.tzinfo import DstTzInfo
from typing import Union

def timestamp_to_date_string(timestamp: int=datetime.datetime.utcnow().timestamp(), str_format: str="%Y%m%d%H%M%S")->str:
    """ Returns datetime string representation of given timestamp with format 'YYYYMMDDHHMMSS'.

    Keyword arguments:
    timestamp -- integer value representing the timestamp to convert (default: datetime.datetime.utcnow().timestamp())
    """
    ts = int(str(timestamp).split(".")[0])
    date = datetime.datetime.fromtimestamp(ts)
    return date.strftime(str_format)

def current_iso_time(tz:Union[str,DstTzInfo]=pytz.timezone('UTC')) -> str:
    """ Return current iso time as str in format YYYY-MM-DDTHH:mm:ssZ

    Keyword arguments:
    tz - timezone (string or DstTzInfo object type)
    """
    try:
        zone = pytz.timezone(tz) if isinstance(tz, str) else tz
    except pytz.exceptions.UnknownTimeZoneError as err:
        return None
    return datetime.datetime.now(tz=zone).isoformat()