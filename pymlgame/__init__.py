import sys
from typing import List

from pymlgame.clock import Clock
from pymlgame.screen import Screen
from pymlgame.surface import Surface
from pymlgame.event import Event
from pymlgame.controller import Controller


__author__ = 'Ricardo Band'
__copyright__ = 'Ricardo Band'
__credits__ = ['Ricardo Band', ]
__license__ = 'MIT'
__version__ = '0.4.0'
__maintainer__ = 'Ricardo Band'
__email__ = 'email@ricardo.band'
__status__ = 'Development'


# predefined colors
RED = (255, 0, 0)
MAGENTA = (255, 0, 255)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
DARKRED = (127, 0, 0)
DARKMAGENTA = (127, 0, 127)
DARKBLUE = (0, 0, 127)
DARKCYAN = (0, 127, 127)
DARKGREEN = (0, 127, 0)
DARKYELLOW = (127, 127, 0)
BLACK = (0, 0, 0)
GREY9 = (25, 25, 25)
GREY8 = (51, 51, 51)
GREY7 = (76, 76, 76)
GREY6 = (102, 102, 102)
GREY5 = (127, 127, 127)
GREY4 = (153, 153, 153)
GREY3 = (178, 178, 178)
GREY2 = (204, 204, 204)
GREY1 = (229, 229, 229)
WHITE = (255, 255, 255)

# controller inputs
CTLR_UP = 0
CTLR_DOWN = 1
CTLR_LEFT = 2
CTLR_RIGHT = 3
CTLR_A = 4
CTLR_B = 5
CTLR_X = 6
CTLR_Y = 7
CTLR_START = 8
CTLR_SELECT = 9
CTLR_R1 = 10
CTLR_R2 = 11
CTLR_L1 = 12
CTLR_L2 = 13

# event types
E_KEYUP = 0
E_KEYDOWN = 1
E_NEWCTLR = 2
E_PING = 3
E_DISCONNECT = 4
E_MESSAGE = 5
E_RUMBLE = 6

CONTROLLER_T = Controller()

def init(host: str = '0.0.0.0', port: int = 1338):
    """
    Initialize pymlgame and the controller thread.

    :param host: Bind to hostname
    :param port: Boind to port
    :type host: str
    :type port: int
    :return: 
    """
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
    if not CONTROLLER_T.queue.empty():
        return CONTROLLER_T.queue.get_nowait()
    else:
        return None
