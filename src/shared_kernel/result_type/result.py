from dataclasses import dataclass
from typing import Callable, ClassVar, cast

from shared_kernel.design_by_contract import ArgumentException
from shared_kernel.functions import hash_combine
from shared_kernel.result_type.UnwrapFailedException import UnwrapFailedException


@dataclass
class Result[T: object, E]:
    __match_args__ = ("_is_ok", "_value", "_error")
    __slots__ = ("_is_ok", "_value", "_error")

    STRING_FORMAT: ClassVar[str] = "Result({}, {})"
    REPR_FORMAT: ClassVar[str] = "Result(is_ok={}, value={}, error={})"

    _is_ok: bool
    _value: T | None
    _error: E | None

    def __str__(self):
        return self.STRING_FORMAT.format(self._value, self._error)

    def __repr__(self):
        return self.REPR_FORMAT.format(self._is_ok, self._value, self._error)

    def __eq__(self, other: object) -> bool:
        return (
            False
            if not isinstance(other, Result)
            else self._is_ok == other._is_ok
            and self._value == other._value
            and self._error == other._error
        )

    def __hash__(self) -> int:
        return hash_combine(self._is_ok, self._value, self._error)

    @classmethod
    def Ok(cls, value: T) -> "Result[T, E]":
        ArgumentException.raise_if_none(value, "Ok.value")
        return cls(True, value, None)

    @classmethod
    def Err(cls, error: E) -> "Result[T, E]":
        ArgumentException.raise_if_none(error, "Err.error")
        return cls(False, None, error)

    def is_ok(self) -> bool:
        return self._is_ok

    def is_ok_and(self, predicate: Callable[[T], bool]) -> bool:
        if self._is_ok and self._value is not None:
            return predicate(self._value)
        return False

    def is_err(self) -> bool:
        return not self._is_ok

    def is_err_and(self, predicate: Callable[[E], bool]) -> bool:
        if not self._is_ok and self._error is not None:
            return predicate(self._error)
        return False

    def expect(self, message: str) -> T:
        if self._is_ok and self._value is not None:
            return self._value
        raise UnwrapFailedException(message)

    def expect_err(self, message: str) -> E:
        if not self._is_ok and self._error is not None:
            return self._error
        raise UnwrapFailedException(message)

    def map[U](self, op: Callable[[T], U]) -> "Result[U, E]":
        if self._is_ok and self._value is not None:
            return Result.Ok(op(self._value))
        return cast(Result[U, E], self)

    def map_err[F](self, op: Callable[[E], F]) -> "Result[T, F]":
        if not self._is_ok and self._error is not None:
            return Result.Err(op(self._error))
        return cast(Result[T, F], self)

    def and_then[U](self, op: Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
        if self._is_ok and self._value is not None:
            return op(self._value)
        return cast(Result[U, E], self)

    def map_or[U](self, default: U, op: Callable[[T], U]) -> U:
        if self._is_ok and self._value is not None:
            return op(self._value)
        return default

    def map_or_else[U](self, default: Callable[[], U], op: Callable[[T], U]) -> U:
        if self._is_ok and self._value is not None:
            return op(self._value)
        return default()

    def or_[U](self, default: U) -> T | U:
        return self._value or default

    def or_else[F](self, op: Callable[[E], "Result[T, F]"]) -> "Result[T, F]":
        if not self._is_ok and self._error is not None:
            return op(self._error)
        return cast(Result[T, F], self)

    def ok(self) -> T | None:
        return self._value

    def err(self) -> E | None:
        return self._error


def Ok[T, E](value: T) -> Result[T, E]:
    return Result.Ok(value)


def Err[T, E](error: E) -> Result[T, E]:
    return Result.Err(error)
