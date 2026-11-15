"""Assignment 2: Compose a Car from an Engine (has-a, not is-a)."""


class Engine:
    """A simple engine.

    Engine(hp)       hp must be positive, else ValueError.
    .running         False at first.
    .start()         set running to True.
    .stop()          set running to False.
    """

    def __init__(self, hp: int) -> None:
        if hp <= 0:
            raise ValueError("hp must be positive")
        self.hp = hp
        self.running = False

    def start(self) -> None:
        self.running = True

    def stop(self) -> None:
        self.running = False


class Car:
    """A car that HAS an engine and delegates to it.

    Car(engine)            keeps the engine it is given (do not create one inside).
    .odometer              kilometres driven, starts at 0.
    .start() / .stop()     delegate to the engine.
    .is_running            property: True when the engine is running.
    .drive(km)             km must be > 0, else ValueError.
                           If the engine is not running raise RuntimeError("engine is off").
                           Otherwise add km to the odometer and return the new odometer value.
    .replace_engine(new)   stop the old engine, switch to the new one (not started),
                           and return the old engine.
    """

    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        self.odometer = 0

    def start(self) -> None:
        self.engine.start()

    def stop(self) -> None:
        self.engine.stop()

    @property
    def is_running(self) -> bool:
        return self.engine.running

    def drive(self, km: float) -> float:
        if km <= 0:
            raise ValueError("km must be positive")
        if not self.engine.running:
            raise RuntimeError("engine is off")
        self.odometer += km
        return self.odometer

    def replace_engine(self, new: Engine) -> Engine:
        old = self.engine
        old.stop()
        self.engine = new
        return old


if __name__ == "__main__":
    car = Car(Engine(120))
    car.start()
    print(car.drive(10), car.is_running)
