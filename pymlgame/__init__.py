import sys
import logging
from typing import List

from .clock import Clock
from .screen import Screen, IntroScreen
from .surface import Surface
from .event import Event, EventType
from .controller import Controller
from .locals import *

__author__ = 'Ricardo Band'
__copyright__ = 'Ricardo Band'
__credits__ = ['Ricardo Band', ]
__license__ = 'MIT'
__version__ = '0.4.0'
__maintainer__ = 'Ricardo Band'
__email__ = 'email@ricardo.band'
__status__ = 'Development'


CONTROLLER_T: object
LOGGER: object

def init(host: str = '0.0.0.0', port: int = 1338, debug: bool = False):
    """
    Initialize pymlgame and the controller thread.

    :param host: Bind to hostname
    :param port: Boind to port
    :type host: str
    :type port: int
    :return: 
    """
    global CONTROLLER_T
    global LOGGER

    if debug:
        LOGGER = logging.getLogger('main')
        LOGGER.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        LOGGER.addHandler(ch)
        LOGGER.debug('DEBUG MODE enabled')

    CONTROLLER_T = Controller()
    CONTROLLER_T.host = host
    CONTROLLER_T.port = port
    CONTROLLER_T.setDaemon(True)  # because it's a deamon it will exit together with the main thread
    CONTROLLER_T.start()


def get_events(max: int = 10) -> List[Event]:
    """
    Get all events since the last time you asked for them. You can define a maximum which is 10 by default.

    :param max: Maximum number of events
    :type max: int
    :return: List of events
    :rtype: List[Event]
    """
    global CONTROLLER_T

    events = []
    for _ in range(0, max):
        e = get_event()
        if e:
            events.append(e)
        else:
            break
    return events


def get_event() -> Event:
    """
    Get the next event in the queue if there is one.

    :return: Next controller event
    :rtype: Event
    """
    global CONTROLLER_T
    global LOGGER

    try:
        if not CONTROLLER_T.queue.empty():
            ev = CONTROLLER_T.queue.get_nowait()
            if LOGGER:
                LOGGER.debug('new event: %s %s %s' % (ev.id, ev.type, ev.data))
            return ev
        else:
            return None
    except NameError:
        sys.exit('PyMLGame is not initialized correctly. Use pymlgame.init() first.')
