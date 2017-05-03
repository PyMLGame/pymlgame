from enum import Enum
from typing import Any


class EventType(Enum):
    E_KEYUP = 0
    E_KEYDOWN = 1
    E_NEWCTLR = 2
    E_PING = 3
    E_DISCONNECT = 4
    E_MESSAGE = 5
    E_RUMBLE = 6


class Event:
    def __init__(self, id: str, type: EventType, data: Any = None):
        self.id = id
        self.type = type
        self.data = data
