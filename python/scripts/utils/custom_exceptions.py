#!/usr/bin/python3

""" Custom exceptions. """
from typing import Union, Any
from pathlib import Path

class InvalidDirectory(Exception):
    """ Invalid path given. Directory does not exist. """
    def __init__(self, directory:Union[str, Path]=None):
        self.dir = directory.absolute() if isinstance(directory, Path) else directory
    def __str__(self):
        err_msg = f'Invalid path given. Directory does not exist.'
        err_msg_dir = f'Invalid path given. Directory does not exist: {self.dir}'
        return err_msg_dir if self.dir is not None else err_msg

class InvalidBoolValue(Exception):
    """ Invalid boolean value given. """
    def __init__(self, v:Any):
        self.v = v
    def __str__(self):
        return f'Unknown boolean value: {self.v}'

class InvalidFile(Exception):
    """ Invalid file given. File either does not exist or is invalid. """
    def __init__(self, f:Union[str, Path]=None):
        self.f = f.absolute().__str__() if isinstance(f, Path) else f
    def __str__(self):
        err_msg = f'Invalid file'
        err_msg += f' {self.f}' if self.f is not None else err_msg
        return err_msg