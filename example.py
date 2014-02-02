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
        self.screen = pymlgame.Screen(ip='127.0.0.1', port=1337)
        self.clock = pymlgame.Clock()
        self.running = True
        self.colors = [GREEN, WHITE, RED, YELLOW, BLUE, CYAN]

    def update(self):
        """
        Update the screens contents in every loop
        """
        self.screen.fill(BLACK)
        self.screen.draw_dot((0, 0), self.colors[0])
        self.screen.draw_dot((self.screen.width - 1, 0), self.colors[0])
        self.screen.draw_dot((self.screen.width - 1, self.screen.height - 1), self.colors[0])
        self.screen.draw_dot((0, self.screen.height - 1), self.colors[0])
        self.screen.draw_line((1, 1), (38, 14), self.colors[1])
        self.screen.draw_rect((2, 2), (36, 12), self.colors[2], self.colors[3])
        self.screen.draw_circle((20, 5), 8, self.colors[4], self.colors[5])

    def render(self):
        """
        Send the current screen content to Mate Light
        """
        self.screen.update()
        self.clock.tick(10)

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