from typing import Protocol, Self


class IFrom[T: object](Protocol):
    @classmethod
    def from_(cls, source: T) -> Self: ...
