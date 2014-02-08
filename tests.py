#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-

"""
pymlgame - Unittests
"""

__author__ = "Ricardo Band"
__copyright__ = "Copyright 2013, Ricardo Band"
__credits__ = ["Ricardo Band"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Ricardo Band"
__email__ = "me@xengi.de"
__status__ = "Development"

import time
import math
import random
import unittest

import pymlgame

TEST_HOST = 'localhost'
TEST_PORT = 1337
TEST_WIDTH = 40
TEST_HEIGHT = 40


class ScreenTest(unittest.TestCase):
    def setUp(self):
        self.screen = pymlgame.Screen(TEST_HOST, TEST_PORT, TEST_WIDTH, TEST_HEIGHT)

    def test_host_port(self):
        self.assertEqual(self.screen.host, TEST_HOST)
        self.assertEqual(self.screen.port, TEST_PORT)

    def test_size(self):
        self.assertEqual(self.screen.width, TEST_WIDTH)
        self.assertEqual(self.screen.height, TEST_HEIGHT)

    def test_reset(self):
        surface = pymlgame.Surface(TEST_WIDTH, TEST_HEIGHT)
        surface.fill(pymlgame.MAGENTA, 1.0)
        self.screen.blit(surface, (0, 0))

        for _ in range(10):
            x = random.randint(0, TEST_WIDTH - 1)
            y = random.randint(0, TEST_HEIGHT - 1)
            self.assertEqual(self.screen.matrix[x][y], pymlgame.MAGENTA)

        self.screen.reset()

        for _ in range(10):
            x = random.randint(0, TEST_WIDTH - 1)
            y = random.randint(0, TEST_HEIGHT - 1)
            self.assertEqual(self.screen.matrix[x][y], pymlgame.BLACK)

    def test_matrix(self):
        self.assertEqual(len(self.screen.matrix), TEST_WIDTH)
        self.assertEqual(len(self.screen.matrix[TEST_WIDTH - 1]), TEST_HEIGHT)

        self.assertEqual(self.screen.matrix[0][0], pymlgame.BLACK)
        self.assertEqual(self.screen.matrix[TEST_WIDTH - 1][TEST_HEIGHT - 1],
                         pymlgame.Surface.get_color(pymlgame.BLACK, 0.1))

    def test_update(self):
        pass

    def test_blit(self):
        surface = pymlgame.Surface(TEST_WIDTH - 2, TEST_HEIGHT - 2)
        surface.fill(pymlgame.WHITE, 1.0)
        self.screen.blit(surface, (1, 1))

        for x in range(TEST_WIDTH):
            for y in range(TEST_HEIGHT):
                if 0 < x < TEST_WIDTH - 1 and 0 < y < TEST_HEIGHT - 1:
                    self.assertEqual(self.screen.matrix[x][y], pymlgame.WHITE)
                else:
                    self.assertEqual(self.screen.matrix[x][y], pymlgame.BLACK)

    def test_point_on_screen(self):
        self.assertTrue(self.screen.point_on_screen((0, 0)))
        self.assertTrue(self.screen.point_on_screen((TEST_WIDTH - 1, 0)))
        self.assertTrue(self.screen.point_on_screen((0, TEST_HEIGHT - 1)))
        self.assertTrue(self.screen.point_on_screen((TEST_WIDTH - 1, TEST_HEIGHT - 1)))
        self.assertFalse(self.screen.point_on_screen((-1, -1)))
        self.assertFalse(self.screen.point_on_screen((TEST_WIDTH, 0)))
        self.assertFalse(self.screen.point_on_screen((0, TEST_HEIGHT)))
        self.assertFalse(self.screen.point_on_screen((TEST_WIDTH, TEST_HEIGHT)))


class SurfaceTest(unittest.TestCase):
    def setUp(self):
        self.surface = pymlgame.Surface(TEST_WIDTH, TEST_HEIGHT)

    def test_size(self):
        self.assertEqual(self.surface.width, TEST_WIDTH)
        self.assertEqual(self.surface.height, TEST_HEIGHT)

    def test_matrix(self):
        self.assertEqual(len(self.surface.matrix), TEST_WIDTH)
        self.assertEqual(len(self.surface.matrix[TEST_WIDTH - 1]), TEST_HEIGHT)

        self.assertEqual(self.surface.matrix[0][0], pymlgame.BLACK)
        self.assertEqual(self.surface.matrix[TEST_WIDTH - 1][TEST_HEIGHT - 1],
                         self.surface.get_color(pymlgame.BLACK, 0.1))

    def test_fill(self):
        self.surface.fill(pymlgame.BLUE, 0.5)

        self.assertEqual(self.surface.matrix[0][0],
                         self.surface.get_color(pymlgame.BLUE, 0.5))
        self.assertEqual(self.surface.matrix[TEST_WIDTH - 1][0],
                         self.surface.get_color(pymlgame.BLUE, 0.5))
        self.assertEqual(self.surface.matrix[0][TEST_HEIGHT - 1],
                         self.surface.get_color(pymlgame.BLUE, 0.5))
        self.assertEqual(self.surface.matrix[TEST_WIDTH - 1][TEST_HEIGHT - 1],
                         self.surface.get_color(pymlgame.BLUE, 0.5))
        for _ in range(10):
            self.assertEqual(self.surface.matrix[random.randrange(0, TEST_WIDTH)][random.randrange(0, TEST_HEIGHT)],
                             self.surface.get_color(pymlgame.BLUE, 0.5))

    def test_draw_dot(self):
        # create 10 random dots
        randpoints = [(random.randrange(0, TEST_WIDTH),
                       random.randrange(0, TEST_HEIGHT)) for _ in range(10)]
        # draw the dots
        for point in randpoints:
            self.surface.draw_dot(point, pymlgame.YELLOW, 1.0)
        # test if drawing was successful
        for x in range(TEST_WIDTH):
            for y in range(TEST_HEIGHT):
                color = self.surface.matrix[x][y]
                if (x, y) in randpoints:
                    self.assertEqual(color, pymlgame.YELLOW)
                else:
                    self.assertEqual(color, pymlgame.BLACK)

    def test_draw_line(self):
        self.surface.draw_line((1, 0), (TEST_WIDTH - 1, 0), pymlgame.GREY6, 1.0)
        self.surface.draw_line((0, 1), (0, TEST_HEIGHT - 1), pymlgame.RED, 1.0)
        test_len = max(TEST_WIDTH, TEST_HEIGHT)
        self.surface.draw_line((test_len - 2, test_len - 2), (2, 2),
                               pymlgame.CYAN, 1.0)

        for x in range(1, TEST_WIDTH):
            self.assertEqual(self.surface.matrix[x][0], pymlgame.GREY6)
            self.assertEqual(self.surface.matrix[x][1], pymlgame.BLACK)
        for y in range(1, TEST_HEIGHT):
            self.assertEqual(self.surface.matrix[0][y], pymlgame.RED)
            self.assertEqual(self.surface.matrix[1][y], pymlgame.BLACK)
        for z in range(2, test_len - 1):
            self.assertEqual(self.surface.matrix[z][z], pymlgame.CYAN)
            self.assertEqual(self.surface.matrix[z + 1][z], pymlgame.BLACK)
            self.assertEqual(self.surface.matrix[z][z + 1], pymlgame.BLACK)

    def test_draw_rect(self):
        self.surface.draw_rect((1, 1), (TEST_WIDTH - 2, TEST_HEIGHT - 2),
                               pymlgame.DARKYELLOW, None, 0.3)

        darkyel = self.surface.get_color(pymlgame.DARKYELLOW, 0.3)
        for x in range(TEST_WIDTH):
            for y in range(TEST_HEIGHT):
                if x == 1 and 0 < y < TEST_HEIGHT - 1 or \
                   x == TEST_WIDTH - 2 and 0 < y < TEST_HEIGHT - 1 or \
                   TEST_WIDTH - 2 > x > 1 == y or \
                   1 < x < TEST_WIDTH - 2 and y == TEST_HEIGHT - 2:
                    self.assertEqual(self.surface.matrix[x][y], darkyel,
                                     '{},{}'.format(x, y))
                else:
                    self.assertEqual(self.surface.matrix[x][y], pymlgame.BLACK)

        self.surface.fill(pymlgame.BLACK)
        self.surface.draw_rect((int(TEST_WIDTH / 2) + 1,
                                int(TEST_HEIGHT / 2) + 1), (1, 1),
                               pymlgame.MAGENTA, pymlgame.DARKCYAN, 1.0)

    def test_draw_circle(self):
        #TODO: invent a way to draw this, then a way to test this
        pos = (int(TEST_WIDTH / 2) - 1, int(TEST_HEIGHT / 2) - 1)
        radius = int(min(TEST_WIDTH, TEST_HEIGHT) / 2) - 2
        self.surface.draw_circle(pos, radius, pymlgame.GREEN, None, 1.0)

    def test_blit(self):
        surface = pymlgame.Surface(TEST_WIDTH - 2, TEST_HEIGHT - 2)
        surface.fill(pymlgame.WHITE, 1.0)
        self.surface.blit(surface, (1, 1))

        for x in range(TEST_WIDTH):
            for y in range(TEST_HEIGHT):
                if 0 < x < TEST_WIDTH - 1 and 0 < y < TEST_HEIGHT - 1:
                    self.assertEqual(self.surface.matrix[x][y], pymlgame.WHITE)
                else:
                    self.assertEqual(self.surface.matrix[x][y], pymlgame.BLACK)

    def test_get_color(self):
        self.assertEqual(pymlgame.Surface.get_color(pymlgame.GREEN, 1.0),
                         pymlgame.GREEN)
        self.assertEqual(pymlgame.Surface.get_color(pymlgame.WHITE, 0.0),
                         pymlgame.BLACK)
        self.assertEqual(pymlgame.Surface.get_color(pymlgame.WHITE, 0.5),
                         tuple([math.floor(val * 0.5)
                                for val in pymlgame.WHITE]))


class ClockTest(unittest.TestCase):
    def setUp(self):
        self.clock = pymlgame.Clock()

    def test_tick(self):
        before = time.time()
        self.clock.tick(24)
        after = time.time()
        self.assertGreater(after, before)
        self.assertAlmostEqual(before, after - 1/24, 2)


if __name__ == '__main__':
    unittest.main()