import pytest

from shared_kernel import ArgumentException, hash_combine


def test_when_given_one_argument_should_return_expected_hash() -> None:
    assert hash_combine(1) == 2654435770


def test_when_given_multiple_arguments_should_return_expected_hash() -> None:
    assert hash_combine(1, 2, 3) == 11093822460243


def test_when_called_multiple_times_with_same_input_and_should_return_consistent_result() -> (
    None
):
    assert hash_combine(1, 2, 3) == hash_combine(1, 2, 3)


def test_when_argument_order_changed_should_return_different_result() -> None:
    assert hash_combine(1, 2, 3) != hash_combine(3, 2, 1)


def test_when_given_no_arguments_should_raise_argument_exception() -> None:
    with pytest.raises(ArgumentException):
        hash_combine()


def test_hash_combine_when_called_with_arguments_should_create_hash() -> None:
    assert isinstance(hash_combine(1, 2, 3), int)


def test_when_given_different_types_should_create_hash() -> None:
    assert isinstance(hash_combine(1, "hello", 3.14, True), int)


def test_when_given_large_input_should_create_hash() -> None:
    assert isinstance(hash_combine(*list(range(1000))), int)
