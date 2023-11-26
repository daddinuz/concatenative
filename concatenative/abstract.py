from typing import final, override
from abc import ABC, abstractmethod


class Concatenative[I, O](ABC):
    @abstractmethod
    def apply(self, value: I) -> O:
        pass

    @final
    def __call__(self, value: I) -> O:
        return self.apply(value)

    @final
    def concat[K](self, other: "Concatenative[O, K]") -> "Concatenative[I, K]":
        class Concatenated(Concatenative[I, K]):
            def __init__(self, head: Concatenative[I, O], tail: Concatenative[O, K]):
                self._head = head
                self._tail = tail

            @override
            def apply(self, value: I) -> K:
                return self._tail.apply(self._head.apply(value))

        return Concatenated(self, other)

    @final
    def __or__[K](self, other: "Concatenative[O, K]") -> "Concatenative[I, K]":
        return self.concat(other)
