import math
import logging
from typing import List, Tuple


class Surface:
    def __init__(self, width: int, height: int):
        self.logger = logging.getLogger('surface')

        self.width: int = width
        self.height: int = height

        self.matrix: List[List[Tuple[int, int, int]]]

        self.fill()

    def fill(self, color: Tuple[int, int, int] = None):
        """
        Fill the surface with the given color or make it transparent.
        
        :param color: Color as tuple or None for transparency [default: None].
        :type color: tuple
        :return: 
        """
        for x in range(self.width):
            for y in range(self.height):
                self.matrix[x][y] = color

    def draw_dot(self, position: Tuple[int, int], color: Tuple[int, int, int]):
        """
        Draw one single dot with the given color on the surface.

        :param position: Position of the dot
        :param color: Color for the dot
        :type position: tuple
        :type color: tuple
        """
        if 0 <= position[0] < self.width and 0 <= position[1] < self.height:
            self.matrix[position[0]][position[1]] = color
        else:
            self.logger.debug('Trying to draw outside surface, position %d, %d' % position)

    def draw_line(self, start, end, color):
        """
        Draw a line with the given color on the surface.

        :param start: Start point of the line
        :param end: End point of the line
        :param color: Color of the line
        :type start: tuple
        :type end: tuple
        :type color: tuple
        """
        def dist(point: Tuple[int, int], start: Tuple[int, int], end: Tuple[int, int]) -> float:
            """
            Check distance from pixel to actual line.
            
            :param point: Point to check
            :param start: Start point of the line
            :param end: End point of the line
            :return: 
            """
            # TODO: wtf is this?!
            return abs((end[0] - start[0]) * (start[1] - point[1]) - (start[0] - point[0]) * (end[1] - start[1])) / math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)

        for x in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
            for y in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                d: float = dist((x, y), start, end)
                if d < 0.5:
                    self.draw_dot((x, y), color)
                # TODO: antialiasing
                #elif d < 0.7:
                #    self.draw_dot((x, y), color)

    def draw_rect(self, position: Tuple[int, int], size: Tuple[int, int], color: Tuple[int, int, int], fillcolor: Tuple[int, int, int] = None):
        """
        Draw a rectangle with the given color on the surface and optionally fill it with color.

        :param position: Top left corner of the rectangle
        :param size: Width and height of the rectangle
        :param color: Color for borders
        :param fillcolor: Color for infill
        :type position: tuple
        :type size: tuple
        :type color: tuple
        :type fillcolor: tuple
        """
        # draw filled rect
        if fillcolor:
            for x in range(size[0]):
                for y in range(size[1]):
                    self.draw_dot((position[0] + x, position[1] + y), fillcolor)
        # draw top and botton line
        for x in range(size[0]):
            self.draw_dot((position[0] + x, position[1]), color)
            self.draw_dot((position[0] + x, position[1] + size[1] - 1), color)
        # draw left and right side
        for y in range(size[1]):
            self.draw_dot((position[0], position[1] + y), color)
            self.draw_dot((position[0] + size[0] - 1, position[1] + y), color)

    def draw_circle(self, position: Tuple[int, int], radius: int, color: Tuple[int, int, int], fillcolor: Tuple[int, int, int] = None):
        """
        Draw a circle with the given color on the screen and optionally fill it with fillcolor.

        :param position: Center of the circle
        :param radius: Radius
        :param color: Color for border
        :param fillcolor: Color for infill
        :type position: tuple
        :type radius: int
        :type color: tuple
        :type fillcolor: tuple
        """
        # TODO: This still produces rubbish but it's on a good way to success
        def dist(d, p, r):
            return abs(math.sqrt((p[0] - d[0])**2 + (p[1] - d[1])**2) - r)

        points = []
        for x in range(position[0] - radius, position[0] + radius):
            for y in range(position[1] - radius, position[1] + radius):
                if 0 < x < self.width and 0 < y < self.height:
                    if dist((x, y), position, radius) < 1.3:
                        points.append((x, y))

        # draw fill color
        if fillcolor:
            for point in points:
                pass
        # draw outline
        for point in points:
            self.draw_dot(point, color)

    def blit(self, surface: Surface, position: Tuple[int, int] = (0, 0)):
        """
        Blits a surface on this surface at position

        :param surface: Surface to blit
        :param position: Top left point to start blitting
        :type surface: Surface
        :type position: tuple
        """
        for x in range(surface.width):
            for y in range(surface.height):
                px = x + position[0]
                py = y + position[1]
                if 0 < px < self.width and 0 < py < self.height:
                    self.matrix[px][py] = surface.matrix[x][y]
