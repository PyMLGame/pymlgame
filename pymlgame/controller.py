# -*- coding: utf-8 -*-

"""
pymlgame - Controller
"""

__author__ = 'Ricardo Band'
__copyright__ = 'Copyright 2014, Ricardo Band'
__credits__ = ['Ricardo Band']
__license__ = 'MIT'
__version__ = '0.1.1'
__maintainer__ = 'Ricardo Band'
__email__ = 'me@xengi.de'
__status__ = 'Development'

import time
import socket
from queue import Queue
from threading import Thread

import pymlgame


class Controller(Thread):
    """
    A controller can be a game controller attached to the system or any other input that can trigger the controller
    functions like a smartphone app.
    """
    def __init__(self, host='127.0.0.1', port=1338):
        """
        Creates a controller deamon
        """
        super(Controller, self).__init__()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        self.queue = Queue()
        self.controllers = {}
        self._next_uid = 0

    def new_controller(self, addr):
        """
        Get an uid for your controller.
        """
        uid = self._next_uid
        self._next_uid += 1
        self.controllers[uid] = [addr, '00000000000000', time.time()]

        # create event for pygame
        event = object()
        event.type = pymlgame.E_NEWCTLR
        event.uid = uid
        self.queue.put_nowait(event)

        # return the uid for the socket
        return uid

    def del_controller(self, uid):
        """
        Remove controller from internal list and tell the game.
        """
        #TODO: check if UID actually exists
        self.controllers.pop(uid)
        event = object()
        event.type = pymlgame.E_DISCONNECT
        event.uid = uid
        self.queue.put_nowait(event)

    def ping(self, uid, addr):
        """
        Just say hello so that pymlgame knows that your controller is still alive. Otherwise the game could delete
        unused controllers after a while. But this has to be implemented by the game.
        """
        self.controllers[uid][0] = addr
        self.controllers[uid][2] = time.time()

        event = object()
        event.type = pymlgame.E_PING
        event.uid = uid
        self.queue.put_nowait(event)

    def update_states(self, uid, addr, states):
        """
        Got states of all buttons from a controller. Now check if something changed and create events if neccesary.
        """
        if self.controllers[uid]:
            old_states = self.controllers[uid][2]
            if old_states != states:
                for key in range(14):
                    if old_states[key] > states[key]:
                        event = object()
                        event.type = pymlgame.E_KEYUP
                        event.uid = uid
                        event.button = key
                        self.queue.put_nowait(event)
                    elif old_states[key] < states[key]:
                        event = object()
                        event.type = pymlgame.E_KEYDOWN
                        event.uid = uid
                        event.button = key
                        self.queue.put_nowait(event)
            self.controllers[uid][0] = addr
            self.controllers[uid][1] = states
            self.controllers[uid][2] = time.time()

    def got_message(self, uid, addr, text):
        """
        The controller has send us a message.
        """
        event = object()
        event.type = pymlgame.E_MESSAGE
        event.uid = uid
        event.text = text
        self.queue.put_nowait(event)

        self.controllers[uid][0] = addr
        self.controllers[uid][2] = time.time()

    def run(self):
        """
        Listen for clients.
        """
        while True:
            data, addr = self.sock.recvfrom(1024)
            data = data.decode('utf-8')
            if data.startswith('/controller/'):
                try:
                    uid = data.split('/')[2]
                    if uid == 'new':
                        uid = self.new_controller(addr)
                        self.sock.sendto('/uid/{}'.format(uid).encode('utf-8'), (addr, 11338))
                    else:
                        # just to be sure
                        uid = int(uid)
                        cmd = data.split('/')[3]
                        if cmd == 'ping':
                            self.ping(uid)
                        elif cmd == 'kthxbye':
                            self.del_controller(uid)
                        elif cmd == 'states':
                            payload = data[12 + len(str(uid)) + 8:]
                            self.update_states(uid, addr, payload)
                        elif cmd == 'text':
                            payload = data[12 + len(str(uid)) + 6:]
                            self.got_message(uid, addr, payload)
                except IndexError:
                    print('coitus interuptus detected!')

            # find unused controllers and delete them
            for uid, state in self.controllers.items():
                if state[2] < time.time() - 60:
                    self.controllers.pop(uid)