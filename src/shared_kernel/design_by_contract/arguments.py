from typing import Any, NoReturn, Optional


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
    def raise_if_none_or_empty(arg: Optional[str], param: str | None = None) -> None:
        if arg is None or len(arg) == 0:
            ArgumentNullException.raise_if_none(arg, param)

    @staticmethod
    def raise_if_none_or_whitespace(
        arg: Optional[str], param: str | None = None
    ) -> None:
        match arg:
            case None:
                ArgumentNullException.raise_if_none(arg, param)
            case str() if arg.isspace():
                raise ArgumentException("String argument cannot be whitespace.", param)

    @staticmethod
    def throw_if_null_or_empty(
        argument: Optional[str], param_name: Optional[str] = None
    ) -> None:
        if argument is None or len(argument) == 0:
            ArgumentException.raise_if_none_or_empty(argument, param_name)

    @staticmethod
    def throw_if_null_or_whitespace(
        argument: Optional[str], param_name: Optional[str] = None
    ) -> None:
        ArgumentException.raise_if_none_or_whitespace(argument, param_name)


class ArgumentNullException(ArgumentException):
    def __init__(self, param_name: Optional[str] = None, message: Optional[str] = None):
        super().__init__(message or "Value cannot be null.", param_name)

    @staticmethod
    def raise_if_none(arg: Any, param: str | None = None) -> None:
        if arg is None:
            ArgumentNullException.throw(param or "")

    @staticmethod
    def throw(param: str) -> NoReturn:
        raise ArgumentNullException(param)

    @staticmethod
    def throw_if_null(argument: Any, param_name: Optional[str] = None) -> None:
        if argument is None:
            raise ArgumentNullException(param_name)
