from typing import override
from concatenative import Concatenative


class _Identity[T](Concatenative[T, T]):
    @override
    def apply(self, value: T) -> T:
        return value


Identity = _Identity()
