# -*- coding: utf-8 -*-

"""
pymlgame - Controller
"""

__author__ = "Ricardo Band"
__copyright__ = "Copyright 2013, Ricardo Band"
__credits__ = ["Ricardo Band"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Ricardo Band"
__email__ = "me@xengi.de"
__status__ = "Development"

from threading import Thread

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

import pymlgame


class Controller(object):
    """
    A controller can be a game controller attached to the system or any other
    input that can trigger the controller functions
    """
    def __init__(self, host, port):
        """
        Creates a controller deamon
        """
        self.host = host
        self.port = port
        self._mapping = {'Up': pymlgame.CTLR_UP,
                         'Down': pymlgame.CTLR_DOWN,
                         'Left': pymlgame.CTLR_LEFT,
                         'Right': pymlgame.CTLR_RIGHT,
                         'A': pymlgame.CTLR_A,
                         'B': pymlgame.CTLR_B,
                         'X': pymlgame.CTLR_X,
                         'Y': pymlgame.CTLR_Y,
                         'Start': pymlgame.CTLR_START,
                         'Select': pymlgame.CTLR_SELECT,
                         'R1': pymlgame.CTLR_R1,
                         'R2': pymlgame.CTLR_R2,
                         'L1': pymlgame.CTLR_L1,
                         'L2': pymlgame.CTLR_L2}
        self._events = {'KeyUp': pymlgame.KEYUP,
                        'KeyDown': pymlgame.KEYDOWN}
        self.queue = []
        self._next_uid = 0

        self.server = SimpleJSONRPCServer((host, port))
        self.server.register_function(self.init)
        self.server.register_function(self.get_button_keys)
        self.server.register_function(self.get_event_keys)
        self.server.register_function(self.ping)
        self.server.register_function(self.trigger_button)

        self.t = Thread(target=self.server.serve_forever)
        self.t.start()

    def init(self):
        """
        Get an uid for your controller.
        """
        uid = self._next_uid
        self._next_uid += 1
        event = Event()
        event.type = pymlgame.NEWCTLR
        event.uid = uid
        self.queue.append(event)
        return uid

    def get_button_keys(self):
        """
        Return a list of possible buttons.
        """
        return list(self._mapping.keys())

    def get_event_keys(self):
        """
        Return a list of possible events.
        """
        return list(self._events.keys())

    def ping(self, uid):
        """
        Just say hello so that pymlgame knows that your controller is still
        in use. Otherwise the game could delete unused controlers after a
        while. But this has to be implemented by the game.
        """
        event = Event()
        event.type = pymlgame.PING
        event.uid = uid
        self.queue.append(event)

    def trigger_button(self, uid, event, button):
        """
        Triggers the given button event.
        """
        if self._events[event] >= 0 and self._mapping[button] >= 0:
            ev = Event()
            ev.uid = uid
            ev.type = self._events[event]
            ev.button = self._mapping[button]
            self.queue.append(ev)

    def get_events(self):
        """
        Empty current event queue and send it's contents to the game.
        """
        ret = []
        while len(self.queue) != 0:
            ret.append(self.queue.pop(0))
        return ret


class Event(object):
    """
    Represents an event which has a type and optionally a uid and a button.
    """
    def __init__(self):
        self.type = None
        self.button = None
        self.uid = None