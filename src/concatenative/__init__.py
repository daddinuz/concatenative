from typing import Any, Callable, Optional, final


type Fn[I, O] = Callable[[I], O]


class Pipe[I, O]:
    __slots__ = "_fn"

    def __init__(self, fn: Fn[I, O]) -> None:
        self._fn = fn

    @final
    def __call__(self, object: I) -> O:
        return self._fn(object)

    @final
    def __or__[Q](self, other: Fn[O, Q]) -> "Pipe[I, Q]":
        return Pipe(lambda i: other(self(i)))

    @final
    def __ror__[J](self, other: Fn[J, I]) -> "Pipe[J, O]":
        return Pipe(lambda j: self(other(j)))

    @final
    def __repr__(self) -> str:
        return repr(self._fn)

    @final
    def __hash__(self) -> int:
        return hash(self._fn)

    @final
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Pipe) and self._fn == other._fn  # type: ignore


def pipe[I, O](fn: Fn[I, O]) -> Pipe[I, O]:
    return Pipe(fn)


def constant[T](object: T) -> Pipe[Any, T]:
    @pipe
    def inner(_: Any) -> T:
        return object

    return inner


@pipe
def identity[T](object: T) -> T:
    return object


def inspect[T](fn: Fn[T, None]) -> Pipe[T, T]:
    @pipe
    def inner(object: T) -> T:
        fn(object)
        return object

    return inner


def project(*args: str) -> Pipe[Any, dict[str, Any]]:
    @pipe
    def inner(object: Any) -> dict[str, Any]:
        return {field: getattr(object, field) for field in args}

    return inner


def update[T](**kwargs: Any) -> Pipe[T, T]:
    @pipe
    def inner(object: T) -> T:
        for key, value in kwargs.items():
            setattr(object, key, value)
        return object

    return inner


def select[T](fn: Fn[T, bool]) -> Pipe[T, Optional[T]]:
    @pipe
    def inner(object: T) -> Optional[T]:
        return object if fn(object) else None

    return inner


def then[T, U](fn: Fn[T, U]) -> Pipe[Optional[T], Optional[U]]:
    @pipe
    def inner(object: Optional[T]) -> Optional[U]:
        return None if object is None else fn(object)

    return inner


def or_else[T](fn: Callable[[], T]) -> Pipe[Optional[T], T]:
    @pipe
    def inner(object: Optional[T]) -> T:
        return fn() if object is None else object

    return inner


@pipe
def unwrap[T](object: Optional[T]) -> T:
    if object is None:
        raise ValueError("unable to unwrap object")
    return object


def expect[T](msg: str) -> Pipe[Optional[T], T]:
    @pipe
    def inner(object: Optional[T]) -> T:
        if object is None:
            raise ValueError(f"expected: {msg}")
        return object

    return inner
