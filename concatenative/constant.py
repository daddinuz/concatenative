from typing import override
from concatenative import Concatenative


class Constant[T](Concatenative[T, T]):
    def __init__(self, value: T):
        self._value

    @override
    def apply(self, value: T) -> T:
        return self._value
