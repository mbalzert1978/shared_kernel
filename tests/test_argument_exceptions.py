import pytest

from shared_kernel.design_by_contract.arguments import ArgumentException


def test_argument_exception_when_initialized_with_message_and_param_should_set_both() -> (
    None
):
    exc = ArgumentException("Test message", "test_param")
    assert str(exc) == "Test message"
    assert exc.param_name == "test_param"


def test_argument_exception_when_initialized_without_param_name_should_set_only_message() -> (
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


def test_argument_exception_message_when_param_name_not_set_should_not_include_param_name() -> (
    None
):
    exc = ArgumentException("Test message")
    assert exc.message == "Test message"


def test_argument_exception_raise_if_none_when_none_should_raise_exception() -> None:
    with pytest.raises(ArgumentException, match="Value cannot be null."):
        ArgumentException.raise_if_none(None, "test_param")


def test_argument_exception_raise_if_none_when_not_none_should_not_raise() -> None:
    assert ArgumentException.raise_if_none("valid", "test_param") is None


def test_argument_exception_raise_if_none_or_empty_when_none_should_raise_exception() -> (
    None
):
    with pytest.raises(ArgumentException, match="Value cannot be null."):
        ArgumentException.raise_if_none_or_empty(None, "test_param")


def test_argument_exception_raise_if_none_or_empty_when_empty_should_raise_exception() -> (
    None
):
    with pytest.raises(ArgumentException, match="String argument cannot be empty."):
        ArgumentException.raise_if_none_or_empty("", "test_param")


def test_argument_exception_raise_if_none_or_empty_when_valid_should_not_raise() -> (
    None
):
    assert ArgumentException.raise_if_none_or_empty("valid", "test_param") is None


def test_argument_exception_raise_if_none_or_whitespace_when_none_should_raise_exception() -> (
    None
):
    with pytest.raises(ArgumentException, match="Value cannot be null."):
        ArgumentException.raise_if_none_or_whitespace(None, "test_param")


def test_argument_exception_raise_if_none_or_whitespace_when_whitespace_should_raise_exception() -> (
    None
):
    with pytest.raises(
        ArgumentException, match="String argument cannot be whitespace."
    ):
        ArgumentException.raise_if_none_or_whitespace("   ", "test_param")


def test_argument_exception_raise_if_none_or_whitespace_when_valid_should_not_raise() -> (
    None
):
    assert ArgumentException.raise_if_none_or_whitespace("valid", "test_param") is None
