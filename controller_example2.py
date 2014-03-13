#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
pymlgame - controller example
=============================

This example shows how you can use your notebooks keyboard to connect to a pymlgame instance.
"""

__author__ = 'Ricardo Band'
__copyright__ = 'Copyright 2014, Ricardo Band'
__credits__ = ['Ricardo Band']
__license__ = 'MIT'
__version__ = '0.1.1'
__maintainer__ = 'Ricardo Band'
__email__ = 'me@xengi.de'
__status__ = 'Development'

import sys
import time
import socket
from threading import Thread, Timer

import pygame

# define some constants
E_UID = pygame.USEREVENT + 1
E_PLAY = pygame.USEREVENT + 2
E_RUMBLE = pygame.USEREVENT + 3


class ReceiverThread(Thread):
    """
    This thread listen on a UDP port for packets from a pymlgame instance.
    """
    def __init__(self, host='127.0.0.1', port=11338):
        """
        Creates the socket and binds it to the given host and port.
        """
        super(ReceiverThread, self).__init__()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

    def run(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            data = data.decode('utf-8')

            if data.startswith('/uid/'):
                ev = pygame.event.Event(E_UID, {'uid': int(data[5:])})
                pygame.event.post(ev)
            elif data.startswith('/play/'):
                ev = pygame.event.Event(E_PLAY, {'filename': str(data[6:])})
                pygame.event.post(ev)
            elif data.startswith('/rumble/'):
                ev = pygame.event.Event(E_RUMBLE, {'duration': float(data[8:].replace(',', '.'))})
                pygame.event.post(ev)


class Controller(object):
    def __init__(self, host='127.0.0.1', port=1337):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        pygame.init()
        self.screen = pygame.display.set_mode((128, 113), pygame.DOUBLEBUF, 32)
        bg = pygame.image.load('kbd.png')
        self.screen.blit(bg, pygame.rect.Rect(0, 0, 128, 113))
        pygame.display.flip()

        self.keys = [0 for _ in range(14)]
        self.mapping = {pygame.K_UP: 0,      # Up
                        pygame.K_DOWN: 1,    # Down
                        pygame.K_LEFT: 2,    # Left
                        pygame.K_RIGHT: 3,   # Right
                        pygame.K_a: 4,       # A
                        pygame.K_w: 5,       # B
                        pygame.K_s: 6,       # X
                        pygame.K_d: 7,       # Y
                        pygame.K_RETURN: 8,  # Start
                        pygame.K_SPACE: 9,   # Select
                        pygame.K_q: 10,      # L1
                        pygame.K_1: 11,      # L2
                        pygame.K_e: 12,      # R1
                        pygame.K_3: 13}      # R2

        self.timeout = 0
        self.rumble_active = False
        self.uid = None

        receiver = ReceiverThread()
        receiver.setDaemon(True)
        receiver.start()

    def ping(self):
        self.sock.sendto(bytes('/ping/{}'.format(self.uid).encode('utf-8')), (self.host, self.port))

    def send_keys(self):
        # alternative states creation: [1 if k else 0 for k in self.keys]
        states = '/states/{}/{}'.format(self.uid, ''.join([str(k) for k in self.keys]))
        self.sock.sendto(states.encode('utf-8'), (self.host, self.port))
        self.timeout = time.time()

    def rumble(self, stop=False):
        if stop:
            # stop the rumble
            pass
        else:
            # start the rumble
            pass

    def play_sound(self, filename):
        pass

    def handle_inputs(self):
        while True:
            if time.time() > self.timeout + 30:
                self.ping()

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONUP:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                elif event.type == E_UID:
                    self.uid = event.uid
                if self.uid:
                    if event.type == E_PLAY:
                        self.play_sound(event.filename)
                    elif event.type == E_RUMBLE:
                        self.rumble()
                        #TODO: check if the timers get killed when they are stopped. no zombies allowed here!
                        t = Timer(event.duration, self.rumble, args=[True, ])
                        t.setDaemon(True)
                        t.start()
                    elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                        try:
                            button = self.mapping[event.key]
                            if event.type == pygame.KEYDOWN:
                                print('{}({}) key down'.format(event.key, button))
                                self.keys[button] = 1
                            elif event.type == pygame.KEYUP:
                                print('{}({}) key up'.format(event.key, button))
                                self.keys[button] = 0
                            self.send_keys()
                        except KeyError:
                            break


if __name__ == '__main__':
    ctlr = Controller()
    try:
        while True:
            ctlr.handle_inputs()
    except KeyboardInterrupt:
        pass