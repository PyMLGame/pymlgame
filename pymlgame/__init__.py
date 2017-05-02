import sys
from typing import List

from pymlgame.clock import Clock
from pymlgame.screen import Screen
from pymlgame.surface import Surface
from pymlgame.event import Event
from pymlgame.controller import Controller
from pymlgame.locals import *

__author__ = 'Ricardo Band'
__copyright__ = 'Ricardo Band'
__credits__ = ['Ricardo Band', ]
__license__ = 'MIT'
__version__ = '0.4.0'
__maintainer__ = 'Ricardo Band'
__email__ = 'email@ricardo.band'
__status__ = 'Development'


CONTROLLER_T = None

def init(host: str = '0.0.0.0', port: int = 1338):
    """
    Initialize pymlgame and the controller thread.

    :param host: Bind to hostname
    :param port: Boind to port
    :type host: str
    :type port: int
    :return: 
    """
    global CONTROLLER_T

    CONTROLLER_T = Controller()
    CONTROLLER_T.host = host
    CONTROLLER_T.port = port
    CONTROLLER_T.setDaemon(True)  # because it's a deamon it will exit together with the main thread
    CONTROLLER_T.start()


def get_events(maximum: int = 10) -> List[Event]:
    """
    Get all events since the last time you asked for them. You can define a maximum which is 10 by default.

    :param maximum: Maximum number of events
    :type maximum: int
    :return: List of events
    :rtype: List[Event]
    """
    global CONTROLLER_T

    events = []
    for ev in range(0, maximum):
        try:
            if CONTROLLER_T.queue.empty():
                break
            else:
                events.append(CONTROLLER_T.queue.get_nowait())
        except NameError:
            sys.exit('PyMLGame is not initialized correctly. Use pymlgame.init() first.')
    return events


def get_event() -> Event:
    """
    Get the next event in the queue if there is one.

    :return: Next controller event
    :rtype: Event
    """
    global CONTROLLER_T

    if not CONTROLLER_T.queue.empty():
        return CONTROLLER_T.queue.get_nowait()
