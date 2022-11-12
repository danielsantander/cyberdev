#!/usr/bin/env python
#!/usr/bin/python3
'''
Unit testing for cipher library within utils.

RUN TESTS:
$ python -m unittest python/scripts/tests/test_exceptions.py

RUN TESTS WITH COVERAGE:
$ python -m coverage run -m unittest python/scripts/tests/test_exceptions.py
$ coverage report
$ coverage annotate -d coverage_files/
'''

import unittest
import os
import sys
import unittest
from pathlib import Path

CURRENT_DIR_NAME = os.path.dirname(os.path.realpath(__file__))
CURRENT_DIR_PATH = Path(CURRENT_DIR_NAME)
PARENT_DIR_NAME = os.path.dirname(CURRENT_DIR_NAME)
# UTILS_DIR = Path(PARENT_DIR_NAME) / 'utils'

sys.path.insert(0, PARENT_DIR_NAME)
from utils import custom_exceptions

class TestInvalidDirectory(unittest.TestCase):
    def setUp(self)->None:
        self.test_dir:Path = CURRENT_DIR_PATH / 'sample_data'


    def test_valid_directory(self):
        self.assertTrue(self.test_dir.exists() and self.test_dir.is_dir())

    def test_invalid_directory(self):
        invalid_directory = CURRENT_DIR_PATH / 'into_the_void'
        self.assertFalse(invalid_directory.exists())
        self.assertFalse(invalid_directory.is_dir())

        def raise_exception():
            raise custom_exceptions.InvalidDirectory(invalid_directory)

        with self.assertRaises(custom_exceptions.InvalidDirectory) as context:
            raise_exception()
        self.assertTrue(str(context.exception).find('Invalid path given. Directory does not exist') != -1)

class TestInvalidBoolValue(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_invalid_boolean(self):
        invalid_boolean = '???'
        def raise_exception():
            raise custom_exceptions.InvalidBoolValue(invalid_boolean)
        with self.assertRaises(custom_exceptions.InvalidBoolValue) as context:
            raise_exception()
        self.assertTrue(str(context.exception).find('Unknown boolean value') != -1)

class TestInvalidFile(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_invalid_file(self):
        invalid_file = CURRENT_DIR_PATH / 'invalid_file.txt'
        self.assertFalse(invalid_file.exists())
        self.assertFalse(invalid_file.is_dir())
        def raise_exception():
            raise custom_exceptions.InvalidFile(invalid_file)
        with self.assertRaises(custom_exceptions.InvalidFile) as context:
            raise_exception()
        self.assertEqual(str(context.exception), f'Invalid file {invalid_file.absolute().__str__()}')

