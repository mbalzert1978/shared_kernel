from dataclasses import dataclass
from http import HTTPStatus
from typing import ClassVar, Self, overload

from shared_kernel.functions import hash_combine


@dataclass(frozen=True)
class Error:
    SEPARATOR: ClassVar = ":"
    code: str
    description: str = ""

    def __str__(self) -> str:
        return f"{self.code}:{self.description}"

    def __repr__(self) -> str:
        return f"Error(code: {self.code}, description:{self.description})"

    def __eq__(self, other: object) -> bool:
        return False if not isinstance(other, Error) else self.code == other.code

    def __hash__(self) -> int:
        return hash_combine(self.code, self.description)

    @classmethod
    def default(cls) -> Self:
        return cls("", "")

    @classmethod
    @overload
    def from_(cls, source: str) -> Self: ...

    @classmethod
    @overload
    def from_(cls, source: HTTPStatus) -> Self: ...

    @classmethod
    def from_(cls, source) -> Self:
        match source:
            case str():
                left, *right = source.split(Error.SEPARATOR)
                return cls(left, next(iter(right), ""))
            case HTTPStatus():
                return cls(str(source.value), source.phrase)
            case _:
                raise ValueError("Invalid source type")
