from typing import Callable, Optional, override
from concatenative import Concatenative


class Then[T, U](Concatenative[Optional[T], Optional[U]]):
    def __init__(self, then: Callable[[T], Optional[U]]):
        self._then = then

    @override
    def apply(self, value: Optional[T]) -> Optional[U]:
        return value if value is None else self._then(value)
