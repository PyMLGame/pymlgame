#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
pymlgame - example game
=======================

This example shows how a simple pymlgame could be written. You also need a connected controller to actually see
something happening. You can use the controller example for this.
"""

__author__ = 'Ricardo Band'
__copyright__ = 'Ricardo Band'
__credits__ = ['Ricardo Band']
__license__ = 'MIT'
__version__ = '0.3.1'
__maintainer__ = 'Ricardo Band'
__email__ = 'email@ricardo.band'
__status__ = 'Development'

from datetime import datetime

import pymlgame
from pymlgame.locals import WHITE, BLUE, GREEN, CYAN, MAGENTA, YELLOW, RED, BLACK, E_NEWCTLR, E_DISCONNECT, E_KEYDOWN, E_KEYUP, E_PING
from pymlgame.screen import Screen
from pymlgame.clock import Clock
from pymlgame.surface import Surface


class Game(object):
    """
    The main game class that holds the gameloop.
    """
    def __init__(self, host, port, width, height):
        """
        Create a screen and define some game specific things.
        """
        self.host = host
        self.port = port
        self.width = width
        self.height = height

        self.players = {}

        pymlgame.init()
        self.screen = Screen(self.host, self.port,
                             self.width, self.height)
        self.clock = Clock(15)
        self.running = True
        self.colors = [WHITE, BLUE, GREEN, CYAN, MAGENTA, YELLOW, RED]

        # surfaces
        self.corners = Surface(self.screen.width, self.screen.height)
        self.lines = Surface(int(self.screen.width / 2) - 2,
                             int(self.screen.height / 2) - 2)
        self.rects = Surface(int(self.screen.width / 2) - 2,
                             int(self.screen.height / 2) - 2)
        self.circle = Surface(int(self.screen.width / 2) - 2,
                              int(self.screen.height / 2) - 2)
        self.filled = Surface(int(self.screen.width / 2) - 2,
                              int(self.screen.height / 2) - 2)

    def update(self):
        """
        Update the screens contents in every loop.
        """
        # this is not really neccesary because the surface is black after initializing
        self.corners.fill(BLACK)
        self.corners.draw_dot((0, 0), self.colors[0])
        self.corners.draw_dot((self.screen.width - 1, 0), self.colors[0])
        self.corners.draw_dot((self.screen.width - 1, self.screen.height - 1),
                              self.colors[0])
        self.corners.draw_dot((0, self.screen.height - 1), self.colors[0])

        self.lines.fill(BLACK)
        self.lines.draw_line((1, 0), (self.lines.width - 1, 0), self.colors[1])
        self.lines.draw_line((0, 1), (0, self.lines.height - 1), self.colors[3])
        self.lines.draw_line((0, 0), (self.lines.width - 1,
                                      self.lines.height - 1), self.colors[2])

        self.rects.fill(BLACK)
        self.rects.draw_rect((0, 0), (int(self.rects.width / 2) - 1,
                                      self.rects.height),
                             self.colors[2], self.colors[3])
        self.rects.draw_rect((int(self.rects.width / 2) + 1, 0),
                             (int(self.rects.width / 2) - 1,
                              self.rects.height),
                             self.colors[3], self.colors[2])

        self.circle.fill(BLACK)
        radius = int(min(self.circle.width, self.circle.height) / 2) - 1
        self.circle.draw_circle((int(self.circle.width / 2) - 1,
                                 int(self.circle.height / 2) - 1), radius,
                                self.colors[4], self.colors[5])

        self.filled.fill(self.colors[6])

    def render(self):
        """
        Send the current screen content to Mate Light.
        """
        self.screen.reset()
        self.screen.blit(self.corners)
        self.screen.blit(self.lines, (1, 1))
        self.screen.blit(self.rects, (int(self.screen.width / 2) + 1, 1))
        self.screen.blit(self.circle, (0, int(self.screen.height / 2) + 1))
        self.screen.blit(self.filled, (int(self.screen.width / 2) + 1,
                                       int(self.screen.height / 2) + 1))

        self.screen.update()
        self.clock.tick()

    def handle_events(self):
        """
        Loop through all events.
        """
        for event in pymlgame.get_events():
            if event.type == E_NEWCTLR:
                #print(datetime.now(), '### new player connected with uid', event.uid)
                self.players[event.uid] = {'name': 'alien_{0}'.format(event.uid), 'score': 0}
            elif event.type == E_DISCONNECT:
                #print(datetime.now(), '### player with uid {} disconnected'.format(event.uid))
                self.players.pop(event.uid)
            elif event.type == E_KEYDOWN:
                #print(datetime.now(), '###', self.players[event.uid]['name'], 'pressed', event.button)
                self.colors.append(self.colors.pop(0))
            elif event.type == E_KEYUP:
                #print(datetime.now(), '###', self.players[event.uid]['name'], 'released', event.button)
                self.colors.append(self.colors.pop(0))
            elif event.type == E_PING:
                #print(datetime.now(), '### ping from', self.players[event.uid]['name'])
                pass

    def gameloop(self):
        """
        A game loop that circles through the methods.
        """
        try:
            while True:
                self.handle_events()
                self.update()
                self.render()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    GAME = Game('127.0.0.1', 1337, 40, 16)
    #GAME = Game('matelight.cbrp3.c-base.org', 1337, 40, 16)
    GAME.gameloop()
