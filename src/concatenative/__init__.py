import operator

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Mapping, NoReturn, Optional, Sequence, final, override

Error = BaseException

type Result[T] = Error | T

type Try[T] = Optional[T] | Result[T]


class Concatenative[I, O](ABC):
    @abstractmethod
    def __call__(self, value: I) -> O:
        pass

    @final
    def __rrshift__(self, value: I) -> O:
        return self(value)

    @final
    def __ror__[J](self, other: Callable[[J], I]) -> "Concatenative[J, O]":
        return Pipe(lambda j: self(other(j)))

    @final
    def __or__[Q](self, other: Callable[[O], Q]) -> "Concatenative[I, Q]":
        return Pipe(lambda i: other(self(i)))


@dataclass(slots=True)
class Pipe[I, O](Concatenative[I, O]):
    apply: Callable[[I], O]

    @final
    @override
    def __call__(self, value: I) -> O:
        return self.apply(value)


def pipe[I, O](apply: Callable[[I], O]) -> Pipe[I, O]:
    return Pipe(apply)


@pipe
def identity[T](value: T) -> T:
    return value


@dataclass(slots=True)
class Constant[T](Concatenative[Any, T]):
    value: T

    @final
    @override
    def __call__(self, _: Any) -> T:
        return self.value


@dataclass(slots=True)
class Inspect[T](Concatenative[T, T]):
    inspect: Callable[[T], None]

    @final
    @override
    def __call__(self, value: T) -> T:
        self.inspect(value)
        return value


@dataclass(slots=True)
class TryInspect[T](Concatenative[Try[T], Try[T]]):
    inspect: Callable[[T], None]

    @final
    @override
    def __call__(self, value: Try[T]) -> Try[T]:
        if not (value is None or isinstance(value, Error)):
            self.inspect(value)
        return value


@dataclass(slots=True)
class InspectError[T](Concatenative[Try[T], Try[T]]):
    inspect: Callable[[Error], None]

    @final
    @override
    def __call__(self, value: Try[T]) -> Try[T]:
        if isinstance(value, Error):
            self.inspect(value)
        return value


@dataclass(slots=True)
class DropIf[T](Concatenative[T, Optional[T]]):
    predicate: Callable[[T], bool]

    @final
    @override
    def __call__(self, value: T) -> Optional[T]:
        if self.predicate(value):
            return None
        return value


@dataclass(slots=True)
class Filter[T](Concatenative[Try[T], Optional[T]]):
    predicate: Callable[[T], bool]

    @final
    @override
    def __call__(self, value: Try[T]) -> Optional[T]:
        if value is None or isinstance(value, Error) or not self.predicate(value):
            return None
        return value


@dataclass(slots=True)
class Map[T, U](Concatenative[Try[T], Try[U]]):
    transform: Callable[[T], U]

    @final
    @override
    def __call__(self, value: Try[T]) -> Try[U]:
        if value is None or isinstance(value, Error):
            return value
        return self.transform(value)


@dataclass(slots=True)
class FlatMap[T, U](Concatenative[Try[T], Try[U]]):
    transform: Callable[[T], Try[U]]

    @final
    @override
    def __call__(self, value: Try[T]) -> Try[U]:
        if value is None or isinstance(value, Error):
            return value
        return self.transform(value)


@dataclass(slots=True)
class TryMap[T, U](Concatenative[Try[T], Try[U]]):
    transform: Callable[[T], U]

    @final
    @override
    def __call__(self, value: Try[T]) -> Try[U]:
        if value is None or isinstance(value, Error):
            return value
        return guard(self.transform, value)


@dataclass(slots=True)
class MapError[T](Concatenative[Try[T], Try[T]]):
    transform: Callable[[Error], Error]

    @final
    @override
    def __call__(self, value: Try[T]) -> Try[T]:
        if isinstance(value, Error):
            return self.transform(value)
        return value


@dataclass(slots=True)
class OrElse[T](Concatenative[Try[T], T]):
    supply: Callable[[], T]

    @final
    @override
    def __call__(self, value: Try[T]) -> T:
        if value is None or isinstance(value, Error):
            return self.supply()
        return value


@dataclass(slots=True)
class OrDefault[T](Concatenative[Try[T], T]):
    default: T

    @final
    @override
    def __call__(self, value: Try[T]) -> T:
        if value is None or isinstance(value, Error):
            return self.default
        return value


@dataclass(slots=True)
class MapOrElse[T, U](Concatenative[Try[T], U]):
    transform: Callable[[T], U]
    supply: Callable[[], U]

    @final
    @override
    def __call__(self, value: Try[T]) -> U:
        if value is None or isinstance(value, Error):
            return self.supply()
        return self.transform(value)


@dataclass(slots=True)
class MapOrDefault[T, U](Concatenative[Try[T], U]):
    transform: Callable[[T], U]
    default: U

    @final
    @override
    def __call__(self, value: Try[T]) -> U:
        if value is None or isinstance(value, Error):
            return self.default
        return self.transform(value)


@dataclass(slots=True)
class Unwrap[T](Concatenative[Try[T], T]):
    message: str

    @final
    @override
    def __call__(self, value: Try[T]) -> T:
        if value is None:
            raise ValueError(self.message)
        if isinstance(value, Error):
            raise ValueError(self.message) from value
        return value


@dataclass(slots=True)
class Raise(Concatenative[Any, NoReturn]):
    error: Error

    @final
    @override
    def __call__(self, value: Any) -> NoReturn:
        raise self.error


def guard[T](apply: Callable[..., T], *args: Any, **kwargs: Any) -> Result[T]:
    try:
        return apply(*args, **kwargs)
    except Error as e:
        return e


def fallible[T](apply: Callable[..., T]) -> Callable[..., Result[T]]:
    from functools import wraps

    @wraps(apply)
    def wrapper(*args: Any, **kwargs: Any) -> Result[T]:
        return guard(apply, *args, **kwargs)

    return wrapper


@dataclass(init=False, slots=True)
class GetItems[T](Concatenative[T, dict[str, Any]]):
    items: Sequence[str]

    def __init__(self, *items: str) -> None:
        self.items = items

    @final
    @override
    def __call__(self, object: T) -> dict[str, Any]:
        get_item: Callable[[Any, str], Any] = type(object).__getitem__  # type: ignore
        return {key: get_item(object, key) for key in self.items}


@dataclass(init=False, slots=True)
class SetItems[T](Concatenative[T, T]):
    items: Mapping[str, Any]

    def __init__(self, **items: Any) -> None:
        self.items = items

    @final
    @override
    def __call__(self, object: T) -> T:
        set_item: Callable[[Any, str, Any], Any] = type(object).__setitem__  # type: ignore
        for key, value in self.items.items():
            set_item(object, key, value)
        return object


@dataclass(init=False, slots=True)
class GetAttrs[T](Concatenative[T, dict[str, Any]]):
    attrs: Sequence[str]

    def __init__(self, *attrs: str) -> None:
        self.attrs = attrs

    @final
    @override
    def __call__(self, object: T) -> dict[str, Any]:
        return {key: getattr(object, key) for key in self.attrs}


@dataclass(init=False, slots=True)
class SetAttrs[T](Concatenative[T, T]):
    attrs: Mapping[str, Any]

    def __init__(self, **attrs: Any) -> None:
        self.attrs = attrs

    @final
    @override
    def __call__(self, object: T) -> T:
        for key, value in self.attrs.items():
            setattr(object, key, value)
        return object


def debug[T](f: Callable[..., T]) -> Callable[..., T]:
    from functools import wraps

    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        # capture inputs before calling the function because it could potentially mutate them
        f_name = f.__name__
        f_args = ", ".join(map(repr, args))
        f_kwargs = ", ".join(map(lambda kv: f"{kv[0]}={repr(kv[1])}", kwargs.items()))
        f_application = f"{f_name}({f_args}, {f_kwargs})"
        try:
            result = f(*args, **kwargs)
        except Error as e:
            print(f_application, "-> raised", type(e))
            raise e
        print(f_application, "->", result)
        return result

    return wrapper


@pipe
@fallible
def prompt(message: str) -> str:
    return input(message)


def _binary_factory(
    op: Callable[[Any, Any], Any]
) -> Callable[[Any], Concatenative[Any, Any]]:
    @dataclass(slots=True)
    class BinaryOperator[T](Concatenative[T, T]):
        rhs: T

        @final
        @override
        def __call__(self, lhs: T) -> T:
            return op(lhs, self.rhs)

    return BinaryOperator


lt = _binary_factory(operator.lt)
le = _binary_factory(operator.le)
eq = _binary_factory(operator.eq)
ne = _binary_factory(operator.ne)
ge = _binary_factory(operator.ge)
gt = _binary_factory(operator.gt)

add = _binary_factory(operator.add)
floordiv = _binary_factory(operator.floordiv)
mod = _binary_factory(operator.mod)
mul = _binary_factory(operator.mul)
matmul = _binary_factory(operator.matmul)
pow = _binary_factory(operator.pow)
sub = _binary_factory(operator.sub)
truediv = _binary_factory(operator.truediv)
