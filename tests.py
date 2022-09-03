from todozer import scheduler
import datetime

def test_x():
    matched = scheduler.match("- Сделать бочку; каждый день", datetime.date.today())
    assert matched is True
