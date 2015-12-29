# -*- coding: utf-8 -*-

"""
PyMLGame
"""

__author__ = 'Ricardo Band'
__copyright__ = 'Ricardo Band'
__credits__ = ['Ricardo Band']
__license__ = 'MIT'
__version__ = '0.3.1'
__maintainer__ = 'Ricardo Band'
__email__ = 'email@ricardo.band'
__status__ = 'Development'

from pymlgame.locals import *
from pymlgame.screen import Screen
from pymlgame.clock import Clock
from pymlgame.surface import Surface
from pymlgame.controller import Controller

CONTROLLER = Controller()


def init(host='0.0.0.0', port=1338):
    """
    Initialize PyMLGame. This creates a controller thread that listens for game controllers and events.

    :param host: Bind to this address
    :param port: Bind to this port
    :type host: str
    :type port: int
    """
    CONTROLLER.host = host
    CONTROLLER.port = port
    CONTROLLER.setDaemon(True)  # because it's a deamon it will exit together with the main thread
    CONTROLLER.start()


def get_events(maximum=10):
    """
    Get all events since the last time you asked for them. You can define a maximum which is 10 by default.

    :param maximum: Maximum number of events
    :type maximum: int
    :return: List of events
    :rtype: list
    """
    events = []
    for ev in range(0, maximum):
        try:
            if CONTROLLER.queue.empty():
                break
            else:
                events.append(CONTROLLER.queue.get_nowait())
        except NameError:
            print('PyMLGame is not initialized correctly. Use pymlgame.init() first.')
            events = False
            break
    return events


def get_event():
    """
    Get the next event in the queue if there is one.

    :return: Next controller event
    :rtype: Event or False
    """
    if not CONTROLLER.queue.empty():
        return CONTROLLER.queue.get_nowait()
    else:
        return False
