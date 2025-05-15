#!/usr/bin/env python
#!/usr/bin/python3

import sys
import unittest
from test_template import TestTemplate, UTILS_DIR, clean_dir

sys.path.insert(0, UTILS_DIR)
from algorithms import calc_x_trajectory, calc_y_trajectory, plot_trajectory

class TestAlgorithms(TestTemplate):
    def setUp(self) -> None:
        self.horizontal_velocity = 10 # meters
        self.vertical_velocity = 10   # meters
        self.time_seconds = 10        # seconds
        self.acceleration = 9.81      # m/s
        return

    def test_calc_x_trajectory(self):
        expected_results = 100
        results = calc_x_trajectory(v1=self.horizontal_velocity, t=self.time_seconds)
        self.assertEqual(expected_results, results)

    def test_calc_y_trajectory(self):
        horizontal_position_x = 10
        expected_results = None
        # TODO: verify results
        results = calc_y_trajectory(v1=self.horizontal_velocity, v2=self.vertical_velocity, t=self.time_seconds, x=horizontal_position_x, a=self.acceleration)
        print(f"results: {results}")
        return

    def tearDown(self) -> None:
        return super().tearDown()

if __name__ == '__main__': unittest.main()