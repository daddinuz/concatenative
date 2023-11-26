from typing import Callable, Optional, override
from concatenative import Concatenative


class OrElse[T](Concatenative[Optional[T], Optional[T]]):
    def __init__(self, or_else: Callable[[], Optional[T]]):
        self._or_else = or_else

    @override
    def apply(self, value: Optional[T]) -> Optional[T]:
        return self._or_else() if value is None else value
