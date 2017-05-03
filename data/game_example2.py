#!/usr/bin/env python3

import pymlgame


class Game:
    def __init__(self):
        pymlgame.init(debug=True)
        self.width = 40
        self.height = 16
        self.screen = pymlgame.Screen('127.0.0.1', 1337, self.width, self.height)
        #self.screen = pymlgame.Screen('matelight.cbrp3.c-base.org', 1337, 40, 16)
        #self.screen = pymlgame.screen.IntroScreen('matelight.cbrp3.c-base.org', 1337, 40, 16)
        self.clock = pymlgame.Clock(200)
        self.surface = pymlgame.Surface(self.width, self.height)
        self.a1 = (0, 0)
        self.a2 = (self.width - 1, self.height - 1)
        self.b1 = (0, self.height - 1)
        self.b2 = (self.width - 1, 0)
        self.c1 = (int(self.width / 2 - 1), 0)
        self.c2 = (int(self.width / 2 - 1), self.height - 1)

    def update(self):
        def move(p):
            x, y = p
            if x == 0 and y < self.height - 1:
                y += 1
            elif y == self.height - 1 and x < self.width - 1:
                x += 1
            elif x == self.width - 1 and y > 0:
                y -= 1
            elif y == 0 and  x > 0:
                x -= 1
            return x, y

        def dark(color):
            return tuple(int(c / 4) for c in color)

        self.surface.fill(pymlgame.BLACK)
        self.a1 = move(self.a1)
        self.a2 = move(self.a2)
        self.b1 = move(self.b1)
        self.b2 = move(self.b2)
        self.c1 = move(self.c1)
        self.c2 = move(self.c2)
        self.surface.draw_line(self.a1, self.a2, pymlgame.CYAN)
        self.surface.draw_line(self.b1, self.b2, pymlgame.MAGENTA)
        self.surface.draw_line(self.c1, self.c2, pymlgame.YELLOW)

    def render(self):
        self.screen.reset()
        self.screen.blit(self.surface)
        self.screen.update()
        self.clock.tick()

    def handle_events(self):
        for event in pymlgame.get_events():
            print(event.id, event.type, event.data)

    def loop(self):
        try:
            while True:
                self.handle_events()
                self.update()
                self.render()
        except KeyboardInterrupt:
            print('KTHXBYE!')

if __name__ == '__main__':
    Game().loop()

