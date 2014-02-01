# -*- coding: utf-8 -*-

import socket

from pymlgame.locals import *


class Screen(object):
    """
    Represents the Mate Light screen and has all the drawing methods.
    """
    def __init__(self, width=40, height=16):
        """
        Create a screen with default size and fill it with black pixels.
        """
        self.width = width
        self.height = height
        self.__matrix = []
        self.fill(BLACK)

    def fill(self, color):
        """
        Fill the whole screen with the given color.
        """
        self.__matrix = []
        for x in range(self.width):
            column = []
            for y in range(self.height):
                column.append(color)
            self.__matrix.append(column)

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
        pass

    def draw_rect(self, pos, size, color, fillcolor=None):
        """
        Draw a rectangle with the given color on the screen and optionally fill it with fillcolor.
        """
        # draw top and botton line
        for x in range(size[0]):
            self.draw_dot((pos[0] + x, pos[1]), color)
            self.draw_dot((pos[0] + x, pos[1] + size[1]), color)
        # draw left and right side
        for y in range(size[1]):
            self.draw_dot((pos[0], pos[1] + y), color)
            self.draw_dot((pos[0] + size[0], pos[1] + y), color)
        # draw filled rect
        if fillcolor:
            for x in range(size[0] - 2):
                for y in range(size[1] - 2):
                    self.draw_dot((pos[0] + 1 + x, pos[1] + 1 + y), fillcolor)

    def draw_circle(self, pos, size, color, fillcolor):
        """
        Draw a circle with the given color on the screen and optionally fill it with fillcolor.
        """
        pass

    def update(self):
        """
        Sends the current screen contents to Mate Light
        """
        display_data = []
        for y in range(self.width):
            for x in range(self.heigth):
                for color in self.__matrix[x][y]:
                    display_data.append(color)

        checksum = bytearray([0, 0, 0, 0])
        data_as_bytes = bytearray(display_data)
        data = data_as_bytes + checksum
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(data, (self.ip, self.port))
