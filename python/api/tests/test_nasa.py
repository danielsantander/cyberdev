#!/usr/bin/env python
#!/usr/bin/python3

import os
import sys
import unittest
from pathlib import Path
from test_template import TestTemplate, clean_dir, API_DIR

sys.path.insert(0, API_DIR)
from nasa import EPIC

class TestNASA(TestTemplate):
    def setUp(self)->None:
        self.test_dir = self._test_dir / 'TestNASA'
        if not self.test_dir.exists(): self.test_dir.mkdir()
        self.epic = EPIC(save_dir=self.test_dir)

    def tearDown(self) -> None:
        if self.test_dir.exists() and self.test_dir.is_dir(): clean_dir(self.test_dir)

    def test_get_epic_images(self):
        self.epic.get_epic_images()
        nasa_dir: Path = self.test_dir / 'epic'
        gif_dir: Path = nasa_dir / 'gifs'
        images_dir: Path = nasa_dir / 'images'
        data_dir:  Path = nasa_dir / 'api_data'
        self.assertTrue(nasa_dir.exists() and nasa_dir.is_dir())
        self.assertTrue(gif_dir.exists() and gif_dir.is_dir())
        self.assertTrue(images_dir.exists() and images_dir.is_dir())
        self.assertTrue(data_dir.exists() and data_dir.is_dir())

if __name__ == '__main__':
    print(f"Testing NASA API...")
    unittest.main()
