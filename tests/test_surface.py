import random

import pymlgame


class TestSurface:
    TEST_WIDTH = 40
    TEST_HEIGHT = 16

    def test_size(self):
        obj = pymlgame.Surface(self.TEST_WIDTH, self.TEST_HEIGHT)

        assert obj.width == self.TEST_WIDTH
        assert obj.height == self.TEST_HEIGHT

    def test_matrix(self):
        obj = pymlgame.Surface(self.TEST_WIDTH, self.TEST_HEIGHT)

        assert len(obj.matrix) == self.TEST_WIDTH
        assert len(obj.matrix[self.TEST_WIDTH - 1]) == self.TEST_HEIGHT

        assert obj.matrix[0][0] == pymlgame.BLACK
        assert obj.matrix[self.TEST_WIDTH - 1][self.TEST_HEIGHT - 1] == pymlgame.BLACK

    def test_fill(self):
        obj = pymlgame.Surface(self.TEST_WIDTH, self.TEST_HEIGHT)

        obj.fill(pymlgame.BLUE)

        assert obj.matrix[0][0] == pymlgame.BLUE
        assert obj.matrix[self.TEST_WIDTH - 1][0] == pymlgame.BLUE
        assert obj.matrix[0][self.TEST_HEIGHT - 1] == pymlgame.BLUE
        assert obj.matrix[self.TEST_WIDTH - 1][self.TEST_HEIGHT - 1] == pymlgame.BLUE
        for _ in range(10):
            assert obj.matrix[random.randrange(0, self.TEST_WIDTH)][random.randrange(0, self.TEST_HEIGHT)] == pymlgame.BLUE

    def test_draw_dot(self):
        obj = pymlgame.Surface(self.TEST_WIDTH, self.TEST_HEIGHT)

        # create 10 random dots
        randpoints = [(random.randrange(0, self.TEST_WIDTH), random.randrange(0, self.TEST_HEIGHT)) for _ in range(10)]
        # draw the dots
        for point in randpoints:
            obj.draw_dot(point, pymlgame.YELLOW)
        # test if drawing was successful
        for x in range(self.TEST_WIDTH):
            for y in range(self.TEST_HEIGHT):
                color = obj.matrix[x][y]
                if (x, y) in randpoints:
                    assert color == pymlgame.YELLOW
                else:
                    assert color == pymlgame.BLACK

    def test_draw_line(self):
        obj = pymlgame.Surface(self.TEST_WIDTH, self.TEST_HEIGHT)

        obj.draw_line((1, 0), (self.TEST_WIDTH - 1, 0), pymlgame.GREY6)
        obj.draw_line((0, 1), (0, self.TEST_HEIGHT - 1), pymlgame.RED)
        test_len = max(self.TEST_WIDTH, self.TEST_HEIGHT)
        obj.draw_line((test_len - 2, test_len - 2), (2, 2), pymlgame.CYAN)

        for x in range(1, self.TEST_WIDTH):
            assert obj.matrix[x][0] == pymlgame.GREY6
            assert obj.matrix[x][1] == pymlgame.BLACK
        for y in range(1, self.TEST_HEIGHT):
            assert obj.matrix[0][y], pymlgame.RED
            assert obj.matrix[1][y], pymlgame.BLACK
        for z in range(2, test_len - 1):
            assert obj.matrix[z][z] == pymlgame.CYAN
            assert obj.matrix[z + 1][z] == pymlgame.BLACK
            assert obj.matrix[z][z + 1] == pymlgame.BLACK

    def test_draw_rect(self):
        obj = pymlgame.Surface(self.TEST_WIDTH, self.TEST_HEIGHT)

        obj.draw_rect((1, 1), (self.TEST_WIDTH - 2, self.TEST_HEIGHT - 2), pymlgame.DARKYELLOW, None)

        for x in range(self.TEST_WIDTH):
            for y in range(self.TEST_HEIGHT):
                if x == 1 and 0 < y < self.TEST_HEIGHT - 1 or \
                   x == self.TEST_WIDTH - 2 and 0 < y < self.TEST_HEIGHT - 1 or \
                   self.TEST_WIDTH - 2 > x > 1 == y or \
                   1 < x < self.TEST_WIDTH - 2 and y == self.TEST_HEIGHT - 2:
                    assert obj.matrix[x][y] == pymlgame.DARKYELLOW
                else:
                    assert obj.matrix[x][y] == pymlgame.BLACK

        obj.fill(pymlgame.BLACK)
        obj.draw_rect((int(self.TEST_WIDTH / 2) + 1, int(self.TEST_HEIGHT / 2) + 1),
                      (1, 1), pymlgame.MAGENTA, pymlgame.DARKCYAN)

    def test_draw_circle(self):
        obj = pymlgame.Surface(self.TEST_WIDTH, self.TEST_HEIGHT)

        # TODO: invent a way to draw this, then a way to test this
        pos = (int(self.TEST_WIDTH / 2) - 1, int(self.TEST_HEIGHT / 2) - 1)
        radius = int(min(self.TEST_WIDTH, self.TEST_HEIGHT) / 2) - 2
        obj.draw_circle(pos, radius, pymlgame.GREEN, None)

    def test_blit(self):
        obj = pymlgame.Surface(self.TEST_WIDTH, self.TEST_HEIGHT)

        surface = pymlgame.Surface(self.TEST_WIDTH - 2, self.TEST_HEIGHT - 2)
        surface.fill(pymlgame.WHITE)
        obj.blit(surface, (1, 1))

        for x in range(self.TEST_WIDTH):
            for y in range(self.TEST_HEIGHT):
                if 0 < x < self.TEST_WIDTH - 1 and 0 < y < self.TEST_HEIGHT - 1:
                    assert obj.matrix[x][y] == pymlgame.WHITE
                else:
                    assert obj.matrix[x][y] == pymlgame.BLACK
