#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-

"""
pymlgame - Unittests
"""

__author__ = 'Ricardo Band'
__copyright__ = 'Copyright 2014, Ricardo Band'
__credits__ = ['Ricardo Band']
__license__ = 'MIT'
__version__ = '0.1.1'
__maintainer__ = 'Ricardo Band'
__email__ = 'me@xengi.de'
__status__ = 'Development'

import time
import random
import unittest

import pymlgame

TEST_HOST = 'localhost'
TEST_RPC_HOST = 'localhost'
TEST_PORT = 1337
TEST_RPC_PORT = 1338
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
        surface.fill(pymlgame.MAGENTA)
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
        self.assertEqual(self.screen.matrix[TEST_WIDTH - 1][TEST_HEIGHT - 1], pymlgame.BLACK)

    def test_update(self):
        pass

    def test_blit(self):
        surface = pymlgame.Surface(TEST_WIDTH - 2, TEST_HEIGHT - 2)
        surface.fill(pymlgame.WHITE)
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
        self.assertEqual(self.surface.matrix[TEST_WIDTH - 1][TEST_HEIGHT - 1], pymlgame.BLACK)

    def test_fill(self):
        self.surface.fill(pymlgame.BLUE)

        self.assertEqual(self.surface.matrix[0][0], pymlgame.BLUE)
        self.assertEqual(self.surface.matrix[TEST_WIDTH - 1][0], pymlgame.BLUE)
        self.assertEqual(self.surface.matrix[0][TEST_HEIGHT - 1], pymlgame.BLUE)
        self.assertEqual(self.surface.matrix[TEST_WIDTH - 1][TEST_HEIGHT - 1], pymlgame.BLUE)
        for _ in range(10):
            self.assertEqual(self.surface.matrix[random.randrange(0, TEST_WIDTH)][random.randrange(0, TEST_HEIGHT)],
                             pymlgame.BLUE)

    def test_draw_dot(self):
        # create 10 random dots
        randpoints = [(random.randrange(0, TEST_WIDTH), random.randrange(0, TEST_HEIGHT)) for _ in range(10)]
        # draw the dots
        for point in randpoints:
            self.surface.draw_dot(point, pymlgame.YELLOW)
        # test if drawing was successful
        for x in range(TEST_WIDTH):
            for y in range(TEST_HEIGHT):
                color = self.surface.matrix[x][y]
                if (x, y) in randpoints:
                    self.assertEqual(color, pymlgame.YELLOW)
                else:
                    self.assertEqual(color, pymlgame.BLACK)

    def test_draw_line(self):
        self.surface.draw_line((1, 0), (TEST_WIDTH - 1, 0), pymlgame.GREY6)
        self.surface.draw_line((0, 1), (0, TEST_HEIGHT - 1), pymlgame.RED)
        test_len = max(TEST_WIDTH, TEST_HEIGHT)
        self.surface.draw_line((test_len - 2, test_len - 2), (2, 2), pymlgame.CYAN)

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
        self.surface.draw_rect((1, 1), (TEST_WIDTH - 2, TEST_HEIGHT - 2), pymlgame.DARKYELLOW, None)

        for x in range(TEST_WIDTH):
            for y in range(TEST_HEIGHT):
                if x == 1 and 0 < y < TEST_HEIGHT - 1 or \
                   x == TEST_WIDTH - 2 and 0 < y < TEST_HEIGHT - 1 or \
                   TEST_WIDTH - 2 > x > 1 == y or \
                   1 < x < TEST_WIDTH - 2 and y == TEST_HEIGHT - 2:
                    self.assertEqual(self.surface.matrix[x][y], pymlgame.DARKYELLOW, '{},{}'.format(x, y))
                else:
                    self.assertEqual(self.surface.matrix[x][y], pymlgame.BLACK)

        self.surface.fill(pymlgame.BLACK)
        self.surface.draw_rect((int(TEST_WIDTH / 2) + 1, int(TEST_HEIGHT / 2) + 1),
                               (1, 1), pymlgame.MAGENTA, pymlgame.DARKCYAN)

    def test_draw_circle(self):
        #TODO: invent a way to draw this, then a way to test this
        pos = (int(TEST_WIDTH / 2) - 1, int(TEST_HEIGHT / 2) - 1)
        radius = int(min(TEST_WIDTH, TEST_HEIGHT) / 2) - 2
        self.surface.draw_circle(pos, radius, pymlgame.GREEN, None)

    def test_blit(self):
        surface = pymlgame.Surface(TEST_WIDTH - 2, TEST_HEIGHT - 2)
        surface.fill(pymlgame.WHITE)
        self.surface.blit(surface, (1, 1))

        for x in range(TEST_WIDTH):
            for y in range(TEST_HEIGHT):
                if 0 < x < TEST_WIDTH - 1 and 0 < y < TEST_HEIGHT - 1:
                    self.assertEqual(self.surface.matrix[x][y], pymlgame.WHITE)
                else:
                    self.assertEqual(self.surface.matrix[x][y], pymlgame.BLACK)


class ClockTest(unittest.TestCase):
    def setUp(self):
        self.clock = pymlgame.Clock()

    def test_tick(self):
        before = time.time()
        self.clock.tick(24)
        after = time.time()
        self.assertGreater(after, before)
        self.assertAlmostEqual(before, after - 1/24, 2)


class Controllertests(unittest.TestCase):
    def setUp(self):
        self.controller = pymlgame.Controller(TEST_RPC_HOST, TEST_RPC_PORT)
        self.server = jsonrpclib.Server('http://{}:{}'.format(TEST_RPC_HOST, TEST_RPC_PORT))

    def tearDown(self):
        self.controller.quit()
        # just wait a second for the socket to close
        time.sleep(1)

    def test_uid(self):
        uid1 = self.server.init()
        uid2 = self.server.init()
        uid3 = self.server.init()
        self.assertGreater(uid3, uid2)
        self.assertGreater(uid2, uid1)

    def test_button_keys(self):
        keys = self.server.get_button_keys()
        self.assertGreater(len(keys), 0)
        self.assertEqual(len(keys), len(self.controller._mapping.keys()))

    def test_event_keys(self):
        keys = self.server.get_event_keys()
        self.assertGreater(len(keys), 0)
        self.assertEqual(len(keys), len(self.controller._events.keys()))

    def test_ping(self):
        self.assertEqual(len(self.controller.queue), 0)
        uid = self.server.init()
        self.assertEqual(len(self.controller.queue), 1)

        self.server.ping(uid)
        self.assertEqual(len(self.controller.queue), 2)
        self.assertEqual(self.controller.queue[1].type, pymlgame.PING)
        self.assertEqual(self.controller.queue[1].uid, uid)

    def test_trigger_button(self):
        self.assertEqual(len(self.controller.queue), 0)
        uid = self.server.init()
        self.assertEqual(len(self.controller.queue), 1)

        self.server.trigger_button(uid, 'KeyDown', 'Up')
        self.server.trigger_button(uid, 'KeyUp', 'Up')
        self.server.trigger_button(uid, 'KeyDown', 'Down')
        self.server.trigger_button(uid, 'KeyUp', 'Down')
        self.server.trigger_button(uid, 'KeyDown', 'Left')
        self.server.trigger_button(uid, 'KeyUp', 'Left')
        self.server.trigger_button(uid, 'KeyDown', 'Right')
        self.server.trigger_button(uid, 'KeyUp', 'Right')
        self.server.trigger_button(uid, 'KeyDown', 'A')
        self.server.trigger_button(uid, 'KeyUp', 'A')
        self.server.trigger_button(uid, 'KeyDown', 'B')
        self.server.trigger_button(uid, 'KeyUp', 'B')
        self.server.trigger_button(uid, 'KeyDown', 'X')
        self.server.trigger_button(uid, 'KeyUp', 'X')
        self.server.trigger_button(uid, 'KeyDown', 'Y')
        self.server.trigger_button(uid, 'KeyUp', 'Y')
        self.server.trigger_button(uid, 'KeyDown', 'Start')
        self.server.trigger_button(uid, 'KeyUp', 'Start')
        self.server.trigger_button(uid, 'KeyDown', 'Select')
        self.server.trigger_button(uid, 'KeyUp', 'Select')
        self.server.trigger_button(uid, 'KeyDown', 'R1')
        self.server.trigger_button(uid, 'KeyUp', 'R1')
        self.server.trigger_button(uid, 'KeyDown', 'R2')
        self.server.trigger_button(uid, 'KeyUp', 'R2')
        self.server.trigger_button(uid, 'KeyDown', 'L1')
        self.server.trigger_button(uid, 'KeyUp', 'L1')
        self.server.trigger_button(uid, 'KeyDown', 'L2')
        self.server.trigger_button(uid, 'KeyUp', 'L2')

        self.assertEqual(len(self.controller.queue), 29)


if __name__ == '__main__':
    unittest.main()