"""Assignment 2: Compose a Car from an Engine (has-a, not is-a)."""


class Engine:
    """A simple engine.

    Engine(hp)       hp must be positive, else ValueError.
    .running         False at first.
    .start()         set running to True.
    .stop()          set running to False.
    """

    def __init__(self, hp):
        # TODO: validate hp, store it, and start with running = False.
        ...

    def start(self):
        # TODO
        ...

    def stop(self):
        # TODO
        ...


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

    def __init__(self, engine):
        # TODO: keep the given engine and set odometer to 0.
        ...

    def start(self):
        # TODO: delegate to the engine.
        ...

    def stop(self):
        # TODO: delegate to the engine.
        ...

    # TODO: add the is_running property.

    def drive(self, km):
        # TODO
        ...

    def replace_engine(self, new):
        # TODO
        ...


if __name__ == "__main__":
    car = Car(Engine(120))
    car.start()
    print(car.drive(10), car.is_running)
