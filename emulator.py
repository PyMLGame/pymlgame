#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
pymlgame - Mate Light emulator
==============================

This little program emulates the awesome Mate Light, just in case you're not on c-base space station but want to send
something to it.

Usage:
  emulator.py [-w=<px>] [-h=<px>] [--host=<ip>] [--port=<num>] [--dot=<size>]
  emulator.py --help
  emulator.py --version

Options:
  --help         Show this screen.
  --version      Show version.
  -w=<px>        Width in pixels [default: 40].
  -h=<px>        Height in pixels [default: 16].
  --host=<host>  Bind to IP address [default: 127.0.0.1].
  --port=<port>  Bind to Port [default: 1337].
  --dot=<px>     Size of dots in pixels [default: 10].
"""

__author__ = 'Ricardo Band'
__copyright__ = 'Copyright 2014, Ricardo Band'
__credits__ = ['Ricardo Band']
__license__ = 'MIT'
__version__ = '0.3.0'
__maintainer__ = 'Ricardo Band'
__email__ = 'me@xengi.de'
__status__ = 'Development'

import sys
import socket

import pygame
from docopt import docopt


class Emu(object):
    """
    The Emulator is a simple pygame game.
    """
    def __init__(self, width=40, height=16, ip='127.0.0.1', port=1337, dotsize=10):
        """
        Creates a screen with the given size, generates the matrix for the Mate bottles and binds the socket for
        incoming frames.
        """
        self.width = width
        self.height = height
        self.dotsize = dotsize
        pygame.init()
        self.screen = pygame.display.set_mode([self.width * self.dotsize, self.height * self.dotsize])
        pygame.display.set_caption("Mate Light Emu")
        self.clock = pygame.time.Clock()
        self.matrix = []
        for c in range(self.width * self.height * 3):
            # fill matrix with black color
            self.matrix.append(0)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))
        # size is width * height * 3 (rgb) + 4 (checksum)
        self.packetsize = self.width * self.height * 3 + 4

    def recv_data(self):
        """
        Grab the next frame and put it on the matrix.
        """
        data, addr = self.sock.recvfrom(self.packetsize)
        matrix = map(ord, data.strip())
        if len(matrix) == self.packetsize:
            self.matrix = matrix[:-4]

    def update(self):
        """
        Generate the output from the matrix.
        """
        pixels = len(self.matrix)
        for x in range(self.width):
            for y in range(self.height):
                pixel = y * self.width * 3 + x * 3
                #TODO: sometimes the matrix is not as big as it should
                if pixel < pixels:
                    pygame.draw.circle(self.screen,
                                       (self.matrix[pixel], self.matrix[pixel + 1], self.matrix[pixel + 2]),
                                       (x * self.dotsize + self.dotsize / 2, y * self.dotsize + self.dotsize / 2), self.dotsize / 2, 0)

    def render(self):
        """
        Output the current screen.
        """
        pygame.display.update()
        pygame.display.flip()

    def gameloop(self):
        """
        Loop through all the necessary stuff and end execution when Ctrl+C was hit.
        """
        try:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.event.post(pygame.event.Event(pygame.QUIT))

                self.recv_data()
                self.update()
                self.render()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    ARGS = docopt(__doc__, version=__version__)
    EMU = Emu(int(ARGS['-w']), int(ARGS['-h']), ARGS['--host'], int(ARGS['--port']), int(ARGS['--dot']))
    EMU.gameloop()
