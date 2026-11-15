import pytest

from practice import load

m = load(__file__)


class FakeEngine:
    """A test double: Car must work with anything that has start/stop/running."""

    def __init__(self):
        self.running = False
        self.calls = []

    def start(self):
        self.calls.append("start")
        self.running = True

    def stop(self):
        self.calls.append("stop")
        self.running = False


def test_engine_basics():
    e = m.Engine(100)
    assert e.hp == 100
    assert e.running is False
    e.start()
    assert e.running is True
    e.stop()
    assert e.running is False


@pytest.mark.parametrize("hp", [0, -5])
def test_engine_rejects_bad_hp(hp):
    with pytest.raises(ValueError):
        m.Engine(hp)


def test_car_is_not_an_engine():
    car = m.Car(m.Engine(100))
    assert not isinstance(car, m.Engine)
    assert car.odometer == 0


def test_car_keeps_the_given_engine():
    engine = m.Engine(100)
    assert m.Car(engine).engine is engine


def test_start_and_stop_delegate():
    fake = FakeEngine()
    car = m.Car(fake)
    car.start()
    assert fake.calls == ["start"]
    assert car.is_running is True
    car.stop()
    assert fake.calls == ["start", "stop"]
    assert car.is_running is False


def test_drive_updates_odometer():
    car = m.Car(m.Engine(100))
    car.start()
    assert car.drive(10) == 10
    assert car.drive(5.5) == 15.5
    assert car.odometer == 15.5


def test_drive_needs_running_engine():
    car = m.Car(m.Engine(100))
    with pytest.raises(RuntimeError, match="engine is off"):
        car.drive(1)
    assert car.odometer == 0


@pytest.mark.parametrize("km", [0, -1])
def test_drive_rejects_bad_distance(km):
    car = m.Car(m.Engine(100))
    car.start()
    with pytest.raises(ValueError):
        car.drive(km)


def test_replace_engine():
    old, new = m.Engine(100), m.Engine(200)
    car = m.Car(old)
    car.start()
    returned = car.replace_engine(new)
    assert returned is old
    assert old.running is False
    assert car.engine is new
    assert car.is_running is False
