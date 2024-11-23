import pytest

from shared_kernel import ArgumentException, hash_combine


def test_when_given_seed_and_one_argument_should_return_expected_hash():
    assert hash_combine(1) == 2654435770


def test_when_given_seed_and_multiple_arguments_should_return_expected_hash():
    assert hash_combine(1, 2, 3) == 11093822460243


def test_when_called_multiple_times_with_same_input_and_seed_should_return_consistent_result():
    assert hash_combine(1, 2, 3) == hash_combine(1, 2, 3)


def test_when_argument_order_changed_should_return_different_result():
    assert hash_combine(1, 2, 3) != hash_combine(3, 2, 1)


def test_when_no_seed_provided_should_return_integer_result():
    assert isinstance(hash_combine(1, 2, 3), int)


def test_when_given_different_types_should_return_integer_result():
    assert isinstance(hash_combine(1, "hello", 3.14, True), int)


def test_when_given_no_arguments_should_raise_argument_exception():
    with pytest.raises(ArgumentException):
        hash_combine()


def test_when_given_large_input_should_return_integer_result():
    assert isinstance(hash_combine(*list(range(1000))), int)
