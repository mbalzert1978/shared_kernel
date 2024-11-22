from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from shared_kernel.design_by_contract import ArgumentNullException
from shared_kernel.result_type.UnwrapFailedException import UnwrapFailedException

T = TypeVar("T", bound=object)
E = TypeVar("E")
U = TypeVar("U", bound=object)
F = TypeVar("F")


@dataclass
class Result(Generic[T, E]):
    __match_args__ = ("_is_ok", "_value", "_error")
    __slots__ = ("_is_ok", "_value", "_error")
    __INVALID_STATE_ERROR__ = "BUG: Invalid state encountered. {}"

    _is_ok: bool
    _value: T | None
    _error: E | None

    @classmethod
    def Ok(cls, value: T) -> "Result[T, E]":
        ArgumentNullException.throw_if_null(value, "Ok.value")
        return cls(True, value, None)

    @classmethod
    def Err(cls, error: E) -> "Result[T, E]":
        ArgumentNullException.throw_if_null(error, "Err.error")
        return cls(False, None, error)

    def is_ok(self) -> bool:
        return self._is_ok

    def is_ok_and(self, predicate: Callable[[T], bool]) -> bool:
        match self:
            case Result(True, value, _):
                assert value
                return predicate(value)
            case _:
                return False

    def is_err(self) -> bool:
        return not self._is_ok

    def is_err_and(self, predicate: Callable[[E], bool]) -> bool:
        match self:
            case Result(False, _, error):
                assert error
                return predicate(error)
            case _:
                return False

    def expect(self, message: str) -> T:
        match self:
            case Result(True, value, _):
                assert value
                return value
            case _:
                raise UnwrapFailedException(message)

    def expect_err(self, message: str) -> E:
        match self:
            case Result(False, _, error):
                assert error
                return error
            case _:
                raise UnwrapFailedException(message)

    def map(self, op: Callable[[T], U]) -> "Result[U, E]":
        match self:
            case Result(True, value, _):
                assert value
                return Result.Ok(op(value))
            case Result(False, _, error):
                assert error
                return Result.Err(error)

    def map_err(self, op: Callable[[E], F]) -> "Result[T, F]":
        match self:
            case Result(True, value, _):
                assert value
                return Result.Ok(value)
            case Result(False, _, error):
                assert error
                return Result.Err(op(error))

    def and_then(self, op: Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
        match self:
            case Result(True, value, _):
                assert value
                return op(value)
            case Result(False, _, error):
                assert error
                return Result.Err(error)

    def map_or(self, default: U, op: Callable[[T], U]) -> U:
        match self:
            case Result(True, value, _):
                assert value
                return op(value)
            case _:
                return default

    def map_or_else(self, default: Callable[[], U], op: Callable[[T], U]) -> U:
        match self:
            case Result(True, value, _):
                assert value
                return op(value)
            case _:
                return default()

    def or_(self, default: U) -> T | U:
        match self:
            case Result(True, value, _):
                assert value
                return value
            case _:
                return default

    def or_else(self, op: Callable[[E], "Result[T, F]"]) -> "Result[T, F]":
        match self:
            case Result(True, value, _):
                assert value
                return Result.Ok(value)
            case Result(False, _, error):
                assert error
                return op(error)

    def ok(self) -> T | None:
        return self._value

    def err(self) -> E | None:
        return self._error


def Ok(value: T) -> Result[T, E]:
    return Result.Ok(value)


def Err(error: E) -> Result[T, E]:
    return Result.Err(error)
