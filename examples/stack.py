from typing import Any
from concatenative import *


def push(value: Any) -> Concatenative[list[Any], list[Any]]:
    @wraps
    def push(stack: list[Any]) -> list[Any]:
        stack.append(value)
        return stack
    return push


@wraps
def add(stack: list[Any]) -> list[Any]:
    r = stack.pop()
    stack[-1] += r
    return stack


@wraps
def sub(stack: list[Any]) -> list[Any]:
    r = stack.pop()
    stack[-1] -= r
    return stack


@wraps
def mul(stack: list[Any]) -> list[Any]:
    r = stack.pop()
    stack[-1] *= r
    return stack


@wraps
def div(stack: list[Any]) -> list[Any]:
    r = stack.pop()
    stack[-1] /= r
    return stack


@wraps
def rem(stack: list[Any]) -> list[Any]:
    r = stack.pop()
    stack[-1] %= r
    return stack


@wraps
def boolean_not(stack: list[Any]) -> list[Any]:
    stack[-1] = not stack[-1]
    return stack


@wraps
def boolean_and(stack: list[Any]) -> list[Any]:
    r = stack.pop()
    stack[-1] = stack[-1] and r
    return stack


@wraps
def boolean_or(stack: list[Any]) -> list[Any]:
    r = stack.pop()
    stack[-1] = stack[-1] or r
    return stack


@wraps
def eq(stack: list[Any]) -> list[Any]:
    r = stack.pop()
    stack[-1] = stack[-1] == r
    return stack


@wraps
def ne(stack: list[Any]) -> list[Any]:
    r = stack.pop()
    stack[-1] = stack[-1] != r
    return stack


@wraps
def lt(stack: list[Any]) -> list[Any]:
    r = stack.pop()
    stack[-1] = stack[-1] < r
    return stack


@wraps
def le(stack: list[Any]) -> list[Any]:
    r = stack.pop()
    stack[-1] = stack[-1] <= r
    return stack


@wraps
def gt(stack: list[Any]) -> list[Any]:
    r = stack.pop()
    stack[-1] = stack[-1] > r
    return stack


@wraps
def ge(stack: list[Any]) -> list[Any]:
    r = stack.pop()
    stack[-1] = stack[-1] >= r
    return stack


@wraps
def ifte(stack: list[Any]) -> list[Any]:
    f = stack.pop()
    t = stack.pop()
    stack = unquote(stack)
    stack[-1] = t if stack[-1] else f
    return unquote(stack)


@wraps
def dup(stack: list[Any]) -> list[Any]:
    stack.append(stack[-1])
    return stack


@wraps
def over(stack: list[Any]) -> list[Any]:
    stack.append(stack[-2])
    return stack


@wraps
def pop(stack: list[Any]) -> list[Any]:
    stack.pop()
    return stack


@wraps
def nip(stack: list[Any]) -> list[Any]:
    stack.pop(-2)
    return stack


@wraps
def swap(stack: list[Any]) -> list[Any]:
    stack[-2], stack[-1] = stack[-1], stack[-2]
    return stack


@wraps
def quote(stack: list[Any]) -> list[Any]:
    stack[-1] = [stack[-1]]
    return stack


@wraps
def unquote(stack: list[Any]) -> list[Any]:
    quote = stack.pop()
    for value in quote:
        if isinstance(value, Concatenative):
            stack = value.apply(stack)
        else:
            stack.append(value)
    return stack


@wraps
def binrec(stack: list[Any]) -> list[Any]:
    merge = stack.pop()
    right = stack.pop()
    left = stack.pop()
    leave = stack.pop()
    case = stack[-1]
    value = stack[-2]

    stack = unquote(stack)
    if stack[-1]:
        stack[-1] = value
        stack.append(leave)
        return unquote(stack)

    setup = [case, leave, left, right, merge]

    stack[-1] = value
    stack.append(left)
    stack = unquote(stack)

    stack.append(case)
    stack.append(leave)
    stack.append(left)
    stack.append(right)
    stack.append(merge)
    stack = binrec(stack)

    stack.append(value)
    stack.append(right)
    stack = unquote(stack)

    stack.append(case)
    stack.append(leave)
    stack.append(left)
    stack.append(right)
    stack.append(merge)
    stack = binrec(stack)

    stack.append(merge)
    return unquote(stack)


def main():
    fib = push([3, lt]) | push([pop, 1]) | push([1, sub]) | push([2, sub]) | push([add]) | binrec
    program = push(30) | fib | Inspect(print)
    program.apply([])


if __name__ == '__main__':
    main()
