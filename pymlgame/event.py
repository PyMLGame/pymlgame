from uuid import UUID
from typing import Any


class Event(object):
    def __init__(self, id: UUID, type: int, data: Any = None):
        self.id = id
        self.type = type
        self.data = data
