#!/usr/bin/python3

""" Unique methods to handle IO to and from the OS. """
import json
from pathlib import Path
from typing import Union


def open_json_from_file(filepath:Union[str,Path]):
    """ Open JSON from filepath and return as dictionary object. 
    
    Keyword arguments:
    filepath -- JSON filepath to open (required)
    """
    data = {}
    p = filepath if isinstance(filepath, Path) else Path(filepath)
    with open(p) as f:
        data = json.load(f)
    return data

def write_json_to_file(filename:Union[str,Path], dic_obj:dict):
    """ Write dictionary object to file as JSON. 
    
    Keyword arguments:
    filename -- name or path of file to write json to (required)
    dict_obj -- dictionary object to convert into JSON file (required)
    """
    p = filename if isinstance(filename,Path) else Path(filename)
    if not p.exists():
        if p.parent.exists():
            p.touch()
        else:
            p.parent.mkdir()
            p.touch()
    with open(p.absolute(), "w") as f:
        # json.dump(dict, f, indent=2)
        f.write(json.dumps(dic_obj, indent=2))
