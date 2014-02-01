#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import pymlgame
from pymlgame.locals import *


class Game(object):
    """
    The main game class that holds the gameloop
    """
    def __init__(self):
        """
        create a screen and define some game specific things
        """
        self.screen = pymlgame.Screen()
        self.running = True
        self.colors = [GREEN, WHITE, RED, YELLOW, BLUE, CYAN]

    def update(self):
        """
        update the screens contents in every loop
        """
        self.screen.fill(BLACK)
        self.screen.draw_dot((0, 0), self.colors[0])
        self.screen.draw_line((3, 0), (20, 3), self.colors[1])
        self.screen.draw_rect((1, 5), (10, 8), self.colors[2], self.colors[3])
        self.screen.draw_circle((20, 5), (8, 8), self.colors[4], self.colors[5])

    def render(self):
        """
        send the current screen content to Mate Light
        """
        self.screen.update()

    def handle_events(self):
        """
        Loop through all events and react to them
        """
        for event in pymlgame.events.get_events():
            if event.type == KEYUP:
                if event.key == K_Arrow_Up or event.key == K_Arrow_Right:
                    self.colors.append(self.colors.pop(0))
                elif event.key == K_Arrow_Down or event.key == K_Arrow_Left:
                    self.colors.insert(0, self.colors.pop())

    def gameloop(self):
        """
        A game loop that circles through the methods
        """
        while self.running:
            self.handle_events()
            self.update()
            self.render()


if __name__ == '__main__':
    GAME = Game()
    GAME.gameloop()