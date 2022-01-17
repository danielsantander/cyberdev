#!/usr/bin/python3
'''
Unique methods to handle IO into the OS.
'''
import json
from pathlib import Path
from typing import Union


def open_json_from_file(filename:Union[str,Path]):
    '''
    Open and return JSON from given filename.
    '''
    data = {}
    p = filename if isinstance(filename, Path) else Path(filename)
    with open(p) as json_file:
        data = json.load(json_file)
    return data

def write_json_to_file(filename:Union[str,Path], json_file:dict):
    '''
    Write json_file to given filepath.
    '''
    p = filename if isinstance(filename,Path) else Path(filename)
    if not p.exists():
        if p.parent.exists():
            p.touch()
        else:
            p.parent.mkdir()
            p.touch()
    with open(p.absolute(), "w") as f:
        f.write(json.dumps(json_file, indent=4))
