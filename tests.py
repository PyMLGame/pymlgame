#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-

"""
pymlgame unittests
"""

__author__ = "Ricardo Band"
__copyright__ = "Copyright 2013, Ricardo Band"
__credits__ = ["Ricardo Band"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Ricardo Band"
__email__ = "me@xengi.de"
__status__ = "Development"

import unittest

import pymlgame
from pymlgame.locals import *

TEST_HOST = 'localhost'
TEST_PORT = 1337
TEST_WIDTH = 40
TEST_HEIGHT = 16


class ScreenTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_host_port(self):
        screen = pymlgame.Screen(host=TEST_HOST,
                                 port=TEST_PORT)
        self.assertEqual(screen.host, TEST_HOST)
        self.assertEqual(screen.port, TEST_PORT)

    def test_size(self):
        screen = pymlgame.Screen(host=TEST_HOST,
                                 port=TEST_PORT,
                                 width=TEST_WIDTH,
                                 height=TEST_HEIGHT)
        self.assertEqual(screen.width, TEST_WIDTH)
        self.assertEqual(screen.height, TEST_HEIGHT)


class SurfaceTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_size(self):
        surface = pymlgame.Surface((TEST_WIDTH, TEST_HEIGHT))
        self.assertEqual(surface.width, TEST_WIDTH)
        self.assertEqual(surface.height, TEST_HEIGHT)


if __name__ == '__main__':
    unittest.main()