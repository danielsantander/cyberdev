#!/usr/bin/python3
'''
Methods to validate booleans.
'''
from typing import Union
from utils.custom_exceptions import InvalidBoolValue

def str2bool(v:Union[str,bool, int]) -> bool:
    ''' Returns boolean value of given input. '''
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