# -*- coding: utf-8 -*-

__author__ = 'xengi'

import time


class Clock(object):
    """
    Measure the time to adjust drawing rates.
    """
    def __init__(self):
        """
        Get a fresh Clock.
        """
        self.__last_tick = False

    def tick(self, fps):
        """
        Let the Clock tick x times per second.
        """
        tick = time.time()
        if self.__last_tick:
            time.sleep(float(1)/fps)
        self.__last_tick = tick