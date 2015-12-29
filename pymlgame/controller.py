# -*- coding: utf-8 -*-

"""
PyMLGame - Controller
"""

from uuid import uuid4
import time
from datetime import datetime
import socket
from queue import Queue
from threading import Thread

from pymlgame.locals import E_NEWCTLR, E_DISCONNECT, E_PING, E_KEYUP, E_KEYDOWN, E_MESSAGE, E_RUMBLE
from pymlgame.event import Event


class Controller(Thread):
    """
    A controller can be a game controller attached to the system or any other input that can trigger the controller
    functions like a smartphone app.
    """
    def __init__(self, host='0.0.0.0', port=1338):
        """
        Creates a controller deamon

        :param host: Bind to address
        :param port: Bind to port
        :type host: str
        :type port: int
        """
        super(Controller, self).__init__()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        self.queue = Queue()
        self.controllers = {}

    def _new_controller(self, addr, port):
        """
        Get an uid for your controller.

        :param addr: Address of the controller
        :param port: Port of the controller
        :type addr: str
        :type port: int
        :return: Unique id of the controller
        :rtype: str
        """
        for uid, controller in self.controllers.items():
            if controller[0] == addr:
                # duplicate address. sending the uid again
                #print('/uid/{} => {}:{}'.format(uid, addr, port))
                self.sock.sendto('/uid/{}'.format(uid).encode('utf-8'), (addr, port))
                return False

        # get an uid and add the controller to the game
        uid = str(uuid4())
        self.controllers[uid] = [addr, port, '00000000000000', time.time()]

        # tell the controller about it
        #print('/uid/{} => {}:{}'.format(uid, addr, port))
        self.sock.sendto('/uid/{}'.format(uid).encode('utf-8'), (addr, port))

        # create event for pymlgame
        e = Event(uid, E_NEWCTLR)
        self.queue.put_nowait(e)

        return uid

    def _del_controller(self, uid):
        """
        Remove controller from internal list and tell the game.

        :param uid: Unique id of the controller
        :type uid: str
        """
        try:
            self.controllers.pop(uid)
            e = Event(uid, E_DISCONNECT)
            self.queue.put_nowait(e)
        except KeyError:
            # There is no such controller, ignore the command
            pass

    def _ping(self, uid, addr, port):
        """
        Just say hello so that pymlgame knows that your controller is still alive. Unused controllers will be deleted
        after a while. This function is also used to update the address and port of the controller if it has changed.

        :param uid: Unique id of the controller
        :param addr: Address of the controller
        :param port: Port that the controller listens on
        :type uid: str
        :type addr: str
        :type port: int
        """
        try:
            self.controllers[uid][0] = addr
            self.controllers[uid][1] = port
            self.controllers[uid][3] = time.time()

            e = Event(uid, E_PING)
            self.queue.put_nowait(e)
        except KeyError:
            # There is no such controller, ignore the command
            pass

    def _update_states(self, uid, states):
        """
        Got states of all buttons from a controller. Now check if something changed and create events if neccesary.

        :param uid: Unique id of the controller
        :param states: Buttons states
        :type uid: str
        :type states: str
        """
        #TODO: use try and catch all exceptions
        # test if uid exists
        if self.controllers[uid]:
            # test if states have correct lenght
            if len(states) == 14:
                old_states = self.controllers[uid][2]
                if old_states != states:
                    for key in range(14):
                        if int(old_states[key]) > int(states[key]):
                            e = Event(uid, E_KEYUP, key)
                            self.queue.put_nowait(e)
                        elif int(old_states[key]) < int(states[key]):
                            e = Event(uid, E_KEYDOWN, key)
                            self.queue.put_nowait(e)
                self.controllers[uid][2] = states
            self.controllers[uid][3] = time.time()

    def _got_message(self, uid, text):
        """
        The controller has send us a message.

        :param uid: Unique id of the controller
        :param text: Text to display
        :type uid: str
        :type text: str
        """
        #TODO: use try
        e = Event(uid, E_MESSAGE, text)
        self.queue.put_nowait(e)

        self.controllers[uid][2] = time.time()

    def send(self, uid, event, payload=None):
        """
        Send an event to a connected controller. Use pymlgame event type and correct payload.
        To send a message to the controller use pymlgame.E_MESSAGE event and a string as payload.

        :param uid: Unique id of the controller
        :param event: Event type
        :param payload: Payload of the event
        :type uid: str
        :type event: Event
        :type payload: str
        :return: Number of bytes send or False
        :rtype: int
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if uid in self.controllers.keys():
            addr = self.controllers[uid][0]
            port = self.controllers[uid][1]
            if event == E_MESSAGE:
                #print('/message/{} => {}:{}'.format(payload, addr, port))
                return sock.sendto('/message/{}'.format(payload).encode('utf-8'), (addr, port))
            elif event == E_RUMBLE:
                #print('/rumble/{} => {}:{}'.format(payload, addr, port))
                return sock.sendto('/rumble/{}'.format(payload).encode('utf-8'), (addr, port))
            else:
                pass
        else:
            pass
        return False

    def run(self):
        """
        Listen for controllers.
        """
        while True:
            data, sender = self.sock.recvfrom(1024)
            addr = sender[0]
            msg = data.decode('utf-8')
            if msg.startswith('/controller/'):
                try:
                    uid = msg.split('/')[2]
                    if uid == 'new':
                        port = int(msg.split('/')[3])
                        self._new_controller(addr, port)
                    else:
                        cmd = msg.split('/')[3]
                        if cmd == 'ping':
                            port = msg.split('/')[3]
                            self._ping(uid, addr, port)
                        elif cmd == 'kthxbye':
                            self._del_controller(uid)
                        elif cmd == 'states':
                            states = msg.split('/')[4]
                            self._update_states(uid, states)
                        elif cmd == 'text':
                            # /controller/<uid>/text/<text>
                            text = msg[12 + len(uid) + 6:]
                            self._got_message(uid, text)
                except IndexError or KeyError:
                    pass
            else:
                pass

            # find unused controllers and delete them
            ctlrs = self.controllers.items()
            for uid, state in ctlrs:
                if state[3] < time.time() - 60:
                    self.controllers.pop(uid)
