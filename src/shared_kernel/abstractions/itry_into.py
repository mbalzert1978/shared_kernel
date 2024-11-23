from typing import Protocol

from shared_kernel.result_type import Result


class ITryInto[T: object, E](Protocol):
    def try_into(self) -> Result[T, E]: ...
