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

import pymlgame


class Controller(object):
    """
    A controller can be a game controller attached to the system or any other
    input that can trigger the controller functions
    """
    def __init__(self):
        """
        Creates a minimal controller
        """
        self.mapping = {'up': None, 'down': None, 'left': None, 'right': None,
                        'ok': None, 'cancel': None,
                        'fire_a': None, 'fire_b': None}
        self.events = []

    def set_mapping(self, mapping):
        """
        Set the new mapping for this contoller
        """
        if mapping['up'] and mapping['down'] and mapping['left'] and \
           mapping['right'] and mapping['ok'] and mapping['cancel'] and \
           mapping['fire_a'] and mapping['fire_b']:
            self.mapping = mapping

    def get_events(self):
        pass