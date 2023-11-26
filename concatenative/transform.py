from typing import Callable, override
from concatenative import Concatenative


class Transform[T, U](Concatenative[T, U]):
    def __init__(self, transform: Callable[[T], U]):
        self._transform = transform

    @override
    def apply(self, value: T) -> U:
        return self._transform(value)
