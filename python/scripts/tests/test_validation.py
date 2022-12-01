#!/usr/bin/python3
'''
Unit testing for validation library.

RUN:
$ python3 -m coverage run --source="." -m unittest python/scripts/tests/test_validation.py --verbose
$ coverage report
$ coverage annotate -d coverage_files/
'''
import unittest
import os
import sys
from pathlib import Path

CURRENT_DIR_NAME = os.path.dirname(os.path.realpath(__file__))
CURRENT_DIR_PATH = Path(CURRENT_DIR_NAME)
PARENT_DIR_NAME = os.path.dirname(CURRENT_DIR_NAME)
# UTILS_DIR = Path(PARENT_DIR_NAME) / 'utils'

sys.path.insert(0, PARENT_DIR_NAME)
from utils.custom_exceptions import InvalidBoolValue
from utils import validation

class TestString2Bool(unittest.TestCase):
    def test_string_values(self):
        self.assertTrue(validation.str2bool('yes'))
        self.assertTrue(validation.str2bool('YES'))
        self.assertTrue(validation.str2bool('true'))
        self.assertTrue(validation.str2bool('TRUE'))
        self.assertTrue(validation.str2bool('t'))
        self.assertTrue(validation.str2bool('T'))
        self.assertTrue(validation.str2bool('y'))
        self.assertTrue(validation.str2bool('Y'))
        self.assertTrue(validation.str2bool('1'))
        self.assertFalse(validation.str2bool('0'))
        self.assertFalse(validation.str2bool('n'))
        self.assertFalse(validation.str2bool('N'))
        self.assertFalse(validation.str2bool('no'))
        self.assertFalse(validation.str2bool('NO'))
        self.assertFalse(validation.str2bool('false'))
        self.assertFalse(validation.str2bool('FALSE'))
        self.assertFalse(validation.str2bool('f'))
        self.assertFalse(validation.str2bool('F'))

    def test_int_value(self):
        self.assertTrue(validation.str2bool(1))
        self.assertFalse(validation.str2bool(0))

    def test_bool_value(self):
        self.assertTrue(validation.str2bool(True))
        self.assertFalse(validation.str2bool(False))

    def test_InvalidBoolValue_exception(self):
        invalid_value = 'thiswontwork'
        self.assertRaises(InvalidBoolValue, validation.str2bool, invalid_value)

if __name__ == '__main__': unittest.main()
