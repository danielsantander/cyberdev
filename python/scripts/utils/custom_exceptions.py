#!/usr/bin/python3
'''
Custome exceptions.
'''
from typing import Union, Any
from pathlib import Path

class InvalidDirectory(Exception):
    ''' Invalid path given. Directory does not exist. '''
    def __init__(self, directory:Union[str, Path]=None):
        self.dir = directory
    def __str__(self):
        err_msg = f'Invalid path given. Directory does not exist.'
        err_msg_dir = f'Invalid path given. Directory does not exist: {self.dir}'
        return err_msg_dir if self.dir is not None else err_msg

class InvalidBoolValue(Exception):
    ''' Invalid boolean value given. '''
    def __init__(self, v:Any):
        self.v = v
    def __str__(self):
        return f'Unknown boolean value.t: {self.v}'