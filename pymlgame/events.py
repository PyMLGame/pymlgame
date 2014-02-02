# -*- coding: utf-8 -*-

"""
pymlgame - Events
"""

__author__ = "Ricardo Band"
__copyright__ = "Copyright 2013, Ricardo Band"
__credits__ = ["Ricardo Band"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Ricardo Band"
__email__ = "me@xengi.de"
__status__ = "Development"


class EventListener(object):
    def __init__(self):
        getch = Getch()
        self.events = []
        self.events.append(getch.get_key())

    def get_events(self):
        """
        Return all events that happened since last time we checked
        """
        return self.events


class Getch:
    def __init__(self):
        pass

    def get_key(self):
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch