#!/usr/bin/python3

import os
import sys
import unittest
from pathlib import Path
from test_base import TestBase

CUR_DIR_NAME = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.dirname(CUR_DIR_NAME))
from utils.algorithms import calc_x_trajectory, calc_y_trajectory, plot_trajectory

class TestAlgorithms(TestBase):
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

    def tearDown(self):
        return

if __name__ == '__main__': unittest.main()