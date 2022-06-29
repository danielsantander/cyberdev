#!/usr/bin/python3
'''
Unit testing for utils library.
'''
import datetime
import unittest
import os
import re
import sys
import logging
from pathlib import Path

CURRENT_DIR_NAME = os.path.dirname(os.path.realpath(__file__))
CURRENT_DIR_PATH = Path(CURRENT_DIR_NAME)
PARENT_DIR_NAME = os.path.dirname(CURRENT_DIR_NAME)
# UTILS_DIR = Path(PARENT_DIR_NAME) / 'utils'

sys.path.insert(0, PARENT_DIR_NAME)
from utils.custom_exceptions import InvalidDirectory, InvalidBoolValue
from utils.custom_logging import create_console_logger, create_logger
from utils.date_helper import timestamp_to_date_string, current_iso_time
from utils.file_helper import write_json_to_file, open_json_from_file, combine_pdfs, create_pdf, encrypt_pdf, rename_path
from utils.image_helper import jpg_to_gif
from utils.navigation import make_directory, clean_directory, get_filenames
from utils.validation import str2bool

class TestLoggerHelper(unittest.TestCase):
    def setUp(self)->None:
        self.cur_dir_path = CURRENT_DIR_PATH
        self.log_dir = self.cur_dir_path / 'test_logs'
        self.log_level = logging.DEBUG
        self.cl = create_console_logger(level=self.log_level)
        self.logger = create_logger(name="TestLogger", level=self.log_level, log_dir=self.log_dir)

    def test_console_logger(self):
        self.assertEqual(isinstance(self.cl, logging.Logger), True)
        self.assertEqual(self.cl.level, self.log_level)

    def test_logger_has_handlers(self):
        self.assertTrue(self.cl.hasHandlers())

    def test_create_logger(self):
        master_log_file = self.log_dir / 'master_logger.log'
        self.assertEqual(isinstance(self.logger, logging.Logger), True)
        self.assertEqual(self.logger.level, self.log_level)
        self.assertTrue(self.logger.hasHandlers())
        self.assertTrue(self.log_dir.exists())
        self.assertTrue(self.log_dir.is_dir())
        self.assertTrue(master_log_file.exists())
        self.assertTrue(master_log_file.is_file())
    
    def tearDown(self)->None:
        if self.log_dir.exists():
            clean_directory(self.log_dir, remove_directory=True)

class TestDateHelper(unittest.TestCase):
    def setUp(self) -> None:
        self.now = datetime.datetime.utcnow()
        self.now_timestamp = self.now.timestamp()
        self.str_format = '%Y%m%d%H%M%S'
        self.now_str = self.now.strftime(self.str_format)

    def test_timestamp_to_str(self):
        results = timestamp_to_date_string(self.now_timestamp)  # 20220117041520
        format_regex = re.compile(r'^\d{4}\d{2}\d{2}\d{2}\d{2}\d{2}$') # YYYYMMDDHHMMSS
        self.assertTrue(isinstance(results, str))
        self.assertEqual(results, self.now_str)
        self.assertTrue(format_regex.match(results) is not None)

    def test_iso_time(self):
        results = current_iso_time()    # 2022-01-17T04:15:20.696565+00:00
        self.assertTrue(isinstance(results, str))
        format_regex = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d*\+\d{2}:\d{2}$')
        self.assertTrue(format_regex.match(results) is not None)

class TestFileHelper(unittest.TestCase):
    def setUp(self)->None:
        self.test_dir = CURRENT_DIR_PATH / 'TestFileHelperDirectory'
        if not self.test_dir.exists():
            self.test_dir.mkdir()
        self.test_json_file = self.test_dir / 'test.json'
        self.pdf_file_dne = self.test_dir / 'DoesNotExist.pdf'
        self.invalid_pdf_file = self.test_dir / 'Invalid.pdf'
        self.encrypted_pdf_file = self.test_dir / 'Encrypted.pdf'
        self.test_json:dict = {'text':'hello world'}

    # JSONs
    def test_write_json(self):
        self.assertFalse(self.test_json_file.exists())
        write_json_to_file(self.test_json_file, self.test_json)
        self.assertTrue(self.test_json_file.exists())

    def test_open_json_from_file(self):
        write_json_to_file(self.test_json_file, self.test_json)
        self.assertTrue(self.test_json_file.exists())
        uploaded_json = open_json_from_file(self.test_json_file)
        self.assertEqual(uploaded_json.get('text', True), self.test_json.get('text', False))
        self.assertTrue(isinstance(uploaded_json, dict))
        self.assertEqual(uploaded_json, self.test_json)

    # PDFs
    def test_combine_pdfs(self):
        
        pdfDir = self.test_dir / 'pdfs'
        self.assertRaises(InvalidDirectory, combine_pdfs, pdfDir)

        if not pdfDir.exists():
            pdfDir.mkdir()

        pdfA = pdfDir / 'FileA.pdf'
        pdfB = pdfDir / 'FileB.pdf'
        pdfC = pdfDir / 'FileC.pdf'
        pdfCombined = pdfDir / 'Combined.pdf'

        # generate pdf files to combine
        pdfList = [pdfA, pdfB, pdfC]
        for pdf in pdfList:
            self.assertFalse(pdf.exists())
            self.assertFalse(pdf.is_file())
            create_pdf(
                name=pdf,
                input_text=pdf.name[:5],
                font_size=22)
            self.assertTrue(pdf.exists())
            self.assertTrue(pdf.is_file())
        
        self.assertFalse(pdfCombined.exists())
        self.assertFalse(pdfCombined.is_file())
        combine_pdfs(inputDir=pdfDir)
        self.assertTrue(pdfCombined.exists())
        self.assertTrue(pdfCombined.is_file())
        # TODO: check pdfCombined object to see if the three files are present

    def test_create_pdf(self):
        self.encrypted_pdf_file.touch()
        self.assertRaises(OSError, encrypt_pdf, self.invalid_pdf_file)
        new_pdf_file = self.test_dir / 'new.pdf';
        self.assertFalse(new_pdf_file.exists())
        create_pdf(
            name=new_pdf_file,
            input_text='Testing Purposes Only',
            font_size=12);
        self.assertTrue(new_pdf_file.exists())

    def test_encrypt_pdf_FileNotFoundError(self):
        self.assertRaises(FileNotFoundError, encrypt_pdf, self.pdf_file_dne)

    def test_encrypt_pdf_OSError(self):
        if not self.test_dir.exists():
            self.test_dir.mkdir()
        self.invalid_pdf_file.touch()
        self.assertRaises(OSError, encrypt_pdf, self.invalid_pdf_file)

    # File manipulation
    def test_rename_path(self):

        # test success rename file
        original_filename = 'test_rename_file.txt'
        rename_filename = 'filename_has_been_changed.txt'
        test_file = self.test_dir / original_filename
        test_file_stream = open(test_file.absolute(), 'w')
        test_file_stream.write('Hello World!\n')
        test_file_stream.close()
        self.assertTrue(test_file.exists())
        self.assertEqual(test_file.name, original_filename)
        results = rename_path(test_file, rename_filename)
        self.assertTrue(results.exists())
        self.assertEqual(results.name, rename_filename)
        results.unlink()
        self.assertFalse(results.exists())
        
        # test FileNotFoundError
        original_filename = 'test_FileNotFoundError.txt'
        test_file = self.test_dir / original_filename
        self.assertRaises(FileNotFoundError, rename_path, test_file, rename_filename)

        # test FileExistsError
        original_filename_a = 'test_FileExistsError_A.txt'
        test_file_a = self.test_dir / original_filename_a
        test_file_a_contents = 'Test File A'
        test_file_a_stream = open(test_file_a.absolute(), 'w')
        test_file_a_stream.write(test_file_a_contents)
        test_file_a_stream.close()

        original_filename_b = 'test_FileExistsError_B.txt'
        test_file_b = self.test_dir / original_filename_b
        test_file_b_contents = 'Test File B'
        test_file_b_stream = open(test_file_b.absolute(), 'w') 
        test_file_b_stream.write(test_file_b_contents)
        test_file_b_stream.close()

        self.assertTrue(test_file_a.exists())
        self.assertTrue(test_file_b.exists())
        self.assertRaises(FileExistsError, rename_path, test_file_a, test_file_b.name)

        # test overwrite existing file
        results = rename_path(test_file_a, test_file_b.name, overwrite=True)
        result_stream = open(results.absolute(), 'r')
        file_contents = result_stream.readline().strip()
        result_stream.close()
        self.assertFalse((self.test_dir / original_filename_a).exists())
        self.assertTrue(results.exists())
        self.assertEqual(results.name, test_file_b.name)
        self.assertEqual(file_contents, test_file_a_contents)
        results.unlink()

        # test cannot rename a directory given a file path as new_name (NotADirectoryError)
        new_dir = self.test_dir / 'new_dir'
        new_dir.mkdir()
        test_file = self.test_dir / 'test_file.txt'
        test_file_stream = open(test_file.absolute(), 'w')
        test_file_stream.write('Hello World!\n')
        test_file_stream.close()
        self.assertTrue(new_dir.exists() and new_dir.is_dir())
        self.assertTrue(test_file.exists())
        self.assertRaises(NotADirectoryError, rename_path, new_dir, test_file, overwrite=True)
        new_dir.rmdir()
        test_file.unlink()

    def tearDown(self) -> None:
        # delete (unlink) any test files or directories
        pdfDir = self.test_dir / 'pdfs'
        if pdfDir.exists() & pdfDir.is_dir():
            [x.unlink() for x in pdfDir.iterdir() if x.is_file()]
            pdfDir.rmdir()
        if self.test_dir.exists() and self.test_dir.is_dir():
            [x.unlink() for x in self.test_dir.iterdir() if x.is_file()]
            self.test_dir.rmdir()

class TestJpgToGif(unittest.TestCase):
    def setUp(self) -> None:
        self.image_dir = CURRENT_DIR_PATH / 'sample_data' / '20210314_NASA_EPIC'
        self.gif_name = 'test.gif'
        self.gif_dir = self.image_dir.parent / 'GIFs'
    
    def test_default(self):
        self.assertFalse(self.gif_dir.is_dir())
        self.assertFalse(self.gif_dir.exists())
        self.gif_dir.mkdir()
        self.assertTrue(self.gif_dir.exists())
        self.assertTrue(self.gif_dir.is_dir())
        self.assertTrue(self.image_dir.exists())
        self.assertTrue(self.image_dir.is_dir())
        self.assertTrue(self.gif_name.endswith('.gif'))
        jpg_to_gif(self.image_dir, self.gif_dir, gif_name=self.gif_name)
        gif_path = self.gif_dir / str(self.gif_name)
        self.assertTrue(gif_path.exists())
        self.assertTrue(gif_path.is_file())
        self.assertTrue(gif_path.name.endswith('.gif'))
    
    def test_invalid_directory_exception_raised(self):
        # self.gif_name = self.gif_name.split('.')[0] # remove file extension
        self.assertRaises(InvalidDirectory, jpg_to_gif, self.image_dir, self.gif_dir, self.gif_name)

    def test_no_name_given(self):
        if self.gif_dir.exists() is False: self.gif_dir.mkdir()
        jpg_to_gif(self.image_dir, self.gif_dir)
        self.assertTrue(any(self.gif_dir.iterdir()))
        gif_path = [x for x in self.gif_dir.iterdir() if x.is_file()][0]
        self.assertTrue(gif_path.exists())
        name_regex = re.compile(r'^\d{4}\d{2}\d{2}\d{2}\d{2}\d{2}\.gif$') #YYYYMMDDHHMMSS
        self.assertTrue(name_regex.match(gif_path.name) is not None)
    
    def tearDown(self):
        if self.gif_dir.is_dir(): [x.unlink() for x in self.gif_dir.iterdir() if x.is_file()]
        if self.gif_dir.exists() and self.gif_dir.is_dir(): self.gif_dir.rmdir()

class TestNavigation(unittest.TestCase):
    def setUp(self)->None:
        self.cur_dir_path = CURRENT_DIR_PATH
        self.test_dir =  self.cur_dir_path / "TestDirectory"

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
        fake_directory_name = self.cur_dir_path / 'FAKE_DIRECTORY'
        self.assertRaises(InvalidDirectory, get_filenames, fake_directory_name)

    def tearDown(self)->None:
        if self.test_dir.exists() and self.test_dir.is_dir():
            [x.unlink() for x in self.test_dir.iterdir() if x.is_file()]
            self.test_dir.rmdir()

class TestString2Bool(unittest.TestCase):
    def test_string_values(self):
        self.assertTrue(str2bool('yes'))
        self.assertTrue(str2bool('YES'))
        self.assertTrue(str2bool('true'))
        self.assertTrue(str2bool('TRUE'))
        self.assertTrue(str2bool('t'))
        self.assertTrue(str2bool('T'))
        self.assertTrue(str2bool('y'))
        self.assertTrue(str2bool('Y'))
        self.assertTrue(str2bool('1'))
        self.assertFalse(str2bool('0'))
        self.assertFalse(str2bool('n'))
        self.assertFalse(str2bool('N'))
        self.assertFalse(str2bool('no'))
        self.assertFalse(str2bool('NO'))
        self.assertFalse(str2bool('false'))
        self.assertFalse(str2bool('FALSE'))
        self.assertFalse(str2bool('f'))
        self.assertFalse(str2bool('F'))
    
    def test_int_value(self):
        self.assertTrue(str2bool(1))
        self.assertFalse(str2bool(0))

    def test_bool_value(self):
        self.assertTrue(str2bool(True))
        self.assertFalse(str2bool(False))
    
    def test_raise_exception(self):
        invalid_value = 'thiswontwork'
        self.assertRaises(InvalidBoolValue, str2bool, invalid_value)

if __name__ == '__main__':
    unittest.main()
