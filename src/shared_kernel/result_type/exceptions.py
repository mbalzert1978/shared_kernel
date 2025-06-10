"""Result type exceptions."""


class UnwrapFailedException(Exception):
    """Exception raised when trying to unwrap a Result in the wrong state."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
