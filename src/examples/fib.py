from concatenative import Inspect

from .stacklang import push, lt, pop, sub, add, binrec


def main():
    fib = (
        push([3, lt])
        | push([pop, 1])
        | push([1, sub])
        | push([2, sub])
        | push([add])
        | binrec
    )
    program = push(30) | fib | Inspect(print)
    program([])


if __name__ == "__main__":
    main()
