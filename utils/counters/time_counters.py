from typing import Callable


class TimeCounter:

    __slots__ = ["counter_value", "seconds", "handler_funct"]

    def __init__(self, seconds: float, handler_funct: Callable) -> None:
        self.counter_value = 0
        self.seconds = seconds
        self.handler_funct = handler_funct

    def count(self, dt: float) -> None:
        self.counter_value += dt

        if self.counter_value >= self.seconds:
            self.counter_value = 0
            self.handler_funct()
