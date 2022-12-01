#!/usr/bin/python3
'''
Unit testing for file helper.

RUN:
$ python3 -m coverage run --source="." -m unittest python/scripts/tests/test_file_helper.py --verbose
$ coverage report
$ coverage annotate -d coverage_files/
'''
import datetime
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
from utils.file_helper import write_json_to_file, open_json_from_file, combine_pdfs, create_pdf, encrypt_pdf, rename_path

class TestFileHelper(unittest.TestCase):
    def setUp(self)->None:
        self.test_dir = CURRENT_DIR_PATH / 'TestFileHelperDirectory'
        if not self.test_dir.exists(): self.test_dir.mkdir()
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

    def test_create_pdf_with_filename_as_path(self):
        new_pdf_file = self.test_dir / 'new.pdf'
        self.assertFalse(new_pdf_file.exists())
        create_pdf(
            name=new_pdf_file,
            input_text='Testing Purposes Only',
            font_size=12)
        self.assertTrue(new_pdf_file.exists())

    def test_create_pdf_with_no_args(self):
        name = f'{datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")}.pdf'
        new_pdf_file_2 = create_pdf()
        self.assertTrue(new_pdf_file_2.exists() and new_pdf_file_2.is_file())
        self.assertEqual(name, new_pdf_file_2.name)
        new_pdf_file_2.unlink()
        self.assertFalse(new_pdf_file_2.exists())

    def test_create_pdf_from_filename(self):
        new_pdf_file_3 = create_pdf(name="new_pdf_file_3")
        self.assertTrue(new_pdf_file_3.exists())
        new_pdf_file_3.unlink()
        self.assertFalse(new_pdf_file_3.exists())

    def test_encrypt_pdf_FileNotFoundError(self):
        self.assertRaises(FileNotFoundError, encrypt_pdf, self.pdf_file_dne)

    def test_encrypt_pdf_OSError(self):
        self.invalid_pdf_file.touch()
        self.assertRaises(OSError, encrypt_pdf, self.invalid_pdf_file)

    def test_encrypt_pdf(self):
        valid_pdf_path = self.test_dir / 'valid.pdf'
        expected_encrypted_pdf_path = self.test_dir / 'validENCRYPTED.pdf'
        valid_pdf_path = create_pdf(name=valid_pdf_path,input_text="valid pdf")
        encrypted_pdf_path = encrypt_pdf(path=valid_pdf_path, outpath=self.test_dir)
        self.assertTrue(expected_encrypted_pdf_path.exists() and expected_encrypted_pdf_path.is_file())
        self.assertEqual(encrypted_pdf_path.name, expected_encrypted_pdf_path.name)

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

if __name__ == '__main__': unittest.main()
