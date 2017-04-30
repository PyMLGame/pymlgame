import pymlgame


class TestController:
    TEST_HOST = 'localhost'
    TEST_PORT = 1338

    def test_id(self):
        obj = pymlgame.Controller(self.TEST_HOST, self.TEST_PORT)

    def test_button_keys(self):
        obj = pymlgame.Controller(self.TEST_HOST, self.TEST_PORT)

    def test_ping(self):
        obj = pymlgame.Controller(self.TEST_HOST, self.TEST_PORT)

    def test_trigger_button(self):
        obj = pymlgame.Controller(self.TEST_HOST, self.TEST_PORT)
