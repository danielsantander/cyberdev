#!/usr/bin/python3
import unittest


import datetime
import unittest
import os
import re
import sys
from pathlib import Path

TEST_DIR_PATH = Path(os.path.dirname(os.path.realpath(__file__)))

class TestBase(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self._now = datetime.datetime.now(datetime.timezone.utc)
        self._cur_dir_path: Path = TEST_DIR_PATH

    def setUp(self) -> None:
        return

    def tearDown(self):
        return
