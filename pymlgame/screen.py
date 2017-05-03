import socket
from time import sleep
from typing import List, Tuple

from .locals import BLACK
from .surface import Surface


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


class IntroScreen(Screen):
    def __init__(self, host: str = '127.0.0.1', port: int = 1337, width: int = 40, height: int = 16):
        super().__init__(host, port, width, height)

        _ = BLACK
        G = (24, 208, 0)
        O = (255, 158, 0)
        B = (0, 24, 255)
        g = (137, 149, 149)
        b = (35, 35, 35)
        W = (255, 255, 255)

        s = Surface(40, 16, BLACK)
        s.matrix = [[_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
                    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
                    [_, _, _, G, G, G, G, G, _, _, G, G, G, _, _, _],
                    [_, _, _, G, _, G, _, _, _, G, _, _, _, G, _, _],
                    [_, _, _, _, G, _, _, _, _, G, _, G, G, G, _, _],
                    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
                    [_, _, _, G, G, _, _, _, _, _, G, G, G, G, _, _],
                    [_, _, _, _, _, G, G, G, _, G, _, _, G, _, _, _],
                    [_, _, _, G, G, _, _, _, _, _, G, G, G, G, _, _],
                    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
                    [_, _, _, G, G, G, G, G, _, G, G, G, G, G, _, _],
                    [_, _, _, _, G, _, _, _, _, _, G, _, _, _, _, _],
                    [_, _, _, _, _, G, G, _, _, _, _, G, G, _, _, _],
                    [_, _, _, _, G, _, _, _, _, _, G, _, _, _, _, _],
                    [_, _, _, G, G, G, G, G, _, G, G, G, G, G, _, _],
                    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
                    [_, _, _, G, G, G, G, G, _, G, G, G, G, G, _, _],
                    [_, _, _, _, _, _, _, G, _, G, _, G, _, G, _, _],
                    [_, _, _, _, _, _, _, G, _, G, _, _, _, G, _, _],
                    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
                    [_, _, _, _, _, g, b, g, _, _, _, _, _, _, _, _],
                    [_, _, _, G, G, b, b, b, _, _, _, _, _, _, _, _],
                    [_, _, G, W, G, g, b, g, _, _, _, _, _, _, _, _],
                    [_, _, G, G, G, g, g, g, G, _, _, _, _, _, _, _],
                    [_, _, G, G, G, g, g, g, G, _, _, _, G, _, _, _],
                    [_, _, G, W, G, g, b, g, _, _, _, G, G, G, _, _],
                    [_, _, _, G, G, b, g, b, O, O, G, G, G, O, O, _],
                    [_, _, _, G, O, g, b, g, O, B, G, G, O, O, O, _],
                    [_, O, O, O, O, B, B, O, B, G, G, G, B, O, O, _],
                    [_, O, O, O, O, B, B, O, B, G, G, B, B, O, O, _],
                    [_, _, _, _, O, O, O, O, G, G, G, B, O, O, O, _],
                    [_, _, _, _, _, G, G, O, G, G, O, O, O, O, O, _],
                    [_, _, _, _, _, _, G, G, G, G, _, _, G, G, _, _],
                    [_, _, _, _, _, _, _, G, G, _, _, _, G, G, _, _],
                    [_, _, _, _, _, _, _, _, _, _, _, _, G, G, _, _],
                    [_, _, _, _, _, _, _, _, _, _, _, _, _, G, _, _],
                    [_, _, _, _, _, _, _, _, _, _, _, _, _, G, _, _],
                    [_, _, _, _, _, _, _, _, _, _, _, _, _, G, _, _],
                    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
                    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _]]
        self.blit(s, (int(width / 2) - 20, int(height / 2) - 8))
        self.update()
        sleep(1)
        for _ in range(3):
            if _ == 1:
                s.matrix[22][3] = G
                s.matrix[25][3] = G
            s.matrix[36][13] = BLACK
            s.matrix[37][13] = BLACK
            s.matrix[36][12] = G
            s.matrix[37][12] = G
            self.blit(s, (int(width / 2) - 20, int(height / 2) - 8))
            self.update()
            sleep(1)
            s.matrix[22][3] = W
            s.matrix[25][3] = W
            s.matrix[36][13] = G
            s.matrix[37][13] = G
            s.matrix[36][12] = BLACK
            s.matrix[37][12] = BLACK
            self.blit(s, (int(width / 2) - 20, int(height / 2) - 8))
            self.update()
            sleep(1)
        self.reset()
