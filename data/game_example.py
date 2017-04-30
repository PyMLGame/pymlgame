#!/usr/bin/env python3

"""
pymlgame - example game
=======================

This example shows how a simple pymlgame could be written. You also need a connected controller to actually see
something happening. You can use the controller example for this.
"""

import pymlgame


class Game:
    """
    The main game class that holds the gameloop, update and render methods.
    """
    def __init__(self):
        """
        Create a screen and define some game specific things.
        """
        self.host = '127.0.0.1'
        self.port = 1337
        self.width = 40
        self.height = 16

        self.players = {}

        # initialize pymlgame
        pymlgame.init()

        # define a screen (matelight)
        self.screen = pymlgame.Screen(self.host, self.port, self.width, self.height)
        # create a clock to get 15 fps frame limit
        self.clock = pymlgame.Clock(15)


        self.running = True

        # create some surfaces
        self.corners = pymlgame.Surface(self.screen.width, self.screen.height)
        self.lines = pymlgame.Surface(int(self.screen.width / 2) - 2,
                                      int(self.screen.height / 2) - 2)
        self.rects = pymlgame.Surface(int(self.screen.width / 2) - 2,
                                      int(self.screen.height / 2) - 2)
        self.circle = pymlgame.Surface(int(self.screen.width / 2) - 2,
                                       int(self.screen.height / 2) - 2)
        self.filled = pymlgame.Surface(int(self.screen.width / 2) - 2,
                                       int(self.screen.height / 2) - 2)

        self.colors = [pymlgame.BLUE, pymlgame.CYAN, pymlgame.GREEN, pymlgame.RED, pymlgame.MAGENTA]

        # Set a timer that switches colors every 10 seconds
        pymlgame.Clock.timer(10, self.swap_colors)


    def swap_colors(self):
        self.colors.append(self.colors.pop(0))
        pymlgame.Clock.timer(10, self.swap_colors)

    def update(self):
        """
        Update the screen contents in every loop.
        """
        # this is not really neccesary because the surface is black after initializing
        self.corners.fill(pymlgame.BLACK)
        self.corners.draw_dot((0, 0), pymlgame.WHITE)
        self.corners.draw_dot((self.screen.width - 1, 0), pymlgame.WHITE)
        self.corners.draw_dot((self.screen.width - 1, self.screen.height - 1), pymlgame.WHITE)
        self.corners.draw_dot((0, self.screen.height - 1), pymlgame.WHITE)

        self.lines.fill(pymlgame.BLACK)
        self.lines.draw_line((1, 0), (self.lines.width - 1, 0), self.colors[0])
        self.lines.draw_line((0, 1), (0, self.lines.height - 1), self.colors[1])
        self.lines.draw_line((0, 0), (self.lines.width - 1, self.lines.height - 1), self.colors[2])

        self.rects.fill(pymlgame.BLACK)
        self.rects.draw_rect((0, 0), (int(self.rects.width / 2) - 1, self.rects.height), self.colors[3], self.colors[4])
        self.rects.draw_rect((int(self.rects.width / 2) + 1, 0), (int(self.rects.width / 2) - 1, self.rects.height), self.colors[4], self.colors[3])

        #self.circle.fill(pymlgame.BLACK)
        #radius = int(min(self.circle.width, self.circle.height) / 2) - 1
        #self.circle.draw_circle((int(self.circle.width / 2) - 1, int(self.circle.height / 2) - 1), radius, pymlgame.MAGENTA, pymlgame.YELLOW)

        self.filled.fill(pymlgame.RED)

    def render(self):
        """
        Draw and send the current screen content to Mate Light.
        """
        self.screen.reset()
        self.screen.blit(self.corners)
        self.screen.blit(self.lines, (1, 1))
        self.screen.blit(self.rects, (int(self.screen.width / 2) + 1, 1))
        self.screen.blit(self.circle, (0, int(self.screen.height / 2) + 1))
        self.screen.blit(self.filled, (int(self.screen.width / 2) + 1, int(self.screen.height / 2) + 1))

        self.screen.update()
        self.clock.tick()

    def handle_events(self):
        """
        Loop through all events.
        """
        for event in pymlgame.get_events():
            if event.type == pymlgame.E_NEWCTLR:
                print('### new player %s connected' % event.id)
                self.players[event.id] = {'name': event.id.hex, 'score': 0}
            elif event.type == pymlgame.E_DISCONNECT:
                print('### player %s disconnected' % event.id)
                self.players.pop(event.id)
            elif event.type == pymlgame.E_KEYDOWN:
                print('### %s pressed %s' % (self.players[event.id]['name'], event.data))
                self.colors.append(self.colors.pop(0))
            elif event.type == pymlgame.E_KEYUP:
                print( '### %s released %s' % (self.players[event.id]['name'], event.data))
                self.colors.append(self.colors.pop(0))
            elif event.type == pymlgame.E_PING:
                print('### ping from %s' % self.players[event.id]['name'])

    def gameloop(self):
        """
        A game loop that circles through the methods.
        """
        try:
            while True:
                self.handle_events()
                self.update()
                self.render()
        except KeyboardInterrupt:
            print('KTHXBYE!')


if __name__ == '__main__':
    GAME = Game()
    GAME.gameloop()
