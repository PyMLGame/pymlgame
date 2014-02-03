#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Mate Light emulator
"""

__author__ = "Ricardo Band"
__copyright__ = "Copyright 2013, Ricardo Band"
__credits__ = ["Ricardo Band"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Ricardo Band"
__email__ = "me@xengi.de"
__status__ = "Development"

import sys
import socket

import pygame


class Emu(object):
    def __init__(self, width=40, height=16, ip='127.0.0.1', port=1337):
        self.width = width
        self.height = height
        pygame.init()
        self.screen = pygame.display.set_mode([self.width * 10, self.height * 10])
        pygame.display.set_caption("Mate Light Emu")
        self.clock = pygame.time.Clock()
        self.matrix = []
        for c in range(self.width * self.height * 3):
            self.matrix.append(0)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))

    def recv_data(self):
        data, addr = self.sock.recvfrom(self.width * self.height * 3 + 4)
        self.matrix = map(ord, data.strip())[:-4]

    def update(self):
        for x in range(self.width):
            for y in range(self.height):
                pixel = y * self.width * 3 + x * 3
                pygame.draw.circle(self.screen, (self.matrix[pixel], self.matrix[pixel + 1], self.matrix[pixel + 2]),
                                   (x * 10 + 5, y * 10 + 5), 5, 0)

    def render(self):
        pygame.display.update()
        pygame.display.flip()

    def gameloop(self):
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
            self.clock.tick(15)


if __name__ == '__main__':
    EMU = Emu()
    EMU.gameloop()