#!/usr/bin/env python3


"""
pymlgame - controller example
=============================

This example shows how you can use your notebooks keyboard to connect to a pymlgame instance.
"""

import sys
import socket
import logging
from threading import Thread
from datetime import datetime, timedelta

import pygame

# define some constants
E_ID = pygame.USEREVENT + 1
E_DOWNLOAD = pygame.USEREVENT + 2
E_PLAY = pygame.USEREVENT + 3
E_RUMBLE = pygame.USEREVENT + 4


class ReceiverThread(Thread):
    """
    This thread will listen on a UDP port for packets from the game.
    """
    def __init__(self, host: str = '0.0.0.0', port: int = 1338):
        """
        Creates the socket and binds it to the given host and port.
        """
        super().__init__()

        self._logger = logging.getLogger('receiver')

        self._host = host
        self._port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind((self._host, self._port))

    def run(self):
        while True:
            data, addr = self._sock.recvfrom(1024)
            try:
                data = data.decode('utf-8').split('/')
                command = data[1]
                param = data[2]

                if command == 'id':
                    e = pygame.event.Event(E_ID, {'id': param})
                    pygame.event.post(e)
                    self._logger.info('id received: %s' % param)
                elif command == 'download':
                    e = pygame.event.Event(E_DOWNLOAD, {'url': param})
                    pygame.event.post(e)
                    self._logger.info('download of %s triggered' % param)
                elif command == 'play':
                    e = pygame.event.Event(E_PLAY, {'filename': param})
                    pygame.event.post(e)
                    self._logger.info('playback of %s triggered' % param)
                elif command == 'rumble':
                    e = pygame.event.Event(E_RUMBLE, {'duration': int(param)})
                    pygame.event.post(e)
                    self._logger.info('request rumble for %s ms' % param)
            except IndexError:
                self._logger.error('invalid command received: %s' % data.decode('utf-8'))


class Controller:
    def __init__(self,
                 game_host: str = '127.0.0.1', game_port: int = 1338,
                 host: str = '0.0.0.0', port: int = 1338):
        self._logger = logging.getLogger('controller')

        self._game_host = game_host  # Bind host of Mate Light
        self._game_port = game_port  # Bind port of Mate Light
        self._host = host  # Bind host of ReceiverThread
        self._port = port  # Bind port of ReceiverThread
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        pygame.init()
        self._screen = pygame.display.set_mode((128, 113), pygame.DOUBLEBUF, 32)
        bg = pygame.image.load('kbd.png')
        self._screen.blit(bg, pygame.rect.Rect(0, 0, 128, 113))
        pygame.display.flip()

        # create state array for buttons
        self._keys = [0 for _ in range(14)]
        self._mapping = {pygame.K_UP: 0,        # Up
                         pygame.K_DOWN: 1,      # Down
                         pygame.K_LEFT: 2,      # Left
                         pygame.K_RIGHT: 3,     # Right
                         pygame.K_a: 4,         # A
                         pygame.K_w: 5,         # B
                         pygame.K_s: 6,         # X
                         pygame.K_d: 7,         # Y
                         pygame.K_RETURN: 8,    # Start
                         pygame.K_SPACE: 9,     # Select
                         pygame.K_q: 10,        # L1
                         pygame.K_1: 11,        # L2
                         pygame.K_e: 12,        # R1
                         pygame.K_3: 13}        # R2

        # if the controller is in idle state a ping signal will be sent
        self._timeout = datetime.now() + timedelta(seconds=30)
        self.rumble_active = False
        self.id = None

        self._receiver = ReceiverThread(self._host, self._port)
        self._receiver.setDaemon(True)
        self._receiver.start()

    def ping(self):
        """
        Send a ping signla to the game so that it knows we are still active.
        
        :return: 
        """
        if self.id:
            self._logger.info('sending ping')
            msg = '/controller/%s/ping/%s' % (self.id, self._receiver._port)
            self._sock.sendto(msg.encode('utf-8'), (self._game_host, self._game_port))

    def send_keys(self):
        """
        Send current key states to the game.
        
        :return: 
        """
        # alternative states creation: [1 if k else 0 for k in self.keys]
        states = '/controller/%s/states/%s' % (self.id, ''.join([str(k) for k in self._keys]))
        self._logger.info('sending states %s' % ''.join([str(k) for k in self._keys]))
        self._sock.sendto(states.encode('utf-8'), (self._game_host, self._game_port))
        self._timeout = datetime.now()

    def send_message(self, msg: str):
        """
        Send message to the game.
        
        :param msg: The message to send.
        :return: 
        """
        self._logger.info('sending of messages not yet implemented')

    def disconnect(self):
        """
        Disconnect from the game.
        
        :return: 
        """
        self._logger.info('disconnecting from game')
        msg = '/controller/%s/kthxbye' % self.id
        self._sock.sendto(msg.encode('utf-8'), (self._game_host, self._game_port))

    def connect(self):
        """
        Connect to game intance.
        
        :return: 
        """
        self._logger.info('connecting to game')
        msg = '/controller/new/{}'.format(self._port)
        self._sock.sendto(msg.encode('utf-8'), (self._game_host, self._game_port))

    def rumble(self, duration: int):
        """
        The controller should vibrate a the given time.
        
        :param duration: Time in milliseconds.
        :type duration: int
        :return: 
        """
        self._logger.warning('rumble not yet implemented')

    def download_sound(self, url: str):
        """
        Download sound file to controller. Typically done when the game starts.
        
        :param url: File to download.
        :type url: str
        :return: 
        """
        self._logger.warning('downloading of media files not yet implemented')

    def play_sound(self, filename: str):
        """
        Play downloaded file.
        
        :param filename: Filename to play. 
        :type filename: str
        :return: 
        """
        self._logger.warning('playing media files not yet implemented')

    def handle_inputs(self):
        """
        Get all events and process them.
        
        :return: 
        """
        if self._timeout < datetime.now() + timedelta(seconds=30):
            self.ping()
            self._timeout = datetime.now() + timedelta(seconds=30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONUP:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            elif event.type == E_ID:
                self.id = event.id

            if self.id is not None:
                if event.type == E_DOWNLOAD:
                    self.download_sound(event.url)
                elif event.type == E_PLAY:
                    self.play_sound(event.filename)
                elif event.type == E_RUMBLE:
                    self.rumble(event.duration)
                elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    try:
                        button = self._mapping[event.key]
                        if event.type == pygame.KEYDOWN:
                            self._keys[button] = 1
                        elif event.type == pygame.KEYUP:
                            self._keys[button] = 0
                        self.send_keys()
                    except KeyError:
                        continue
            else:
                self.connect()


if __name__ == '__main__':
    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    ctlr = Controller('127.0.0.1', 1338, '0.0.0.0', 1338)
    try:
        while True:
            ctlr.handle_inputs()
    except KeyboardInterrupt:
        if ctlr.id is not None:
            # for a clean shutdown disconnect from the game
            ctlr.disconnect()
