from typing import Any, Optional


class ArgumentException(Exception):
    def __init__(
        self,
        message: Optional[str] = None,
        param_name: Optional[str] = None,
        inner_exception: Optional[Exception] = None,
    ):
        self.param_name = param_name
        self.inner_exception = inner_exception
        super().__init__(message or "Value does not fall within the expected range.")

    @property
    def message(self) -> str:
        base_message = super().args[0]
        if self.param_name:
            return f"{base_message} (Parameter '{self.param_name}')"
        return base_message

    @staticmethod
    def raise_if_none(arg: Any, param: str | None = None) -> None:
        if arg is None:
            raise ArgumentException("Value cannot be null.", param)

    @staticmethod
    def raise_if_none_or_empty(arg: Optional[str], param: str | None = None) -> None:
        if arg is None:
            ArgumentException.raise_if_none(arg, param)
        elif len(arg) == 0:
            raise ArgumentException("String argument cannot be empty.", param)

    @staticmethod
    def raise_if_none_or_whitespace(
        arg: Optional[str], param: str | None = None
    ) -> None:
        if arg is None:
            ArgumentException.raise_if_none(arg, param)
        elif arg.isspace():
            raise ArgumentException("String argument cannot be whitespace.", param)
