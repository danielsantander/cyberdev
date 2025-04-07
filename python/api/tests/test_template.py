#!/usr/bin/env python
#!/usr/bin/python3

import datetime
import json
import os
import sys
import unittest
from pathlib import Path
from typing import Union

TEST_DIR = os.path.dirname(os.path.realpath(__file__))   # current directory
API_DIR = os.path.dirname(TEST_DIR)                      # parent directory
sys.path.insert(0, API_DIR)

def clean_dir(directory:Path):
    assert directory.exists() and directory.is_dir()
    for x in directory.iterdir():
        if x.is_file(): x.unlink()
        elif x.is_dir(): clean_dir(x)
    directory.rmdir()
    return

def write_json_to_file(filename:Union[str,Path], data:dict):
    """
    Write dictionary object to file as JSON.

    Keyword arguments:
    filename -- name or path of file to write json to (required)
    dict_obj -- dictionary object to convert into JSON file (required)
    """
    p = filename if isinstance(filename,Path) else Path(filename)
    if not p.parent.exists(): p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists(): p.touch()
    p = p if str(p.name).endswith('.json') else p.parent/f"{p.stem}.json"

    with open(p.absolute(), "w") as f:
        # json.dump(data, f, indent=2)  # should work as well
        f.write(json.dumps(data, indent=2))

class TestTemplate(unittest.TestCase):
    _test_dir = Path(TEST_DIR)
    _test_dir.mkdir(parents=True, exist_ok=True)
    _now = datetime.datetime.now(datetime.timezone.utc)

    def setUp(self):
        return

    def tearDown(self):
        if self._test_dir.exists() and self._test_dir.is_dir():
            clean_dir(self._test_dir)
        return
