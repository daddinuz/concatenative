import typing

from typing import Any
from concatenative import Pipe, pipe, inspect


def apply(code: list[Any]) -> Pipe[list[Any], list[Any]]:
    @pipe
    def inner(stack: list[Any]) -> list[Any]:
        return call(stack, code)

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
    stack = call(stack, c)
    quote = t if stack.pop() else f
    return call(stack, quote)


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
    return call(stack, quote)


@pipe
def binrec(stack: list[Any]) -> list[Any]:
    merge = stack.pop()
    right = stack.pop()
    left = stack.pop()
    leave = stack.pop()
    case = stack.pop()
    value = stack[-1]
    return binrec_aux(stack, value, case, leave, left, right, merge)


def binrec_aux(
    stack: list[Any],
    value: Any,
    case: list[Any],
    leave: list[Any],
    left: list[Any],
    right: list[Any],
    merge: list[Any],
) -> list[Any]:
    stack = call(stack, case)

    can_leave = stack[-1]
    stack[-1] = value

    if can_leave:
        return call(stack, leave)

    stack = call(stack, left)
    stack = binrec_aux(stack, stack[-1], case, leave, left, right, merge)

    stack.append(value)
    stack = call(stack, right)
    stack = binrec_aux(stack, stack[-1], case, leave, left, right, merge)

    return call(stack, merge)


def call(stack: list[Any], code: list[Any]) -> list[Any]:
    for value in code:
        if isinstance(value, Pipe):
            stack = typing.cast(list[Any], value(stack))
        else:
            stack.append(value)
    return stack


def main():
    fib = (
        push([3, lt])
        | push([pop, 1])
        | push([1, sub])
        | push([2, sub])
        | push([add])
        | binrec
    )
    program = push(30) | fib | inspect(print)
    program([])


if __name__ == "__main__":
    main()
