from typing import final, override
from abc import ABC, abstractmethod


class Apply[I, O](ABC):
    @abstractmethod
    def apply(self, value: I) -> O:
        pass


class Concatenative[I, O](Apply[I, O]):
    @final
    def __call__(self, value: I) -> O:
        return self.apply(value)

    @final
    def __or__[Q](self, other: "Concatenative[O, Q]") -> "Concatenative[I, Q]":
        class Concatenated(Concatenative[I, Q]):
            def __init__(self, head: Apply[I, O], tail: Apply[O, Q]):
                self._head = head
                self._tail = tail

            @override
            def apply(self, value: I) -> Q:
                return self._tail.apply(self._head.apply(value))

        return Concatenated(self, other)
