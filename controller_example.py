#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
pymlgame - controller example
=============================

This example shows how you can use your notebooks keyboard to connect to a pymlgame instance.
"""

import sys
import time
import socket
import logging
logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
from datetime import datetime
from threading import Thread

import pygame

# define some constants
E_UID = pygame.USEREVENT + 1
E_DOWNLOAD = pygame.USEREVENT + 2
E_PLAY = pygame.USEREVENT + 3
E_RUMBLE = pygame.USEREVENT + 4


class ReceiverThread(Thread):
    """
    This thread will listen on a UDP port for packets from the game.
    """
    def __init__(self, host='127.0.0.1', port=11337):
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

            logging.info('example info')
            logging.warning('example warning')
            logging.error('example error')
            logging.critical('example critical')
            #print(datetime.now(), '<<< {}'.format(data))
            if data.startswith('/uid/'):
                #print(datetime.now(), '### uid', data[5:], 'received')
                e = pygame.event.Event(E_UID, {'uid': int(data[5:])})
                pygame.event.post(e)
            elif data.startswith('/download/'):
                e = pygame.event.Event(E_DOWNLOAD, {'url': str(data[10:])})
                pygame.event.post(e)
            elif data.startswith('/play/'):
                e = pygame.event.Event(E_PLAY, {'filename': str(data[6:])})
                pygame.event.post(e)
            elif data.startswith('/rumble/'):
                e = pygame.event.Event(E_RUMBLE, {'duration': float(data[8:].replace(',', '.'))})
                pygame.event.post(e)


class Controller(object):
    def __init__(self, game_host='127.0.0.1', game_port=1338, host='127.0.0.1', port=11337):
        self.game_host = game_host  # Host of Mate Light
        self.game_port = game_port  # Port of Mate Light
        self.host = host  # Host of ReceiverThread
        self.port = port  # Port of ReceiverThread
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

        self.timeout = 0  # if the controller is in idle state a ping signal will be sent
        self.rumble_active = False
        self.uid = None

        self._receiver = ReceiverThread(host, port)
        self._receiver.setDaemon(True)
        self._receiver.start()

    def ping(self):
        if self.uid:
            msg = '/controller/{}/ping/{}'.format(self.uid, self._receiver.port)
            self.sock.sendto(msg.encode('utf-8'), (self.game_host, self.game_port))
            #print(datetime.now(), '>>>', msg)

    def send_keys(self):
        # alternative states creation: [1 if k else 0 for k in self.keys]
        states = '/controller/{}/states/{}'.format(self.uid, ''.join([str(k) for k in self.keys]))
        self.sock.sendto(states.encode('utf-8'), (self.game_host, self.game_port))
        #print(datetime.now(), '>>>' + states)
        self.timeout = time.time()

    def send_message(self, msg):
        pass

    def disconnect(self):
        msg = '/controller/{}/kthxbye'.format(self.uid)
        self.sock.sendto(msg.encode('utf-8'), (self.game_host, self.game_port))

    def connect(self):
        msg = '/controller/new/{}'.format(self.port)
        self.sock.sendto(msg.encode('utf-8'), (self.game_host, self.game_port))

    def rumble(self, duration):
        pass

    def download_sound(self, url):
        pass

    def play_sound(self, filename):
        pass

    def handle_inputs(self):
        if time.time() > self.timeout + 30:
            self.ping()
            self.timeout = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONUP:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            elif event.type == E_UID:
                #print(datetime.now(), '### UID event received', event.uid)
                self.uid = event.uid

            if self.uid is not None:
                #print(datetime.now(), '### UID set. checking other events')
                if event.type == E_DOWNLOAD:
                    self.download_sound(event.url)
                elif event.type == E_PLAY:
                    self.play_sound(event.filename)
                elif event.type == E_RUMBLE:
                    self.rumble(event.duration)
                elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    try:
                        button = self.mapping[event.key]
                        if event.type == pygame.KEYDOWN:
                            #print('{} | {}'.format(event.key, button))
                            self.keys[button] = 1
                        elif event.type == pygame.KEYUP:
                            #print('{} | {}'.format(event.key, button))
                            self.keys[button] = 0
                        self.send_keys()
                    except KeyError:
                        break
            else:
                #print(datetime.now(), '### UID not set. connecting to game.')
                self.connect()
                time.sleep(1)


if __name__ == '__main__':
    ctlr = Controller('127.0.0.1', 1338, '127.0.0.1', 11337)
    try:
        while True:
            ctlr.handle_inputs()
    except KeyboardInterrupt:
        if ctlr.uid is not None:
            ctlr.disconnect()
        pass