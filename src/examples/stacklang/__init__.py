import typing

from typing import Any
from concatenative import Pipe, pipe


def apply(code: list[Any]) -> Pipe[list[Any], list[Any]]:
    @pipe
    def inner(stack: list[Any]) -> list[Any]:
        return _call(stack, code)

    return inner


def push(value: Any) -> Pipe[list[Any], list[Any]]:
    @pipe
    def inner(stack: list[Any]) -> list[Any]:
        stack.append(value)
        return stack

    return inner


@pipe
def add(stack: list[Any]) -> list[Any]:
    r = stack.pop()
    stack[-1] += r
    return stack


@pipe
def sub(stack: list[Any]) -> list[Any]:
    r = stack.pop()
    stack[-1] -= r
    return stack


@pipe
def mul(stack: list[Any]) -> list[Any]:
    r = stack.pop()
    stack[-1] *= r
    return stack


@pipe
def div(stack: list[Any]) -> list[Any]:
    r = stack.pop()
    stack[-1] /= r
    return stack


@pipe
def idiv(stack: list[Any]) -> list[Any]:
    r = stack.pop()
    stack[-1] //= r
    return stack


@pipe
def rem(stack: list[Any]) -> list[Any]:
    r = stack.pop()
    stack[-1] %= r
    return stack


@pipe
def boolean_not(stack: list[Any]) -> list[Any]:
    stack[-1] = not stack[-1]
    return stack


@pipe
def boolean_and(stack: list[Any]) -> list[Any]:
    r = stack.pop()
    stack[-1] = stack[-1] and r
    return stack


@pipe
def boolean_or(stack: list[Any]) -> list[Any]:
    r = stack.pop()
    stack[-1] = stack[-1] or r
    return stack


@pipe
def eq(stack: list[Any]) -> list[Any]:
    r = stack.pop()
    stack[-1] = stack[-1] == r
    return stack


@pipe
def ne(stack: list[Any]) -> list[Any]:
    r = stack.pop()
    stack[-1] = stack[-1] != r
    return stack


@pipe
def lt(stack: list[Any]) -> list[Any]:
    r = stack.pop()
    stack[-1] = stack[-1] < r
    return stack


@pipe
def le(stack: list[Any]) -> list[Any]:
    r = stack.pop()
    stack[-1] = stack[-1] <= r
    return stack


@pipe
def gt(stack: list[Any]) -> list[Any]:
    r = stack.pop()
    stack[-1] = stack[-1] > r
    return stack


@pipe
def ge(stack: list[Any]) -> list[Any]:
    r = stack.pop()
    stack[-1] = stack[-1] >= r
    return stack


@pipe
def ifte(stack: list[Any]) -> list[Any]:
    f = stack.pop()
    t = stack.pop()
    c = stack.pop()
    stack = _call(stack, c)
    quote = t if stack.pop() else f
    return _call(stack, quote)


@pipe
def dup(stack: list[Any]) -> list[Any]:
    stack.append(stack[-1])
    return stack


@pipe
def over(stack: list[Any]) -> list[Any]:
    stack.append(stack[-2])
    return stack


@pipe
def pop(stack: list[Any]) -> list[Any]:
    stack.pop()
    return stack


@pipe
def nip(stack: list[Any]) -> list[Any]:
    stack.pop(-2)
    return stack


@pipe
def swap(stack: list[Any]) -> list[Any]:
    stack[-2], stack[-1] = stack[-1], stack[-2]
    return stack


@pipe
def quote(stack: list[Any]) -> list[Any]:
    stack[-1] = [stack[-1]]
    return stack


@pipe
def unquote(stack: list[Any]) -> list[Any]:
    quote = stack.pop()
    return _call(stack, quote)


@pipe
def binrec(stack: list[Any]) -> list[Any]:
    merge = stack.pop()
    right = stack.pop()
    left = stack.pop()
    leave = stack.pop()
    case = stack.pop()
    value = stack[-1]
    return _binrec(stack, value, case, leave, left, right, merge)


def _binrec(
    stack: list[Any],
    value: Any,
    case: list[Any],
    leave: list[Any],
    left: list[Any],
    right: list[Any],
    merge: list[Any],
) -> list[Any]:
    stack = _call(stack, case)

    can_leave = stack[-1]
    stack[-1] = value

    if can_leave:
        return _call(stack, leave)

    stack = _call(stack, left)
    stack = _binrec(stack, stack[-1], case, leave, left, right, merge)

    stack.append(value)
    stack = _call(stack, right)
    stack = _binrec(stack, stack[-1], case, leave, left, right, merge)

    return _call(stack, merge)


def _call(stack: list[Any], code: list[Any]) -> list[Any]:
    for value in code:
        if isinstance(value, Pipe):
            stack = typing.cast(list[Any], value(stack))
        else:
            stack.append(value)
    return stack
