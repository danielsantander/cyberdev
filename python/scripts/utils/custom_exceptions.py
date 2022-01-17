#!/usr/bin/python3
'''
Custome exceptions.
'''
from typing import Union, Any
from pathlib import Path

class InvalidDirectory(Exception):
    ''' Invalid path given. Directory does not exist. '''
    def __init__(self, directory:Union[str, Path]):
        self.dir = directory
    def __str__(self):
        return f'Invalid path given. Directory does not exist: {self.dir}'

class InvalidBoolValue(Exception):
    ''' Invalid boolean value given. '''
    def __init__(self, v:Any):
        self.v = v
    def __str__(self):
        return f'Unknown boolean value.t: {self.v}'