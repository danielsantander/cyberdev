#!/usr/bin/env python
#!/usr/bin/python3

import unittest
import os
import sys
from pathlib import Path
from test_template import UTILS_DIR, TestTemplate

sys.path.insert(0, UTILS_DIR)
from ciphers import Caesar

class TestCaesarCipher(TestTemplate):
    def setUp(self):
        super().setUp()
        self.message = 'FAIRBANKS'
        self.encrypted_msg = 'idluedqnv'
        self.offset = 3
        self.case_sensitive = False

    def test_encrypt(self):
        """Test encrypting messages with the Caesar encryption method."""
        caesar = Caesar(message=self.message, offset=self.offset, case_sensitive=self.case_sensitive)
        encryption = caesar.encrypt()
        self.assertNotEqual(self.message, encryption)
        self.assertEqual(self.encrypted_msg, encryption)

    def test_decrypt(self):
        """Test decrypting messages encrypted with the Caesar method."""
        caesar = Caesar(message=self.encrypted_msg, offset=self.offset, case_sensitive=self.case_sensitive)
        decryption = caesar.decrypt()
        self.assertNotEqual(self.encrypted_msg, decryption)
        self.assertEqual(self.message.lower(), decryption)

    def test_main(self):
        """Test main method"""
        import subprocess

        msg = 'BaTmAn'
        offset = 8
        expected_encrypted_msg = 'JiBuIv'

        cipher_path = Path(UTILS_DIR) / 'ciphers.py'
        self.assertTrue(cipher_path.exists() and cipher_path.is_file())

        cmd: subprocess.CompletedProcess = subprocess.run(["python3", f"{cipher_path.absolute()}",  msg, f"-o {offset}", "-c"], capture_output=True)
        self.assertEqual(cmd.returncode, 0)
        self.assertEqual(expected_encrypted_msg, cmd.stdout.decode('utf-8').replace("\n", ""))

    def tearDown(self) -> None:
        return super().tearDown()

if __name__ == '__main__': unittest.main()
