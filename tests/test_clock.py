from datetime import datetime, timedelta

import pymlgame


class ClockTest:
    def test_tick(self):
        obj = pymlgame.Clock()

        before = datetime.now()
        obj.tick(24)
        after = datetime.now()
        assert after >= before + timedelta(seconds=24)
