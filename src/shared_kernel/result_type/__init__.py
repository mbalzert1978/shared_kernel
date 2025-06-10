"""Result type for error handling."""

from .exceptions import UnwrapFailedException
from .result import Err, Ok, Result, ResultFactory

__all__ = ["Result", "ResultFactory", "UnwrapFailedException"]
