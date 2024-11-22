from typing import Protocol, Self

from shared_kernel.result_type import Result


class ITryFrom[T: object](Protocol):
    @classmethod
    def try_from(cls, source: T) -> Result[Self, Exception]: ...
