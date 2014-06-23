# -*- coding: utf-8 -*-

__author__ = 'Ricardo Band'
__copyright__ = 'Copyright 2014, Ricardo Band'
__credits__ = ['Ricardo Band']
__license__ = 'MIT'
__version__ = '0.2.0'
__maintainer__ = 'Ricardo Band'
__email__ = 'me@xengi.de'
__status__ = 'Development'

# from pymlgame.locals import *
# from pymlgame.screen import Screen
# from pymlgame.clock import Clock
# from pymlgame.surface import Surface
from pymlgame.controller import Controller

_ctlr = Controller()


def init(host='0.0.0.0', port=1338):
    """
    Initialize pymlgame. This creates a controller thread that listens for game controllers and events.
    """
    _ctlr.host = host
    _ctlr.port = port
    _ctlr.setDaemon(True)  # because it's a deamon it will exit together with the main thread
    _ctlr.start()


def get_events(maximum=10):
    """
    Get all events since the last time you asked for them. You can define a maximum which is 10 by default.
    """
    events = []
    for ev in range(0, maximum):
        try:
            if _ctlr.queue.empty():
                break
            else:
                events.append(_ctlr.queue.get_nowait())
        except NameError:
            not_initialized()
            events = False
            break
    return events


def get_event():
    """
    Get the next event in the queue if there is one.
    """
    if not _ctlr.queue.empty():
        return _ctlr.queue.get_nowait()
    else:
        return False


def not_initialized():
    print('pymlgame is not initialized correctly. Use pymlgame.init() first.')
