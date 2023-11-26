from typing import Callable, Optional, override
from concatenative import Concatenative


class Select[T](Concatenative[T, Optional[T]]):
    def __init__(self, select: Callable[[T], bool]):
        self._select = select

    @override
    def apply(self, value: T) -> Optional[T]:
        return value if self._select(value) else None
