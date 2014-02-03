# -*- coding: utf-8 -*-

"""
pymlgame - Surface
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

from pymlgame.locals import *


class Surface(object):
    """
    Represents a sheet to draw on
    """
    def __init__(self, size):
        """
        Create a surface with default size and fill it with black pixels.
        """
        self.width = size[0]
        self.height = size[1]
        self.matrix = []
        self.fill(BLACK)

    def fill(self, color, brightness=0.1):
        """
        Fill the whole screen with the given color.
        """
        color = [val * brightness for val in color]
        self.matrix = [[color for y in range(self.height)] for x in range(self.width)]

    def draw_dot(self, pos, color, brightness=0.1):
        """
        Draw one single dot with the given color on the screen.
        """
        color = [val * brightness for val in color]
        if 0 <= pos[0] < self.width and 0 <= pos[1] < self.height:
            self.matrix[pos[0]][pos[1]] = color
        else:
            print('{:d},{:d} is outside the screen'.format(pos[0], pos[1]))

    def draw_line(self, start, end, color, brightness=0.1):
        """
        Draw a line with the given color on the screen.
        """
        def dist(point, start, end):
            return abs((end[0] - start[0]) * (start[1] - point[1]) -
                       (start[0] - point[0]) * (end[1] - start[1])) / math.sqrt((end[0] - start[0])**2 +
                                                                                (end[1] - start[1])**2)

        color = [val * brightness for val in color]
        points = []
        for x in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
            for y in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                if dist((x, y), start, end) < 0.5:
                    points.append((x, y))
        for point in points:
            self.draw_dot((point[0], point[1]), color)

    def draw_rect(self, pos, size, color, fillcolor=None, brightness=0.1):
        """
        Draw a rectangle with the given color on the screen and optionally fill it with fillcolor.
        """
        color = [val * brightness for val in color]
        fillcolor = [val * brightness for val in fillcolor]
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

    def draw_circle(self, pos, radius, color, fillcolor=None, brightness=0.1):
        """
        Draw a circle with the given color on the screen and optionally fill it with fillcolor.
        """
        def dist(point, pos):
            return abs(math.sqrt((pos[0] - point[0])**2 + (pos[1] - point[1])**2) - radius)

        color = [val * brightness for val in color]
        fillcolor = [val * brightness for val in fillcolor]
        # draw outline
        points = []
        for x in range(pos[0] - radius, pos[0] + radius):
            for y in range(pos[1] - radius, pos[1] + radius):
                if 0 < x < self.width and 0 < y < self.height:
                    if dist((x, y), pos) < 1:
                        self.draw_dot((x, y), color)
                        points.append((x, y))

        # draw fill color
        if fillcolor:
            for point in points:
                pass