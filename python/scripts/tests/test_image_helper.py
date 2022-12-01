#!/usr/bin/env python
#!/usr/bin/python3
'''
Unit testing for image helper.

RUN:
$ python3 -m coverage run --source="." -m unittest python/scripts/tests/test_image_helper.py --verbose
$ coverage report
$ coverage annotate -d coverage_files/
'''
import unittest
import os
import re
import sys
from pathlib import Path

TESTS_DIR = os.path.dirname(os.path.realpath(__file__))
CUR_DIR_PATH = Path(TESTS_DIR)
SCRIPTS_DIR = os.path.dirname(TESTS_DIR)

sys.path.insert(0, SCRIPTS_DIR)
from utils.custom_exceptions import InvalidDirectory
from utils.file_helper import create_pdf
from utils.image_helper import jpg_to_gif, pdf_to_jpg

class TestJpgToGif(unittest.TestCase):
    def setUp(self) -> None:
        self.cur_dir_path = CUR_DIR_PATH
        self.sample_data_dir = CUR_DIR_PATH / 'sample_data'
        self.image_dir_path = CUR_DIR_PATH / 'sample_data' / '20210314_NASA_EPIC'
        self.test_dir_path = CUR_DIR_PATH / 'TestDirectory'
        if not self.test_dir_path.exists(): self.test_dir_path.mkdir()

    def test_jpg_to_gif(self):
        expected_gif_file_path = self.test_dir_path / 'test.gif'
        self.assertFalse(expected_gif_file_path.exists() or expected_gif_file_path.is_file())
        gif_path = jpg_to_gif(self.image_dir_path, self.test_dir_path, 'test.gif')
        self.assertTrue(isinstance(gif_path, Path))
        self.assertTrue(gif_path.exists() and gif_path.is_file())

    def test_no_name_given(self):
        gif_path = jpg_to_gif(self.image_dir_path, self.test_dir_path)
        self.assertTrue(gif_path.exists())
        name_regex = re.compile(r'^\d{4}\d{2}\d{2}\d{2}\d{2}\d{2}\.gif$') #YYYYMMDDHHMMSS
        self.assertTrue(name_regex.match(gif_path.name) is not None)

    def test_invalid_directory_exception(self):
        invalid_dir_path = self.cur_dir_path / 'invalid_directory'
        self.assertRaises(InvalidDirectory, jpg_to_gif, self.image_dir_path, invalid_dir_path)

    def tearDown(self) -> None:
        if self.test_dir_path.is_dir(): [x.unlink() for x in self.test_dir_path.iterdir() if x.is_file()]
        if self.test_dir_path.exists() and self.test_dir_path.is_dir(): self.test_dir_path.rmdir()

class TestPdfToJpg(unittest.TestCase):
    def setUp(self) -> None:
        self.cur_dir_path = CUR_DIR_PATH
        self.test_dir_path = CUR_DIR_PATH / 'TestDirectory'
        if not self.test_dir_path.exists(): self.test_dir_path.mkdir()
        self.pdf_file_dne = self.test_dir_path / 'DoesNotExist.pdf'

    def test_pdf_to_jpg(self):
        pdf_file_path = self.test_dir_path / 'test.pdf'
        pdf_file_path = create_pdf(name=pdf_file_path, input_text='TEST PDF TO JPG')
        self.assertTrue(pdf_file_path.exists() and pdf_file_path.is_file())

        pdf_to_jpg(pdf_file_path, outPath=self.test_dir_path)
        expected_jpg_fie_path = self.test_dir_path / 'test.jpg'
        self.assertTrue(expected_jpg_fie_path.exists() and expected_jpg_fie_path.is_file())

    def test_PDFPageCountError_exception(self):
        pass

    def test_FileNotFoundError_exception(self):
        self.assertRaises(FileNotFoundError, pdf_to_jpg, self.pdf_file_dne)
        self.assertRaises(FileNotFoundError, pdf_to_jpg, self.test_dir_path)

    def tearDown(self) -> None:
        if self.test_dir_path.is_dir(): [x.unlink() for x in self.test_dir_path.iterdir() if x.is_file()]
        if self.test_dir_path.exists() and self.test_dir_path.is_dir(): self.test_dir_path.rmdir()


