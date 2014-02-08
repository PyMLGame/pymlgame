#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-

"""
pymlgame example game
"""

__author__ = "Ricardo Band"
__copyright__ = "Copyright 2013, Ricardo Band"
__credits__ = ["Ricardo Band"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Ricardo Band"
__email__ = "me@xengi.de"
__status__ = "Development"

import pymlgame


class Game(object):
    """
    The main game class that holds the gameloop
    """
    def __init__(self, host, port, width, height):
        """
        Create a screen and define some game specific things
        """
        self.screen = pymlgame.Screen(host, port, width, height)
        self.clock = pymlgame.Clock()
        self.running = True
        self.colors = [pymlgame.WHITE,
                       pymlgame.BLUE,
                       pymlgame.GREEN,
                       pymlgame.CYAN,
                       pymlgame.MAGENTA,
                       pymlgame.YELLOW,
                       pymlgame.RED]

        # surfaces
        self.corners = pymlgame.Surface(self.screen.width, self.screen.height)
        self.lines = pymlgame.Surface(int(self.screen.width / 2) - 2,
                                      int(self.screen.height / 2) - 2)
        self.rects = pymlgame.Surface(int(self.screen.width / 2) - 2,
                                      int(self.screen.height / 2) - 2)
        self.circle = pymlgame.Surface(int(self.screen.width / 2) - 2,
                                       int(self.screen.height / 2) - 2)
        self.filled = pymlgame.Surface(int(self.screen.width / 2) - 2,
                                       int(self.screen.height / 2) - 2)

    def update(self):
        """
        Update the screens contents in every loop
        """
        # this is not really neccesary because the surface is black after
        # initializing

        self.corners.fill(pymlgame.BLACK)
        self.corners.draw_dot((0, 0), self.colors[0])
        self.corners.draw_dot((self.screen.width - 1, 0), self.colors[0])
        self.corners.draw_dot((self.screen.width - 1, self.screen.height - 1),
                              self.colors[0])
        self.corners.draw_dot((0, self.screen.height - 1), self.colors[0])

        self.lines.fill(pymlgame.BLACK)
        self.lines.draw_line((1, 0), (self.lines.width - 1, 0), self.colors[1])
        self.lines.draw_line((0, 1), (0, self.lines.height - 1), self.colors[3])
        self.lines.draw_line((0, 0), (self.lines.width - 1,
                                      self.lines.height - 1), self.colors[2])

        self.rects.fill(pymlgame.BLACK)
        self.rects.draw_rect((0, 0), (int(self.rects.width / 2) - 1,
                                      self.rects.height),
                             self.colors[2], self.colors[3])
        self.rects.draw_rect((int(self.rects.width / 2) + 1, 0),
                             (int(self.rects.width / 2) - 1,
                              self.rects.height),
                             self.colors[3], self.colors[2])

        self.circle.fill(pymlgame.BLACK)
        radius = int(min(self.circle.width, self.circle.height) / 2) - 1
        self.circle.draw_circle((int(self.circle.width / 2) - 1,
                                 int(self.circle.height / 2) - 1), radius,
                                self.colors[4], self.colors[5])

        self.filled.fill(self.colors[6])

    def render(self):
        """
        Send the current screen content to Mate Light
        """
        self.screen.reset()
        self.screen.blit(self.corners)
        self.screen.blit(self.lines, (1, 1))
        self.screen.blit(self.rects, (int(self.screen.width / 2) + 1, 1))
        self.screen.blit(self.circle, (0, int(self.screen.height / 2) + 1))
        self.screen.blit(self.filled, (int(self.screen.width / 2) + 1,
                                       int(self.screen.height / 2) + 1))

        self.screen.update()
        self.clock.tick(2)

    def handle_events(self):
        """
        Loop through all events
        """
        self.colors.append(self.colors.pop(0))

    def gameloop(self):
        """
        A game loop that circles through the methods
        """
        try:
            while True:
                self.handle_events()
                self.update()
                self.render()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    GAME = Game('127.0.0.1', 1337, 40, 40)
    GAME.gameloop()