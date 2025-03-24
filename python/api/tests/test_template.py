#!/usr/bin/env python
#!/usr/bin/python3

import datetime
import os
import sys
import unittest
from pathlib import Path

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

class TestTemplate(unittest.TestCase):
    _test_dir = Path(TEST_DIR)

    def setUp(self):
        self.now = datetime.datetime.utcnow()
        return

    def tearDown(self):
        if self._test_dir.exists() and self._test_dir.is_dir():
            clean_dir(self._test_dir)
        return
