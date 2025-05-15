#!/usr/bin/env python
#!/usr/bin/python3

import unittest
import sys
import unittest
from pathlib import Path
from test_template import SCRIPTS_DIR, TestTemplate

sys.path.insert(0, SCRIPTS_DIR)
from utils import custom_exceptions

class TestInvalidDirectory(TestTemplate):
    def setUp(self)->None:
        super().setUp()
        self.test_dir : Path = self._test_dir / 'TestInvalidDirectory'
        self.test_dir.mkdir(parents=True, exist_ok=True)

    def test_valid_directory(self):
        self.assertTrue(self.test_dir.exists() and self.test_dir.is_dir())


    def test_invalid_directory(self):
        invalid_directory = self.test_dir / 'into_the_void'
        self.assertFalse(invalid_directory.exists())
        self.assertFalse(invalid_directory.is_dir())

        def raise_exception():
            raise custom_exceptions.InvalidDirectory(invalid_directory)

        with self.assertRaises(custom_exceptions.InvalidDirectory) as context:
            raise_exception()
        self.assertTrue(str(context.exception).find('Invalid path given. Directory does not exist') != -1)

    def tearDown(self):
        return super().tearDown()

class TestInvalidBoolValue(TestTemplate):
    def setUp(self) -> None:
        return super().setUp()

    def test_invalid_boolean(self):
        invalid_boolean = '???'
        def raise_exception():
            raise custom_exceptions.InvalidBoolValue(invalid_boolean)
        with self.assertRaises(custom_exceptions.InvalidBoolValue) as context:
            raise_exception()
        self.assertTrue(str(context.exception).find('Unknown boolean value') != -1)

    def tearDown(self):
        return super().tearDown()

class TestInvalidFile(TestTemplate):
    def setUp(self) -> None:
        super().setUp()
        self.test_dir : Path = self._test_dir / 'TestInvalidFile'

    def test_invalid_file(self):
        invalid_file = self.test_dir / 'invalid_file.txt'
        self.assertFalse(invalid_file.exists())
        self.assertFalse(invalid_file.is_dir())
        def raise_exception():
            raise custom_exceptions.InvalidFile(invalid_file)
        with self.assertRaises(custom_exceptions.InvalidFile) as context:
            raise_exception()
        self.assertEqual(str(context.exception), f'Invalid file {invalid_file.absolute().__str__()}')

    def tearDown(self):
        return super().tearDown()


if __name__ == '__main__': unittest.main()