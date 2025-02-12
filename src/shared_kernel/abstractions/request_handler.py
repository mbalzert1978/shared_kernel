from typing import Protocol
from .request import Request


class RequestHandler[TRequest: Request[TResponse], TResponse](Protocol):
    async def handle(self, request: TRequest) -> TResponse:...