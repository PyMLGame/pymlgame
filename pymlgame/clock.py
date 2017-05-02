import time
from typing import Callable
from datetime import datetime, timedelta


class Clock:
    """
    Measure the time to adjust drawing rates.
    """
    def __init__(self, fps: int):
        """
        Get a fresh Clock which ticks n times per second.

        :param fps: Target frames per second
        :type fps: int
        """
        self.fps = fps
        self.last_tick = datetime.now()

    def tick(self):
        """
        Let the Clock tick.
        """
        wait = timedelta(seconds=1) / self.fps - (datetime.now() - self.last_tick)
        if wait > timedelta(seconds=0):
            time.sleep(wait.total_seconds())
        self.last_tick = datetime.now()

    @staticmethod
    def timer(timeout: float, callback: Callable, *args):
        """
        Call function after timeout.
        
        :param timeout: Time to wait in seconds. 
        :param callback: function to call after timeout.
        :param args: Arguments for callback.
        :type timeout: float
        :type callback: Callable
        :return: 
        """
        time.sleep(timeout)
        callback(*args)
