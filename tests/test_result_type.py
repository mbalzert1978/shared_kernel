from typing import TypeVar

import pytest

from shared_kernel.design_by_contract import ArgumentException
from shared_kernel.result_type import ResultFactory, functions
from shared_kernel.result_type.exceptions import UnwrapFailedException

T = TypeVar("T")
E = TypeVar("E")


def test_ok_when_created_then_is_ok_and_has_value() -> None:
    result = ResultFactory.ok(42)
    assert functions.is_ok(result)
    assert not functions.is_err(result)
    assert functions.unwrap(result) == 42
    assert functions.err(result) is None


def test_err_when_created_then_is_err_and_has_error() -> None:
    result = ResultFactory.err("error")
    assert not functions.is_ok(result)
    assert functions.is_err(result)
    assert functions.ok(result) is None
    assert functions.err(result) == "error"


def test_is_ok_and_when_ok_and_predicate_true_then_returns_true() -> None:
    result = ResultFactory.ok(42)
    assert functions.is_ok_and(result, lambda x: x > 40)


def test_is_ok_and_when_err_then_returns_false() -> None:
    result = ResultFactory.err("error")
    assert not functions.is_ok_and(result, lambda x: x > 3)


def test_is_ok_and_when_ok_and_predicate_false_then_returns_false() -> None:
    result = ResultFactory.ok(42)
    assert not functions.is_ok_and(result, lambda x: x < 40)


def test_is_err_and_when_err_and_predicate_true_then_returns_true() -> None:
    result = ResultFactory.err("error")
    assert functions.is_err_and(result, lambda x: len(x) > 3)


def test_is_err_and_when_err_and_predicate_false_then_returns_false() -> None:
    result = ResultFactory.err("error")
    assert not functions.is_err_and(result, lambda x: len(x) < 3)


def test_is_err_and_when_ok_then_returns_false() -> None:
    result = ResultFactory.ok(42)
    assert not functions.is_err_and(result, lambda x: len(x) > 3)


def test_expect_when_ok_then_returns_value() -> None:
    result = ResultFactory.ok(42)
    assert functions.expect(result, "Should not fail") == 42


def test_expect_when_err_then_raises_unwrap_exception() -> None:
    with pytest.raises(UnwrapFailedException):
        functions.expect(ResultFactory.err("error"), "Should fail")


def test_expect_err_when_err_then_returns_error() -> None:
    result = ResultFactory.err("error")
    assert functions.expect_err(result, "Should not fail") == "error"


def test_expect_err_when_ok_then_raises_unwrap_exception() -> None:
    with pytest.raises(UnwrapFailedException):
        functions.expect_err(ResultFactory.ok(42), "Should fail")


def test_or_when_ok_then_returns_value() -> None:
    result = ResultFactory.ok(42)
    assert functions.unwrap_or(result, 0) == 42


def test_or_when_err_then_returns_default() -> None:
    result = ResultFactory.err("error")
    assert functions.unwrap_or(result, 0) == 0


def test_map_when_ok_then_applies_function() -> None:
    result = ResultFactory.ok(42)
    mapped = functions.map(result, lambda x: x * 2)
    assert functions.ok(mapped) == 84


def test_map_when_err_then_preserves_error() -> None:
    result = ResultFactory.err("error")
    mapped = functions.map(result, lambda x: x * 2)
    assert functions.err(mapped) == "error"


def test_map_err_when_ok_then_preserves_value() -> None:
    result = ResultFactory.ok(42)
    mapped = functions.map_err(result, lambda e: e.upper())
    assert functions.ok(mapped) == 42


def test_map_err_when_err_then_applies_function() -> None:
    result = ResultFactory.err("error")
    mapped = functions.map_err(result, lambda e: e.upper())
    assert functions.err(mapped) == "ERROR"


def test_map_or_when_ok_then_applies_function() -> None:
    result = ResultFactory.ok(42)
    assert functions.map_or(result, 0, lambda x: x * 2) == 84


def test_map_or_when_err_then_returns_default() -> None:
    result = ResultFactory.err("error")
    assert functions.map_or(result, 0, lambda x: x * 2) == 0


def test_map_or_else_when_ok_then_applies_function() -> None:
    result = ResultFactory.ok(42)
    assert functions.map_or_else(result, lambda _: 0, lambda x: x * 2) == 84


def test_or_else_when_ok_then_returns_value() -> None:
    result = ResultFactory.ok(42)
    assert functions.ok(functions.or_else(result, lambda err: ResultFactory.err(len(err)))) == 42


def test_or_else_when_err_then_computes_default() -> None:
    result = ResultFactory.err("error")
    assert functions.err(functions.or_else(result, lambda err: ResultFactory.err(len(err)))) == 5


def test_map_or_else_when_err_then_applies_default_function() -> None:
    result = ResultFactory.err("error")
    assert functions.map_or_else(result, lambda e: 5, lambda x: x * 2) == 5


def test_and_then_when_ok_and_function_returns_ok_then_chains_result() -> None:
    result = ResultFactory.ok(42)
    chained = functions.and_then(
        result, lambda x: ResultFactory.ok(x * 2) if x > 40 else ResultFactory.err("Too small")
    )
    assert functions.ok(chained) == 84


def test_and_then_when_ok_and_function_returns_err_then_returns_err() -> None:
    result = ResultFactory.ok(30)
    chained = functions.and_then(
        result, lambda x: ResultFactory.ok(x * 2) if x > 40 else ResultFactory.err("Too small")
    )
    assert functions.err(chained) == "Too small"


def test_and_then_when_err_then_preserves_error() -> None:
    result = ResultFactory.err("Initial error")
    chained = functions.and_then(result, lambda x: ResultFactory.ok(x * 2))
    assert functions.err(chained) == "Initial error"


def test_ok_raises_attribute_null_error_when_value_is_none():
    with pytest.raises(ArgumentException, match="Argument cannot be none.") as exc:
        ResultFactory.ok(None)

    assert exc.value.message == "Argument cannot be none. (Parameter 'value')"
    assert exc.value.param_name == "value"


def test_err_raises_attribute_none_error_when_error_is_none():
    with pytest.raises(ArgumentException, match="Argument cannot be none.") as exc:
        ResultFactory.err(None)

    assert exc.value.message == "Argument cannot be none. (Parameter 'error')"
    assert exc.value.param_name == "error"


def test_result_equality_when_ok_results_with_same_value_then_returns_true() -> None:
    r1 = ResultFactory.ok(42)
    r2 = ResultFactory.ok(42)
    r3 = ResultFactory.ok("test")
    r4 = ResultFactory.ok("test")
    assert r1 == r2
    assert r3 == r4


def test_result_equality_when_ok_results_with_different_values_then_returns_false() -> None:
    r1 = ResultFactory.ok(42)
    r2 = ResultFactory.ok(43)
    assert r1 != r2


def test_result_equality_when_ok_and_err_results_then_returns_false() -> None:
    r1 = ResultFactory.ok(42)
    r2 = ResultFactory.err("error")
    assert r1 != r2


def test_result_equality_when_err_results_with_same_error_then_returns_true() -> None:
    r1 = ResultFactory.err("error")
    r2 = ResultFactory.err("error")
    r3 = ResultFactory.err(42)
    r4 = ResultFactory.err(42)
    assert r1 == r2
    assert r3 == r4


def test_result_equality_when_err_results_with_different_errors_then_returns_false() -> None:
    r1 = ResultFactory.err("error1")
    r2 = ResultFactory.err("error2")
    assert r1 != r2


def test_result_hash_when_ok_results_with_same_value_then_returns_same_hash() -> None:
    r1 = ResultFactory.ok(42)
    r2 = ResultFactory.ok(42)
    r3 = ResultFactory.ok("test")
    r4 = ResultFactory.ok("test")
    assert hash(r1) == hash(r2)
    assert hash(r3) == hash(r4)


def test_result_hash_when_ok_results_with_different_values_then_returns_different_hash() -> None:
    r1 = ResultFactory.ok(42)
    r2 = ResultFactory.ok(43)
    assert hash(r1) != hash(r2)


def test_result_hash_when_err_results_with_same_error_then_returns_same_hash() -> None:
    r1 = ResultFactory.err("error")
    r2 = ResultFactory.err("error")
    r3 = ResultFactory.err(42)
    r4 = ResultFactory.err(42)
    assert hash(r1) == hash(r2)
    assert hash(r3) == hash(r4)


def test_result_hash_when_err_results_with_different_errors_then_returns_different_hash() -> None:
    r1 = ResultFactory.err("error1")
    r2 = ResultFactory.err("error2")
    assert hash(r1) != hash(r2)


def test_result_repr_when_ok_result_then_returns_expected_string() -> None:
    r1 = ResultFactory.ok(42)
    r2 = ResultFactory.ok("test")
    assert repr(r1) == "Ok(value=42)"
    assert repr(r2) == "Ok(value='test')"


def test_result_repr_when_err_result_then_returns_expected_string() -> None:
    r1 = ResultFactory.err("error")
    r2 = ResultFactory.err(42)
    assert repr(r1) == "Err(error='error')"
    assert repr(r2) == "Err(error=42)"


def test_result_str_when_ok_result_then_returns_expected_string() -> None:
    r1 = ResultFactory.ok(42)
    r2 = ResultFactory.ok("test")
    assert str(r1) == "Ok(42)"
    assert str(r2) == "Ok(test)"


def test_result_str_when_err_result_then_returns_expected_string() -> None:
    r1 = ResultFactory.err("error")
    r2 = ResultFactory.err(42)
    assert str(r1) == "Err(error)"
    assert str(r2) == "Err(42)"


def test_result_hash_and_equality_when_equal_results_then_have_same_hash() -> None:
    r1 = ResultFactory.ok(42)
    r2 = ResultFactory.ok(42)
    r3 = ResultFactory.err("error")
    r4 = ResultFactory.err("error")

    assert r1 == r2 and hash(r1) == hash(r2)
    assert r3 == r4 and hash(r3) == hash(r4)
    assert r1 != r3 and hash(r1) != hash(r3)


def test_result_with_complex_objects_when_comparing_and_hashing_then_behaves_correctly() -> None:
    class ComplexObject:
        def __init__(self, value):
            self.value = value

        def __eq__(self, other):
            return isinstance(other, ComplexObject) and self.value == other.value

        def __hash__(self):
            return hash(self.value)

    obj1 = ComplexObject(42)
    obj2 = ComplexObject(42)
    obj3 = ComplexObject(43)

    r1 = ResultFactory.ok(obj1)
    r2 = ResultFactory.ok(obj2)
    r3 = ResultFactory.ok(obj3)

    assert r1 == r2
    assert r1 != r3
    assert hash(r1) == hash(r2)
    assert hash(r1) != hash(r3)


def test_result_repr_and_str_with_complex_objects_when_converted_then_uses_object_repr() -> None:
    class ComplexObject:
        def __repr__(self):
            return "ComplexObject()"

    obj = ComplexObject()
    r1 = ResultFactory.ok(obj)
    r2 = ResultFactory.err(obj)

    assert repr(r1) == "Ok(value=ComplexObject())"
    assert str(r1) == "Ok(ComplexObject())"
    assert repr(r2) == "Err(error=ComplexObject())"
    assert str(r2) == "Err(ComplexObject())"
