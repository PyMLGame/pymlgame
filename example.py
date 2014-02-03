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
from pymlgame.locals import *


class Game(object):
    """
    The main game class that holds the gameloop
    """
    def __init__(self):
        """
        Create a screen and define some game specific things
        """
        self.screen = pymlgame.Screen(host='127.0.0.1', port=1337)
        self.clock = pymlgame.Clock()
        self.running = True
        self.colors = [GREEN, WHITE, RED, YELLOW, BLUE, CYAN]

    def update(self):
        """
        Update the screens contents in every loop
        """
        # this is not really neccesary because the screen is black after initializing
        bg = pymlgame.Surface((self.screen.width, self.screen.height))
        bg.fill(BLACK)

        corners = pymlgame.Surface((self.screen.width, self.screen.height))
        corners.draw_dot((0, 0), self.colors[0])
        corners.draw_dot((self.screen.width - 1, 0), self.colors[0])
        corners.draw_dot((self.screen.width - 1, self.screen.height - 1), self.colors[0])
        corners.draw_dot((0, self.screen.height - 1), self.colors[0])

        lines = pymlgame.Surface((38, 14))
        lines.draw_line((0, 0), (37, 13), self.colors[1])
        lines.draw_line((13, 0), (37, 0), self.colors[1])

        rectangles = pymlgame.Surface((22, 10))
        rectangles.draw_rect((0, 0), (10, 10), self.colors[2], self.colors[3])
        rectangles.draw_rect((12, 0), (10, 10), self.colors[3], self.colors[2])

        circles = pymlgame.Surface((10, 10))
        circles.draw_circle((4, 4), 4, self.colors[4], self.colors[5])

        self.screen.blit(bg)
        self.screen.blit(corners)
        self.screen.blit(lines, (1, 1))
        #self.screen.blit(rectangles, (3, 3))
        #self.screen.blit(circles, (27, 3))

    def render(self):
        """
        Send the current screen content to Mate Light
        """
        self.screen.update()
        self.clock.tick(5)

    def handle_events(self):
        """
        Loop through all events and react to them
        """
        for event in pymlgame.events.get_events():
            #print(event)
            #if event['type'] == KEYUP:
            #    if event['key'] == K_Arrow_Up or event['key'] == K_Arrow_Right:
            #        self.colors.append(self.colors.pop(0))
            #    elif event['key'] == K_Arrow_Down or event['key'] == K_Arrow_Left:
            #        self.colors.insert(0, self.colors.pop())
            pass
        self.colors.append(self.colors.pop(0))

    def gameloop(self):
        """
        A game loop that circles through the methods
        """
        while self.running:
            self.handle_events()
            self.update()
            self.render()


if __name__ == '__main__':
    GAME = Game()
    GAME.gameloop()