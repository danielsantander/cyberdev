#!/usr/bin/env python
#!/usr/bin/python3

import unittest
import os
import sys
import logging
from pathlib import Path
from test_template import SCRIPTS_DIR, TestTemplate

sys.path.insert(0, SCRIPTS_DIR)
from utils import custom_logging
from utils.navigation import clean_directory

class TestCustomLogging(TestTemplate):
    def setUp(self) -> None:
        super().setUp()
        self.log_level:int = logging.DEBUG
        self.log_dir:Path = self._test_dir / 'TestCustomLogging'
        if not self.log_dir.exists(): self.log_dir.mkdir(parents=True, exist_ok=True)

    def test_console_logger(self):
        console_logger = custom_logging.create_console_logger(level=self.log_level)
        self.assertEqual(isinstance(console_logger, logging.Logger), True)
        self.assertEqual(console_logger.level, self.log_level)
        self.assertTrue(console_logger.hasHandlers())

    def test_creating_rotational_logger(self):
        master_logger_path:Path = self.log_dir / 'TestLogger.log'
        self.assertFalse(master_logger_path.exists())

        logger =  custom_logging.create_logger(name='TestLogger', level=self.log_level, log_dir=self.log_dir)
        self.assertTrue(master_logger_path.exists())
        self.assertTrue(master_logger_path.is_file())
        self.assertEqual(isinstance(logger, logging.Logger), True)
        self.assertEqual(logger.level, self.log_level)
        self.assertTrue(logger.hasHandlers())

    def tearDown(self) -> None:
        return super().tearDown()

if __name__ == '__main__': unittest.main()