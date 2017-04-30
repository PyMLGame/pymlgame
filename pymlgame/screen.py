import socket
from typing import List, Tuple

from pymlgame.locals import BLACK
from pymlgame.surface import Surface


class Screen:
    def __init__(self, host: str = '127.0.0.1', port: int = 1337, width: int = 40, height: int = 16):
        self.host: str = host
        self.port: int = port
        self.width: int = width
        self.height: int = height

        self.matrix: List[List[Tuple[int, int, int]]]

        self.reset()

    def reset(self, color: Tuple[int, int, int] = BLACK):
        """
        Resets the screen to the privided given color.
        
        :param color: The color to reset the screen [default (0, 0, 0).
        :type color: tuple
        :return: 
        """
        #for x in range(self.width):
        #    for y in range(self.height):
        #        self.matrix[x][y] = color
        self.matrix = [[color for _ in range(self.height)] for _ in range(self.width)]

    def update(self):
        """
        Sends the current screen contents to the Mate Light.
        
        :return:
        """
        display_data: List[int] = []
        for y in range(self.height):
            for x in range(self.width):
                # check for transparency, add black if transparent
                if self.matrix[x][y]:
                    for color in self.matrix[x][y]:
                        display_data.append(color)
                else:
                    display_data.extend([0, 0, 0])

        checksum = bytearray([0, 0, 0, 0])
        data_as_bytes = bytearray(display_data)
        data = data_as_bytes + checksum
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(data, (self.host, self.port))

    def point_on_screen(self, position: Tuple[int, int]) -> bool:
        """
        Checks if the point is still on the screen.

        :param position: The point to check
        :type position: tuple
        :return: Is it?
        :rtype: bool
        """
        return 0 <= position[0] < self.width and 0 <= position[1] < self.height

    def blit(self, surface: Surface, position: Tuple[int, int] = (0, 0)):
        """
        Blits a surface on the screen at a specific position.

        :param surface: Surface to blit.
        :param position: Top left corner to start blitting [default: (0, 0)].
        :type surface: Surface
        :type position: tuple
        """
        for x in range(surface.width):
            for y in range(surface.height):
                if surface.matrix[x][y]:
                    point = (x + position[0], y + position[1])
                    if self.point_on_screen(point):
                        self.matrix[point[0]][point[1]] = surface.matrix[x][y]
