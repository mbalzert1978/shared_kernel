from http import HTTPStatus

import pytest

from shared_kernel import ArgumentException, Error


def test_error_str_when_code_and_description_provided_then_returns_formatted_string():
    error = Error("404", "Not Found")
    assert str(error) == "404:Not Found"


def test_error_repr_when_called_then_returns_formatted_string():
    error = Error("500", "Internal Server Error")
    assert repr(error) == "Error(code: 500, description:Internal Server Error)"


def test_error_eq_when_same_code_then_returns_true():
    error1 = Error("400", "Bad Request")
    error2 = Error("400", "Different Description")
    assert error1 == error2


def test_error_eq_when_different_code_then_returns_false():
    error1 = Error("400", "Bad Request")
    error2 = Error("404", "Not Found")
    assert error1 != error2


def test_error_hash_when_same_code_and_description_then_returns_same_hash():
    error1 = Error("403", "Forbidden")
    error2 = Error("403", "Forbidden")
    assert hash(error1) == hash(error2)


def test_error_default_when_called_then_returns_error_with_empty_strings():
    error = Error.default()
    assert error.code == "" and error.description == ""


def test_error_from_when_string_with_separator_then_splits_correctly():
    error = Error.from_("404:Not Found")
    assert error.code == "404" and error.description == "Not Found"


def test_error_from_when_string_without_separator_then_sets_description_to_empty_str():
    error = Error.from_("500")
    assert error.code == "500" and error.description == ""


def test_error_from_when_http_status_then_creates_error_from_status():
    error = Error.from_(HTTPStatus.NOT_FOUND)
    assert error.code == "404" and error.description == "Not Found"


def test_error_from_when_invalid_type_then_raises_value_error():
    with pytest.raises(ArgumentException, match="Invalid source type"):
        Error.from_(123)


def test_error_idempotence_when_converted_to_string_and_back():
    original_error = Error("418", "I'm a teapot")
    error_string = str(original_error)
    reconstructed_error = Error.from_(error_string)
    assert original_error == reconstructed_error
    assert original_error.code == reconstructed_error.code
    assert original_error.description == reconstructed_error.description


def test_error_idempotence_when_converted_to_string_and_back_with_empty_description_str():
    original_error = Error("204")
    error_string = str(original_error)
    reconstructed_error = Error.from_(error_string)
    assert original_error == reconstructed_error
    assert original_error.code == reconstructed_error.code
    assert original_error.description == reconstructed_error.description == ""
