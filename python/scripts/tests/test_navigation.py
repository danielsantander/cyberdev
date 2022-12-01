#!/usr/bin/python3
'''
Unit testing for navigation library.

RUN:
$ python3 -m coverage run --source="." -m unittest python/scripts/tests/test_navigation.py --verbose
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
from utils.custom_exceptions import InvalidDirectory
from utils.navigation import make_directory, clean_directory, get_filenames

class TestNavigation(unittest.TestCase):
    def setUp(self)->None:
        self.test_dir =  CURRENT_DIR_PATH / "TestNavigationDirectory"

    def test_make_directory(self):
        self.assertEqual(self.test_dir.exists(), False)
        self.assertEqual(self.test_dir.is_dir(), False)
        self.test_dir = make_directory(self.test_dir)
        self.assertEqual(self.test_dir.exists(), True)
        self.assertEqual(self.test_dir.is_dir(), True)
        self.test_dir.rmdir()

    def test_get_list_of_filenames(self):
        # make test files
        self.test_dir = make_directory(self.test_dir)
        new_file = self.test_dir / 'testfile.txt'
        filename_list = []
        filepath_list = []
        self.assertEqual(new_file.exists(), False)
        new_file.touch(exist_ok=True)
        self.assertEqual(new_file.exists(), True)
        self.assertEqual(new_file.is_file(), True)

        # test get_filenames as list of file names
        filename_list = get_filenames(self.test_dir)
        self.assertEqual(isinstance(filename_list[0], str), True)
        self.assertEqual(len(filename_list), 1)
        self.assertEqual(filename_list[0], new_file.name)

        # test get_filenames as list of paths
        filepath_list = get_filenames(self.test_dir, return_as_path=True)
        self.assertEqual(isinstance(filepath_list[0], Path), True)
        self.assertEqual(filepath_list[0].name, new_file.name)

        # remove file
        new_file.unlink()

    def test_clean_directory(self):
        # make test files
        self.test_dir = make_directory(self.test_dir)
        (self.test_dir / 'testfile1.txt').touch(exist_ok=True)
        (self.test_dir / 'testfile2.txt').touch(exist_ok=True)
        file_list = get_filenames(self.test_dir)
        self.assertEqual(len(file_list), 2)

        file_list = []
        cleaned_file_list = []
        clean_directory(self.test_dir)
        cleaned_file_list = get_filenames(self.test_dir)
        self.assertEqual(len(cleaned_file_list), 0)

        # test with "remove_directory" flag set to True
        removed_directory = clean_directory(self.test_dir, remove_directory=True)
        self.assertEqual(removed_directory.is_dir(), False)
        self.assertEqual(removed_directory.exists(), False)
        self.assertEqual(self.test_dir.is_dir(), False)
        self.assertEqual(self.test_dir.exists(), False)

    def test_get_certain_files(self):
        # make test files
        self.test_dir = make_directory(self.test_dir)
        (self.test_dir / 'testfile1.txt').touch(exist_ok=True)
        (self.test_dir / 'testfile2.txt').touch(exist_ok=True)
        file_list = get_filenames(self.test_dir)
        self.assertEqual(len(file_list), 2)

    def test_invalid_directory_raises_exception(self):
        fake_directory_name:Path = CURRENT_DIR_PATH / 'FAKE_DIRECTORY'
        self.assertRaises(InvalidDirectory, get_filenames, fake_directory_name)

    def tearDown(self)->None:
        if self.test_dir.exists() and self.test_dir.is_dir(): clean_directory(self.test_dir, remove_directory=True)

if __name__ == '__main__': unittest.main()
