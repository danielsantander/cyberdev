#!/usr/bin/python3

""" Custom validation methods. """
from typing import Union
from utils.custom_exceptions import InvalidBoolValue

def str2bool(v:Union[str,bool,int]=None) -> bool:
    """Returns boolean value of given input.
    Keyword arguments:
    v -- value to convert into boolean (required)
    """
    if v is None: return False
    if isinstance(v, bool):
        return v
    elif isinstance(v, int):
        return bool(v)
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise InvalidBoolValue(v)