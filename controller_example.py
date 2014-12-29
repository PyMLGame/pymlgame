#!/usr/bin/env python2
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

DEBUG = True

# define some constants
E_UID = pygame.USEREVENT + 1
E_DOWNLOAD = pygame.USEREVENT + 2
E_PLAY = pygame.USEREVENT + 3
E_RUMBLE = pygame.USEREVENT + 4


class ReceiverThread(Thread):
    """
    This thread will listen on a UDP port for packets from the game.
    """
    def __init__(self, host='0.0.0.0', port=1338):
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
            if data.startswith('/uid/'):
                e = pygame.event.Event(E_UID, {'uid': int(data[5:])})
                pygame.event.post(e)
                if DEBUG: logging.info('uid received: {}'.format(data[5:]))
            elif data.startswith('/download/'):
                e = pygame.event.Event(E_DOWNLOAD, {'url': str(data[10:])})
                pygame.event.post(e)
                if DEBUG: logging.info('download of {} triggered'.format(data[10:]))
            elif data.startswith('/play/'):
                e = pygame.event.Event(E_PLAY, {'filename': str(data[6:])})
                pygame.event.post(e)
                if DEBUG: logging.info('playback of {} triggered'.format(data[6:]))
            elif data.startswith('/rumble/'):
                e = pygame.event.Event(E_RUMBLE, {'duration': int(data[8:])})
                pygame.event.post(e)
                if DEBUG: logging.info('request rumble for {}ms'.format(data[8:]))


class Controller(object):
    def __init__(self, game_host='127.0.0.1', game_port=1338, host='0.0.0.0', port=1338):
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

        self._receiver = ReceiverThread(self.host, self.port)
        self._receiver.setDaemon(True)
        self._receiver.start()

    def ping(self):
        if self.uid:
            if DEBUG: logging.info('sending ping')
            msg = '/controller/{}/ping/{}'.format(self.uid, self._receiver.port)
            self.sock.sendto(msg.encode('utf-8'), (self.game_host, self.game_port))

    def send_keys(self):
        # alternative states creation: [1 if k else 0 for k in self.keys]
        states = '/controller/{}/states/{}'.format(self.uid, ''.join([str(k) for k in self.keys]))
        if DEBUG: logging.info('sending states {}'.format(''.join([str(k) for k in self.keys])))
        self.sock.sendto(states.encode('utf-8'), (self.game_host, self.game_port))
        self.timeout = time.time()

    def send_message(self, msg):
        if DEBUG: logging.info('sending of messages not yet implemented')
        pass

    def disconnect(self):
        if DEBUG: logging.info('disconnecting from game')
        msg = '/controller/{}/kthxbye'.format(self.uid)
        self.sock.sendto(msg.encode('utf-8'), (self.game_host, self.game_port))

    def connect(self):
        if DEBUG: logging.info('connecting to game')
        msg = '/controller/new/{}'.format(self.port)
        self.sock.sendto(msg.encode('utf-8'), (self.game_host, self.game_port))

    def rumble(self, duration):
        if DEBUG: logging.info('rumble not yet implemented')
        pass

    def download_sound(self, url):
        if DEBUG: logging.info('downloading of media files not yet implemented')
        pass

    def play_sound(self, filename):
        if DEBUG: logging.info('playing media files not yet implemented')
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
                self.uid = event.uid

            if self.uid is not None:
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
                            self.keys[button] = 1
                        elif event.type == pygame.KEYUP:
                            self.keys[button] = 0
                        self.send_keys()
                    except KeyError:
                        break
            else:
                self.connect()
                time.sleep(1)


if __name__ == '__main__':
    ctlr = Controller('127.0.0.1', 1338, '0.0.0.0', 1338)
    try:
        while True:
            ctlr.handle_inputs()
    except KeyboardInterrupt:
        if ctlr.uid is not None:
            ctlr.disconnect()
        pass
