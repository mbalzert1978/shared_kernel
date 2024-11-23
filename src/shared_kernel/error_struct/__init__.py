from dataclasses import dataclass
from http import HTTPStatus
from typing import ClassVar, Self, overload

from shared_kernel.design_by_contract import ArgumentException
from shared_kernel.functions import hash_combine


@dataclass(frozen=True)
class Error:
    _SEPARATOR: ClassVar[str] = ":"
    _EMPTY_STRING: ClassVar[str] = ""
    _INVALID_SOURCE_TYPE: ClassVar[str] = "Invalid source type"
    _STR_FORMAT: ClassVar[str] = "{}{}{}"
    _REPR_FORMAT: ClassVar[str] = "Error(code: {}, description:{})"

    code: str
    description: str = _EMPTY_STRING

    def __str__(self) -> str:
        return self._STR_FORMAT.format(self.code, self._SEPARATOR, self.description)

    def __repr__(self) -> str:
        return self._REPR_FORMAT.format(self.code, self.description)

    def __eq__(self, other: object) -> bool:
        return False if not isinstance(other, Error) else self.code == other.code

    def __hash__(self) -> int:
        return hash_combine(self.code, self.description)

    @classmethod
    def default(cls) -> Self:
        return cls(cls._EMPTY_STRING, cls._EMPTY_STRING)

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
                left, *right = source.split(cls._SEPARATOR)
                return cls(left, next(iter(right), cls._EMPTY_STRING))
            case HTTPStatus():
                return cls(str(source.value), source.phrase)
            case _:
                raise ArgumentException(cls._INVALID_SOURCE_TYPE, str(source))
