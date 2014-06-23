# -*- coding: utf-8 -*-

"""
pymlgame - Surface
"""

import math

from pymlgame.locals import *


class Surface(object):
    """
    Represents a sheet to draw on
    """
    def __init__(self, width, height):
        """
        Create a surface with default size and fill it with black pixels.
        """
        self.width = width
        self.height = height
        self.matrix = None
        self.fill(BLACK)

    def fill(self, color):
        """
        Fill the whole screen with the given color.
        """
        self.matrix = [[color for _ in range(self.height)] for _ in range(self.width)]

    def draw_dot(self, pos, color):
        """
        Draw one single dot with the given color on the screen.
        """
        if 0 <= pos[0] < self.width and 0 <= pos[1] < self.height:
            self.matrix[pos[0]][pos[1]] = color

    def draw_line(self, start, end, color):
        """
        Draw a line with the given color on the screen.
        """
        def dist(p, a, b):
            return (abs((b[0] - a[0]) * (a[1] - p[1]) - (a[0] - p[0]) * (b[1] - a[1])) /
                    math.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2))

        points = []
        for x in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
            for y in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                if dist((x, y), start, end) < 0.5:
                    points.append((x, y))
        for point in points:
            self.draw_dot(point, color)

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
        if fillcolor and size[0] >= 3 and size[1] >= 3:
            for x in range(size[0] - 2):
                for y in range(size[1] - 2):
                    self.draw_dot((pos[0] + 1 + x, pos[1] + 1 + y), fillcolor)

    def draw_circle(self, pos, radius, color, fillcolor=None):
        """
        Draw a circle with the given color on the screen and optionally fill it with fillcolor.
        """
        #TODO: This still produces rubbish but it's on a good way to success
        def dist(d, p, r):
            return abs(math.sqrt((p[0] - d[0])**2 + (p[1] - d[1])**2) - r)

        points = []
        for x in range(pos[0] - radius, pos[0] + radius):
            for y in range(pos[1] - radius, pos[1] + radius):
                if 0 < x < self.width and 0 < y < self.height:
                    if dist((x, y), pos, radius) < 1.3:
                        points.append((x, y))

        # draw fill color
        if fillcolor:
            for point in points:
                pass
        # draw outline
        for point in points:
            self.draw_dot(point, color)

    def blit(self, surface, pos=(0, 0)):
        """
        Blits a surface on this surface at pos
        """
        for x in range(surface.width):
            for y in range(surface.height):
                px = x + pos[0]
                py = y + pos[1]
                if 0 < px < self.width and 0 < py < self.height:
                    self.matrix[px][py] = surface.matrix[x][y]

    def replace_color(self, before, after):
        """
        Replaces a color on a surface with another one.
        """
        #TODO: find a faster way to do this (maybe a nice list comprehension?)
        for x in range(self.width):
            for y in range(self.height):
                if self.matrix[x][y] == before:
                    self.matrix[x][y] = after