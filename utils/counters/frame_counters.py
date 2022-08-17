from typing import Callable


class OneWayCounter:
    """Counter class."""

    def __init__(
        self,
        max_value: float | int,
        reach_max_value_handler: Callable,
        increment_value: float = 1,
        looping: bool = True,
    ) -> None:
        """Set the needed attributes.

        Args:
            max_value (int): the max value of the counter
            reach_max_value_handler (Callable): The function witch is called when the counter reaches the max value.
            increment_value (float, optional): The value with which the counter is increment. Defaults to 1.
        """
        self.counter_value: float = 0
        self.increment_value = increment_value
        self.max_value = max_value
        self.reach_max_value_handler = reach_max_value_handler
        self.looping = looping
        if not self.looping:
            self.counting = False

    def start(self) -> None:
        self.counter_value = 0
        self.counting = True

    def count(self) -> None:
        """Increment the current value of the counter."""
        self.counter_value += self.increment_value
        self.check_max_value()

    def check_max_value(self) -> None:
        """If the counter reaches the max value, then call the handler function."""
        if self.counter_value < self.max_value:
            return

        if not self.looping and self.counting:
            self.reach_max_value_handler()
            self.counting = False
        else:
            self.reach_max_value_handler()
            self.curent_value = 0


class TwoWayCounter:
    def __init__(
        self, max_value: float | int, reach_max_value_handler: Callable = None, increment_value: float = 1
    ) -> None:
        self.dir: int = 1
        self.counter_value: float = 0
        self.increment_value = increment_value
        self.max_value = max_value
        self.reach_max_value_handler = reach_max_value_handler

    def count(self) -> None:
        """Incrementor decrement the current value of the counter."""
        self.counter_value += self.increment_value * self.dir
        self.check_max_value()

    def check_max_value(self) -> None:
        """If the counter reaches the max value, then reverse direction and call the handler function."""
        if self.counter_value < self.max_value and self.counter_value > -1:
            return

        self.reverse_counter_direction()
        self.count()
        if self.reach_max_value_handler:
            self.reach_max_value_handler()

    def reverse_counter_direction(self) -> None:
        """Reverse the counter direction."""
        self.dir *= -1
