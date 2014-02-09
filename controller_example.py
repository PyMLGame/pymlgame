#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
pymlgame - controller example
=============================

This example shows how you can use a controller connected to a laptop or any
other machine capable of pygame to connect to a pymlgame instance.
"""

__author__ = "Ricardo Band"
__copyright__ = "Copyright 2013, Ricardo Band"
__credits__ = ["Ricardo Band"]
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Ricardo Band"
__email__ = "me@xengi.de"
__status__ = "Development"

import sys

import pygame
import jsonrpclib


class Controller(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        pygame.init()
        self.joysticks = [[pygame.joystick.Joystick(j), None, None]
                          for j in range(pygame.joystick.get_count())]
        self.screen = pygame.display.set_mode((100, 10))
        pygame.display.set_caption("pymlgame_ctlr")
        self.clock = pygame.time.Clock()
        self.server = jsonrpclib.Server('http://' + self.host + ':' +
                                        str(self.port))
        for joy in self.joysticks:
            joy[0].init()
            joy[1] = self.server.init()
            if joy[0].get_name() == 'Xbox 360 Wireless Receiver':
                joy[2] = {0: 'A',
                          1: 'B',
                          2: 'X',
                          3: 'Y',
                          4: 'L1',
                          5: 'R1',
                          6: 'Select',
                          7: 'Start',
                          11: 'Left',
                          12: 'Right',
                          13: 'Up',
                          14: 'Down'}

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.joystick.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
            if event.type == pygame.JOYBUTTONDOWN:
                print('joy', self.joysticks[event.joy][0].get_name(),
                      '(uid:', self.joysticks[event.joy][1], ')button pressed:',
                      event.button)
                self.server.trigger_button(self.joysticks[event.joy][1],
                                           'KeyDown',
                                           self.joysticks[event.joy][2][event.button])
            if event.type == pygame.JOYBUTTONUP:
                print('joy', self.joysticks[event.joy][0].get_name(),
                      '(uid:', self.joysticks[event.joy][1], ')button released:',
                      event.button)
                self.server.trigger_button(self.joysticks[event.joy][1],
                                           'KeyUp',
                                           self.joysticks[event.joy][2][event.button])

    def update(self):
        pass

    def render(self):
        pygame.display.update()
        pygame.display.flip()

    def gameloop(self):
        try:
            while True:
                self.handle_events()
                self.update()
                self.render()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    CTLR = Controller('127.0.0.1', 1338)
    CTLR.gameloop()
