#!/usr/bin/env python
#!/usr/bin/python3

import unittest
import os
import sys
from test_template import SCRIPTS_DIR, TestTemplate

sys.path.insert(0, SCRIPTS_DIR)
from utils.custom_exceptions import InvalidBoolValue
from utils import validation

class TestString2Bool(TestTemplate):
    def test_string_values(self):
        for truthy in ['y', 'yes', 't', 'true', '1']:
            self.assertTrue(validation.str2bool(truthy.lower()))
            self.assertTrue(validation.str2bool(truthy.upper()))
        for falsy in ['n', 'no', 'f', 'false', '0']:
            self.assertFalse(validation.str2bool(falsy))
            self.assertFalse(validation.str2bool(falsy))

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
