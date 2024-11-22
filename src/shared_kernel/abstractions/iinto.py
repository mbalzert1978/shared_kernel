from typing import Protocol


class IInto[T: object](Protocol):
    def into(self) -> T: ...
