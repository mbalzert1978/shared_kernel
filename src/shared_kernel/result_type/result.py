from dataclasses import dataclass

from shared_kernel.design_by_contract.arguments import ArgumentException
from shared_kernel.functions.hash_functions import hash_combine

type Result[T, E] = Ok[T] | Err[E]


@dataclass(frozen=True, slots=True)
class Ok[T]:
    """Success variant of Result."""

    value: T

    def __str__(self) -> str:
        return f"Ok({self.value})"

    def __repr__(self) -> str:
        return f"Ok(value={self.value!r})"

    def __hash__(self) -> int:
        return hash_combine(self.__class__.__name__, self.value)

    def __eq__(self, other: object) -> bool:
        match other:
            case Ok(value):
                return self.value == value
            case _:
                return False


@dataclass(frozen=True, slots=True)
class Err[E]:
    """Error variant of Result."""

    error: E

    def __str__(self) -> str:
        return f"Err({self.error})"

    def __repr__(self) -> str:
        return f"Err(error={self.error!r})"

    def __hash__(self) -> int:
        return hash_combine(self.__class__.__name__, self.error)

    def __eq__(self, other: object) -> bool:
        match other:
            case Err(error):
                return self.error == error
            case _:
                return False


class ResultFactory[T, E]:
    """Factory class for creating Result instances."""

    @staticmethod
    def ok(value: T) -> Result[T, E]:
        """Create an Ok variant."""
        ArgumentException.raise_if_none(value, "value")
        return Ok[T](value)

    @staticmethod
    def err(error: E) -> Result[T, E]:
        """Create an Err variant."""
        ArgumentException.raise_if_none(error, "error")
        return Err[E](error)
