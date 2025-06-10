"""Result type implementation using discriminated unions and PEP 695 type hints."""

from __future__ import annotations

from typing import Any, Callable, Iterator

from shared_kernel.result_type import Err, Ok, Result

from .exceptions import UnwrapFailedException


def is_ok[T, E](result: Result[T, E]) -> bool:
    """Return True if the result is Ok."""
    return isinstance(result, Ok)


def is_err[T, E](result: Result[T, E]) -> bool:
    """Return True if the result is Err."""
    return isinstance(result, Err)


def is_ok_and[T, E](result: Result[T, E], f: Callable[[T], bool]) -> bool:
    """Return True if the result is Ok and the value inside matches a predicate."""
    match result:
        case Ok(value):
            return f(value)
        case _:
            return False


def is_err_and[T, E](result: Result[T, E], f: Callable[[E], bool]) -> bool:
    """Return True if the result is Err and the value inside matches a predicate."""
    match result:
        case Err(error):
            return f(error)
        case _:
            return False


def ok[T, E](result: Result[T, E]) -> T | None:
    """Convert from Result[T, E] to Optional[T]."""
    match result:
        case Ok(value):
            return value
        case _:
            return None


def err[T, E](result: Result[T, E]) -> E | None:
    """Convert from Result[T, E] to Optional[E]."""
    match result:
        case Err(error):
            return error
        case _:
            return None


def map[T, E, U](result: Result[T, E], op: Callable[[T], U]) -> Result[U, E]:
    """Apply a function to the contained Ok value."""
    match result:
        case Ok(value):
            return Ok[U](op(value))
        case Err(error):
            return Err[E](error)


def map_or[T, E, U](result: Result[T, E], default: U, f: Callable[[T], U]) -> U:
    """Return the provided default (if Err) or apply a function to the contained value."""
    match result:
        case Ok(value):
            return f(value)
        case _:
            return default


def map_or_else[T, E, U](result: Result[T, E], default: Callable[[E], U], f: Callable[[T], U]) -> U:
    """Return the result of default() (if Err) or apply f to the contained value."""
    match result:
        case Ok(value):
            return f(value)
        case Err(error):
            return default(error)


def map_err[T, E, F](result: Result[T, E], op: Callable[[E], F]) -> Result[T, F]:
    """Apply a function to the contained Err value."""
    match result:
        case Ok(value):
            return Ok[T](value)
        case Err(error):
            return Err[F](op(error))


def inspect[T, E](result: Result[T, E], f: Callable[[T], Any]) -> Result[T, E]:
    """Call a function with a reference to the contained value if Ok."""
    match result:
        case Ok(value):
            f(value)
    return result


def inspect_err[T, E](result: Result[T, E], f: Callable[[E], Any]) -> Result[T, E]:
    """Call a function with a reference to the contained value if Err."""
    match result:
        case Err(error):
            f(error)
    return result


def expect[T, E](result: Result[T, E], msg: str) -> T:
    """Unwrap a result, yielding the content of an Ok, or raise UnwrapFailedException."""
    match result:
        case Ok(value):
            return value
        case Err(error):
            raise UnwrapFailedException(f"{msg}: {error}")


def unwrap[T, E](result: Result[T, E]) -> T:
    """Return the Ok value, or raise UnwrapFailedException."""
    return expect(result, "called `Result.unwrap()` on an `Err` value")


def expect_err[T, E](result: Result[T, E], msg: str) -> E:
    """Return the Err value, or raise UnwrapFailedException with a custom message."""
    match result:
        case Err(error):
            return error
        case Ok(value):
            raise UnwrapFailedException(f"{msg}: {value}")


def unwrap_err[T, E](result: Result[T, E]) -> E:
    """Return the Err value, or raise UnwrapFailedException."""
    return expect_err(result, "called `Result.unwrap_err()` on an `Ok` value")


def unwrap_or[T, E](result: Result[T, E], default: T) -> T:
    """Return the contained Ok value or the provided default."""
    match result:
        case Ok(value):
            return value
        case _:
            return default


def unwrap_or_else[T, E](result: Result[T, E], op: Callable[[E], T]) -> T:
    """Return the contained Ok value or compute it from a closure."""
    match result:
        case Ok(value):
            return value
        case Err(error):
            return op(error)


def and_[T, E, U](result: Result[T, E], res: Result[U, E]) -> Result[U, E]:
    """Return res if result is Ok, otherwise return result's Err value."""
    match result:
        case Ok(_):
            return res
        case Err(error):
            return Err[E](error)


def and_then[T, E, U](result: Result[T, E], op: Callable[[T], Result[U, E]]) -> Result[U, E]:
    """Call op if Ok, otherwise return result's Err value."""
    match result:
        case Ok(value):
            return op(value)
        case Err(error):
            return Err[E](error)


def or_[T, E, F](result: Result[T, E], res: Result[T, F]) -> Result[T, F]:
    """Return result if Ok, otherwise return res."""
    match result:
        case Ok(value):
            return Ok[T, F](value)
        case _:
            return res


def or_else[T, E, F](result: Result[T, E], op: Callable[[E], Result[T, F]]) -> Result[T, F]:
    """Return result if Ok, otherwise call op."""
    match result:
        case Ok(value):
            return Ok[T](value)
        case Err(error):
            return op(error)


def iter[T, E](result: Result[T, E]) -> Iterator[T]:
    """Return an iterator over the possibly contained value."""
    match result:
        case Ok(value):
            yield value
        case _:
            return


def from_iter[A, E, V](iter_: Iterator[Result[A, E]]) -> Result[V, E]:
    """Convert an iterator of Results into a Result of a container."""
    values = []
    for item in iter_:
        match item:
            case Ok(value):
                values.append(value)
            case Err(error):
                return Err[E](error)
    return Ok[V](values)  # type: ignore
