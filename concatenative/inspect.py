from typing import Callable, override
from concatenative import Concatenative


class Inspect[T](Concatenative[T, T]):
    def __init__(self, inspect: Callable[[T], None]):
        self._inspect = inspect

    @override
    def apply(self, value: T) -> T:
        self._inspect(value)
        return value
