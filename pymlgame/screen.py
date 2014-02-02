# -*- coding: utf-8 -*-

"""
pymlgame - Screen
"""

__author__ = "Ricardo Band"
__copyright__ = "Copyright 2013, Ricardo Band"
__credits__ = ["Ricardo Band"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Ricardo Band"
__email__ = "me@xengi.de"
__status__ = "Development"

import math
import socket

from pymlgame.locals import *


class Screen(object):
    """
    Represents the Mate Light screen and has all the drawing methods.
    """
    def __init__(self, ip, port, width=40, height=16, brightness=0.1):
        """
        Create a screen with default size and fill it with black pixels.
        """
        self.ip = ip
        self.port = port
        self.width = width
        self.height = height
        self.brightness = brightness
        self.__matrix = []
        self.fill(BLACK)

    def fill(self, color):
        """
        Fill the whole screen with the given color.
        """
        self.__matrix = [[color for y in range(self.height)] for x in range(self.width)]

    def draw_dot(self, pos, color):
        """
        Draw one single dot with the given color on the screen.
        """
        if 0 <= pos[0] < self.width and 0 <= pos[1] < self.height:
            self.__matrix[pos[0]][pos[1]] = color
        else:
            print('{:d},{:d} is outside the screen'.format(pos[0], pos[1]))

    def draw_line(self, start, end, color):
        """
        Draw a line with the given color on the screen.
        """
        def dist(point, start, end):
            x = point[0]
            y = point[1]
            a = abs((end[0] - start[0]) * (start[1] - y) - (start[0] - x) * (end[1] - start[1]))
            b = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            result = a / b
            return result
        points = []
        for x in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
            for y in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                if dist((x, y), start, end) < 0.5:
                    points.append((x, y))
        for point in points:
            self.draw_dot((point[0], point[1]), color)

    def draw_rect(self, pos, size, color, fillcolor=None):
        """
        Draw a rectangle with the given color on the screen and optionally fill it with fillcolor.
        """
        # draw top and botton line
        for x in range(size[0]):
            self.draw_dot((pos[0] + x, pos[1]), color)
            self.draw_dot((pos[0] + x, pos[1] + size[1] - 1), color)
        # draw left and right side
        for y in range(size[1]):
            self.draw_dot((pos[0], pos[1] + y), color)
            self.draw_dot((pos[0] + size[0] - 1, pos[1] + y), color)
        # draw filled rect
        if fillcolor:
            for x in range(size[0] - 2):
                for y in range(size[1] - 2):
                    self.draw_dot((pos[0] + 1 + x, pos[1] + 1 + y), fillcolor)

    def draw_circle(self, pos, radius, color, fillcolor):
        """
        Draw a circle with the given color on the screen and optionally fill it with fillcolor.
        """
        def dist(point, pos):
            return abs(math.sqrt((pos[0] - point[0])**2 + (pos[1] - point[1])**2) - radius)

        # draw outline
        points = []
        for x in range(pos[0] - radius, pos[0] + radius):
            for y in range(pos[1] - radius, pos[1] + radius):
                if 0 < x < self.width and 0 < y < self.height:
                    if dist((x, y), pos) < 1:
                        self.draw_dot((x, y), color)
                        points.append((x, y))

        # draw fill color
        for point in points:
            pass

        print(points)

    def update(self):
        """
        Sends the current screen contents to Mate Light
        """
        display_data = []
        for y in range(self.height):
            for x in range(self.width):
                for color in self.__matrix[x][y]:
                    display_data.append(int(color * self.brightness))

        checksum = bytearray([0, 0, 0, 0])
        data_as_bytes = bytearray(display_data)
        data = data_as_bytes + checksum
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(data, (self.ip, self.port))
