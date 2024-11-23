from collections.abc import Sized


class ArgumentException(Exception):
    DEFAULT_MESSAGE = "Value does not fall within the expected range."
    NONE_ARGUMENT_MESSAGE = "Argument cannot be none."
    EMPTY_ARGUMENT_MESSAGE = "Argument cannot be empty."
    WHITESPACE_ARGUMENT_MESSAGE = "String argument cannot be whitespace."
    PARAMETER_MESSAGE_FORMAT = "{} (Parameter '{}')"

    def __init__(
        self,
        message: str | None = None,
        param_name: str | None = None,
        inner_exception: Exception | None = None,
    ):
        self.param_name = param_name
        self.inner_exception = inner_exception
        super().__init__(message or self.DEFAULT_MESSAGE)

    @property
    def message(self) -> str:
        base_message = super().args[0]
        if self.param_name:
            return self.PARAMETER_MESSAGE_FORMAT.format(base_message, self.param_name)
        return base_message

    @classmethod
    def raise_if_none(cls, arg: object | None, param: str | None = None) -> None:
        if arg is None:
            raise cls(cls.NONE_ARGUMENT_MESSAGE, param)

    @classmethod
    def raise_if_none_or_empty(
        cls, arg: Sized | None, param: str | None = None
    ) -> None:
        match arg:
            case None:
                cls.raise_if_none(arg, param)
            case Sized() as sized if len(sized) == 0:
                raise cls(cls.EMPTY_ARGUMENT_MESSAGE, param)

    @classmethod
    def raise_if_none_or_whitespace(
        cls, arg: str | None, param: str | None = None
    ) -> None:
        match arg:
            case None:
                cls.raise_if_none(arg, param)
            case str() as string if string.isspace():
                raise cls(cls.WHITESPACE_ARGUMENT_MESSAGE, param)
