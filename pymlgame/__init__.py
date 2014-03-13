# -*- coding: utf-8 -*-

__author__ = 'Ricardo Band'
__copyright__ = 'Copyright 2014, Ricardo Band'
__credits__ = ['Ricardo Band']
__license__ = 'MIT'
__version__ = '0.1.1'
__maintainer__ = 'Ricardo Band'
__email__ = 'me@xengi.de'
__status__ = 'Development'

import socket

from pymlgame.locals import *
from pymlgame.screen import Screen
from pymlgame.clock import Clock
from pymlgame.surface import Surface
from pymlgame.controller import Controller


def init(host='127.0.0.1', port=1337):
    """
    Initialize pymlgame. This creates a controller thread that listens for game controllers and events.
    """
    global ctlr
    ctlr = Controller(host, port + 1)
    ctlr.start()


def get_events(maximum=10):
    """
    Get all events since the last time you asked for them. You can define a maximum which is 10 by default.
    """
    events = []
    for ev in range(0, maximum):
        try:
            if ctlr.queue.empty():
                break
            else:
                events.append(ctlr.queue.get_nowait())
        except NameError:
            not_initialized()
            events = False
            break
    return events


def get_event():
    """
    Get the next event in the queue if there is one.
    """
    if not ctlr.queue.empty():
        return ctlr.queue.get_nowait()
    else:
        return False


def controller_send(uid, event, data):
    """
    Send an event to a connected controller. Use the pymlgame event type and the coorect data payload. For example is
    you want to send a message to the controller use the event pymlgame.MESSAGE and a string payload.

    It returns the number of bytes send when everything went fine or False when something went wrong.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if uid in ctlr.controllers.keys():
            addr = ctlr.controllers[uid][0]
            if event == E_MESSAGE:
                return sock.sendto('/message/{}'.format(data).encode('utf-8'), (addr, 11338))
            elif event == E_RUMBLE:
                return sock.sendto('/rumble/{}'.format(data).encode('utf-8'), (addr, 11338))
        else:
            print('This UID ({}) doesn\'t exist.'.format(uid))
            return False
    except NameError:
        not_initialized()
        return False


def not_initialized():
    print('pymlgame is not initialized correctly. Use pymlgame.init() first.')