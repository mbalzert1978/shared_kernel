from dataclasses import dataclass
from typing import Callable

from shared_kernel.design_by_contract import ArgumentException
from shared_kernel.result_type.UnwrapFailedException import UnwrapFailedException


@dataclass
class Result[T: object, E]:
    __match_args__ = ("_is_ok", "_value", "_error")
    __slots__ = ("_is_ok", "_value", "_error")
    __INVALID_STATE_ERROR__ = "BUG: Invalid state encountered. {}"

    _is_ok: bool
    _value: T | None
    _error: E | None

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
        match self:
            case Result(True, value, _):
                assert value is not None
                return predicate(value)
            case _:
                return False

    def is_err(self) -> bool:
        return not self._is_ok

    def is_err_and(self, predicate: Callable[[E], bool]) -> bool:
        match self:
            case Result(False, _, error):
                assert error is not None
                return predicate(error)
            case _:
                return False

    def expect(self, message: str) -> T:
        match self:
            case Result(True, value, _):
                assert value is not None
                return value
            case _:
                raise UnwrapFailedException(message)

    def expect_err(self, message: str) -> E:
        match self:
            case Result(False, _, error):
                assert error is not None
                return error
            case _:
                raise UnwrapFailedException(message)

    def map[U](self, op: Callable[[T], U]) -> "Result[U, E]":
        match self:
            case Result(True, value, _):
                assert value is not None
                return Result.Ok(op(value))
            case Result(False, _, error):
                assert error is not None
                return Result.Err(error)
        raise AssertionError(Result.__INVALID_STATE_ERROR__.format("map"))

    def map_err[F](self, op: Callable[[E], F]) -> "Result[T, F]":
        match self:
            case Result(True, value, _):
                assert value is not None
                return Result.Ok(value)
            case Result(False, _, error):
                assert error is not None
                return Result.Err(op(error))
        raise AssertionError(Result.__INVALID_STATE_ERROR__.format("map_err"))

    def and_then[U](self, op: Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
        match self:
            case Result(True, value, _):
                assert value is not None
                return op(value)
            case Result(False, _, error):
                assert error is not None
                return Result.Err(error)
        raise AssertionError(Result.__INVALID_STATE_ERROR__.format("and_then"))

    def map_or[U](self, default: U, op: Callable[[T], U]) -> U:
        match self:
            case Result(True, value, _):
                assert value is not None
                return op(value)
            case _:
                return default

    def map_or_else[U](self, default: Callable[[], U], op: Callable[[T], U]) -> U:
        match self:
            case Result(True, value, _):
                assert value is not None
                return op(value)
            case _:
                return default()

    def or_[U](self, default: U) -> T | U:
        match self:
            case Result(True, value, _):
                assert value is not None
                return value
            case _:
                return default

    def or_else[F](self, op: Callable[[E], "Result[T, F]"]) -> "Result[T, F]":
        match self:
            case Result(True, value, _):
                assert value is not None
                return Result.Ok(value)
            case Result(False, _, error):
                assert error is not None
                return op(error)
        raise AssertionError(Result.__INVALID_STATE_ERROR__.format("map_or_else"))

    def ok(self) -> T | None:
        return self._value

    def err(self) -> E | None:
        return self._error


def Ok[T, E](value: T) -> Result[T, E]:
    return Result.Ok(value)


def Err[T, E](error: E) -> Result[T, E]:
    return Result.Err(error)
