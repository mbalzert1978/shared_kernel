from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class Request[TResponse:object](Protocol):
    pass