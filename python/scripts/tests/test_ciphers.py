#!/usr/bin/python3
'''
Unit testing for cipher library within utils.
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
from utils.ciphers import caesar

class TestCaesarCipher(unittest.TestCase):
    def setUp(self):
        self.message = 'FAIRBANKS'
        self.encrypted_msg = 'idluedqnv'
        self.test_offset = 3

    def test_encrypt(self):
        """Test encrypting messages with the Caesar encryption method."""
        encryption = caesar.encrypt(self.message, self.test_offset)
        self.assertNotEqual(self.message, encryption)
        self.assertEqual(self.encrypted_msg, encryption)

    def test_decrypt(self):
        """Test decrypting messages encrypted with the Caesar method."""
        decryption = caesar.decrypt(self.encrypted_msg, self.test_offset)
        self.assertNotEqual(self.encrypted_msg, decryption)
        self.assertEqual(self.message.lower(), decryption)

    def test_failures(self):
        """Test method failures."""
        self.assertRaises(Exception, caesar.encrypt, self.message, -1)
        self.assertRaises(Exception, caesar.encrypt, self.message, 26)
        self.assertRaises(Exception, caesar.decrypt, self.encrypted_msg, -1)
        self.assertRaises(Exception, caesar.decrypt, self.encrypted_msg, 26)

if __name__ == '__main__':
    unittest.main()
