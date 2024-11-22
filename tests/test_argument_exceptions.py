import pytest

from shared_kernel.design_by_contract.arguments import (
    ArgumentException,
    ArgumentNullException,
)


def test_argument_exception_when_initialized_should_set_message_and_param_name() -> (
    None
):
    exc = ArgumentException("Test message", "test_param")
    assert str(exc) == "Test message"
    assert exc.param_name == "test_param"


def test_argument_exception_message_when_no_param_name_set_should_not_include_param_name() -> (
    None
):
    exc = ArgumentException("Test message")
    assert str(exc) == "Test message"
    assert exc.param_name is None


def test_argument_exception_message_when_param_name_set_should_include_param_name() -> (
    None
):
    exc = ArgumentException("Test message", "test_param")
    assert exc.message == "Test message (Parameter 'test_param')"


def test_argument_exception_message_when_param_name_is_not_set_should_not_include_param_name() -> (
    None
):
    exc = ArgumentException("Test message")
    assert exc.message == "Test message"


def test_argument_exception_raise_if_none_or_empty_when_none_should_raise_argument_null_exception() -> (
    None
):
    with pytest.raises(ArgumentNullException):
        ArgumentException.raise_if_none_or_empty(None, "test_param")


def test_argument_exception_raise_if_none_or_empty_when_empty_should_raise_argument_exception() -> (
    None
):
    with pytest.raises(ArgumentException, match="String argument cannot be empty."):
        ArgumentException.raise_if_none_or_empty("", "test_param")


def test_argument_exception_raise_if_none_or_empty_when_valid_should_not_raise() -> (
    None
):
    ArgumentException.raise_if_none_or_empty("valid", "test_param")


def test_argument_exception_raise_if_none_or_whitespace_when_none_should_raise_argument_null_exception() -> (
    None
):
    with pytest.raises(ArgumentNullException):
        ArgumentException.raise_if_none_or_whitespace(None, "test_param")


def test_argument_exception_raise_if_none_or_whitespace_when_whitespace_should_raise_argument_exception() -> (
    None
):
    with pytest.raises(
        ArgumentException, match="String argument cannot be whitespace."
    ):
        ArgumentException.raise_if_none_or_whitespace("   ", "test_param")


def test_argument_exception_raise_if_none_or_whitespace_when_valid_should_not_raise() -> (
    None
):
    ArgumentException.raise_if_none_or_whitespace("valid", "test_param")


def test_argument_exception_throw_if_null_or_empty_when_none_should_raise_argument_null_exception() -> (
    None
):
    with pytest.raises(ArgumentNullException):
        ArgumentException.throw_if_null_or_empty(None, "test_param")


def test_argument_exception_throw_if_null_or_empty_when_empty_should_raise_argument_exception() -> (
    None
):
    with pytest.raises(ArgumentException, match="String argument cannot be empty."):
        ArgumentException.throw_if_null_or_empty("", "test_param")


def test_argument_exception_throw_if_null_or_empty_when_valid_should_not_raise() -> (
    None
):
    ArgumentException.throw_if_null_or_empty("valid", "test_param")


def test_argument_exception_throw_if_null_or_whitespace_when_none_should_raise_argument_null_exception() -> (
    None
):
    with pytest.raises(ArgumentNullException):
        ArgumentException.throw_if_null_or_whitespace(None, "test_param")


def test_argument_exception_throw_if_null_or_whitespace_when_whitespace_should_raise_argument_exception() -> (
    None
):
    with pytest.raises(
        ArgumentException, match="String argument cannot be whitespace."
    ):
        ArgumentException.throw_if_null_or_whitespace("   ", "test_param")


def test_argument_exception_throw_if_null_or_whitespace_when_valid_should_not_raise() -> (
    None
):
    ArgumentException.throw_if_null_or_whitespace("valid", "test_param")


def test_argument_null_exception_when_initialized_should_set_message_and_param_name() -> (
    None
):
    exc = ArgumentNullException("test_param")
    assert str(exc) == "Value cannot be null."
    assert exc.param_name == "test_param"


def test_argument_null_exception_raise_if_none_when_none_should_raise_argument_null_exception() -> (
    None
):
    with pytest.raises(ArgumentNullException):
        ArgumentNullException.raise_if_none(None, "test_param")


def test_argument_null_exception_raise_if_none_when_valid_should_not_raise() -> None:
    ArgumentNullException.raise_if_none("valid", "test_param")


def test_argument_null_exception_throw_should_raise_argument_null_exception() -> None:
    with pytest.raises(ArgumentNullException):
        ArgumentNullException.throw("test_param")


def test_argument_null_exception_throw_if_null_when_none_should_raise_argument_null_exception() -> (
    None
):
    with pytest.raises(ArgumentNullException):
        ArgumentNullException.throw_if_null(None, "test_param")


def test_argument_null_exception_throw_if_null_when_valid_should_not_raise() -> None:
    ArgumentNullException.throw_if_null("valid", "test_param")
