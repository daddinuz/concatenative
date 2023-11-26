import functools

from typing import Callable, override
from concatenative import Concatenative


def wraps[T, U](f: Callable[[T], U]) -> Concatenative[T, U]:
    class Wrapper(Concatenative[T, U]):
        @override
        def apply(self, value: T) -> U:
            return f(value)

    wrapper = Wrapper()
    functools.update_wrapper(wrapper, f)
    return wrapper
