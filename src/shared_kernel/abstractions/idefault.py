from typing import Protocol, Self


class IDefault(Protocol):
    @classmethod
    def default(cls) -> Self: ...
