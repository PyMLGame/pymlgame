import pymlgame


class TestController:
    TEST_HOST = 'localhost'
    TEST_PORT = 0

    def test_id(self):
        obj = pymlgame.Controller(self.TEST_HOST, 0)
        self.TEST_PORT = obj._sock.getsockname()[1]
        assert isinstance(self.TEST_PORT, int)

    def test_button_keys(self):
        obj = pymlgame.Controller(self.TEST_HOST, 0)
        self.TEST_PORT = obj._sock.getsockname()[1]
        assert isinstance(self.TEST_PORT, int)

    def test_ping(self):
        obj = pymlgame.Controller(self.TEST_HOST, 0)
        self.TEST_PORT = obj._sock.getsockname()[1]
        assert isinstance(self.TEST_PORT, int)

    def test_trigger_button(self):
        obj = pymlgame.Controller(self.TEST_HOST, 0)
        self.TEST_PORT = obj._sock.getsockname()[1]
        assert isinstance(self.TEST_PORT, int)
