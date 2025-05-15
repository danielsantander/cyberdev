#!/usr/bin/env python
#!/usr/bin/python3

import unittest
import os
import re
import sys
from pathlib import Path
from test_template import SCRIPTS_DIR, TEST_DIR, TestTemplate

sys.path.insert(0, SCRIPTS_DIR)
from utils.custom_exceptions import InvalidDirectory
from utils.file_helper import create_pdf
from utils.image_helper import jpg_to_gif, pdf_to_jpg

class TestJpgToGif(TestTemplate):
    def setUp(self):
        self.test_dir = self._test_dir / 'TestImageHelper' / 'TestJpgToGif'
        if self.test_dir.exists() is False: self.test_dir.mkdir(parents=True, exist_ok=True)
        self.sample_test_data:Path = Path(TEST_DIR) / 'sample_test_data'
        self.image_dir_path = self.sample_test_data / '20210314_NASA_EPIC'

    def test_jpg_to_gif(self):
        expected_gif_file_path = self.test_dir / 'test.gif'
        self.assertFalse(expected_gif_file_path.exists() or expected_gif_file_path.is_file())
        gif_path = jpg_to_gif(self.image_dir_path, self.test_dir, 'test.gif')
        self.assertTrue(isinstance(gif_path, Path))
        self.assertTrue(gif_path.exists() and gif_path.is_file())

    def test_no_name_given(self):
        gif_path = jpg_to_gif(self.image_dir_path, self.test_dir)
        self.assertTrue(gif_path.exists())
        name_regex = re.compile(r'^\d{4}\d{2}\d{2}\d{2}\d{2}\d{2}\.gif$') #YYYYMMDDHHMMSS
        self.assertTrue(name_regex.match(gif_path.name) is not None)

    def test_invalid_directory_exception(self):
        invalid_dir_path = self.test_dir / 'InvalidDirectory'
        self.assertFalse(invalid_dir_path.exists())
        self.assertRaises(InvalidDirectory, jpg_to_gif, self.image_dir_path, invalid_dir_path)

    def tearDown(self) -> None:
        return super().tearDown()

class TestPdfToJpg(TestTemplate):
    def setUp(self):
        super().setUp()
        self.test_dir = self._test_dir / 'TestImageHelper' / 'TestPdfToJpg'
        if not self.test_dir.exists(): self.test_dir.mkdir(parents=True, exist_ok=True)
        self.pdf_file_dne = self.test_dir / 'DoesNotExist.pdf'

    @unittest.skip('exception: pdf2image.exceptions.PDFPageCountError: Unable to get page count.')
    def test_pdf_to_jpg(self):
        pdf_file_path = self.test_dir / 'test.pdf'
        pdf_file_path = create_pdf(name=pdf_file_path, input_text='TEST PDF TO JPG')
        self.assertTrue(pdf_file_path.exists() and pdf_file_path.is_file())

        pdf_to_jpg(pdf_file_path, outPath=self.test_dir)
        expected_jpg_fie_path = self.test_dir / 'test.jpg'
        self.assertTrue(expected_jpg_fie_path.exists() and expected_jpg_fie_path.is_file())

    def test_PDFPageCountError_exception(self):
        pass

    def test_FileNotFoundError_exception(self):
        self.assertRaises(FileNotFoundError, pdf_to_jpg, self.pdf_file_dne)
        self.assertRaises(FileNotFoundError, pdf_to_jpg, self.test_dir)

    def tearDown(self):
        return super().tearDown()

if __name__ == '__main__': unittest.main()
