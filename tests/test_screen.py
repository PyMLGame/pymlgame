import random

import pymlgame


class TestScreen:
    TEST_HOST = ''
    TEST_PORT = 1337
    TEST_WIDTH = 40
    TEST_HEIGHT = 16

    def test_host_port(self):
        obj = pymlgame.Screen(self.TEST_HOST, self.TEST_PORT, self.TEST_WIDTH, self.TEST_HEIGHT)

        assert obj.host == self.TEST_HOST
        assert obj.port == self.TEST_PORT

    def test_size(self):
        obj = pymlgame.Screen(self.TEST_HOST, self.TEST_PORT, self.TEST_WIDTH, self.TEST_HEIGHT)

        assert obj.width == self.TEST_WIDTH
        assert obj.height == self.TEST_HEIGHT

    def test_reset(self):
        obj = pymlgame.Screen(self.TEST_HOST, self.TEST_PORT, self.TEST_WIDTH, self.TEST_HEIGHT)
        surface = pymlgame.Surface(self.TEST_WIDTH, self.TEST_HEIGHT)

        surface.fill(pymlgame.MAGENTA)
        obj.blit(surface, (0, 0))

        for _ in range(10):
            x = random.randint(0, self.TEST_WIDTH - 1)
            y = random.randint(0, self.TEST_HEIGHT - 1)
            assert obj.matrix[x][y] == pymlgame.MAGENTA

        obj.reset()

        for _ in range(10):
            x = random.randint(0, self.TEST_WIDTH - 1)
            y = random.randint(0, self.TEST_HEIGHT - 1)
            assert obj.matrix[x][y] == pymlgame.BLACK

    def test_matrix(self):
        obj = pymlgame.Screen(self.TEST_HOST, self.TEST_PORT, self.TEST_WIDTH, self.TEST_HEIGHT)

        assert len(obj.matrix) == self.TEST_WIDTH
        assert len(obj.matrix[self.TEST_WIDTH - 1]) == self.TEST_HEIGHT

        assert obj.matrix[0][0] == pymlgame.BLACK
        assert obj.matrix[self.TEST_WIDTH - 1][self.TEST_HEIGHT - 1] == pymlgame.BLACK

    def test_update(self):
        pass

    def test_blit(self):
        obj = pymlgame.Screen(self.TEST_HOST, self.TEST_PORT, self.TEST_WIDTH, self.TEST_HEIGHT)
        surface = pymlgame.Surface(self.TEST_WIDTH - 2, self.TEST_HEIGHT - 2)

        surface.fill(pymlgame.WHITE)
        obj.blit(surface, (1, 1))

        for x in range(self.TEST_WIDTH):
            for y in range(self.TEST_HEIGHT):
                if 0 < x < self.TEST_WIDTH - 1 and 0 < y < self.TEST_HEIGHT - 1:
                    assert obj.matrix[x][y] == pymlgame.WHITE
                else:
                    assert obj.matrix[x][y] == pymlgame.BLACK

    def test_point_on_screen(self):
        obj = pymlgame.Screen(self.TEST_HOST, self.TEST_PORT, self.TEST_WIDTH, self.TEST_HEIGHT)

        assert obj.point_on_screen((0, 0))
        assert obj.point_on_screen((self.TEST_WIDTH - 1, 0))
        assert obj.point_on_screen((0, self.TEST_HEIGHT - 1))
        assert obj.point_on_screen((self.TEST_WIDTH - 1, self.TEST_HEIGHT - 1))
        assert not obj.point_on_screen((-1, -1))
        assert not obj.point_on_screen((self.TEST_WIDTH, 0))
        assert not obj.point_on_screen((0, self.TEST_HEIGHT))
        assert not obj.point_on_screen((self.TEST_WIDTH, self.TEST_HEIGHT))
        assert obj.point_on_screen((self.TEST_WIDTH - 1, self.TEST_HEIGHT - 1))
