import pytest

from shared_kernel import ArgumentException, Err, Ok, Result, UnwrapFailedException


def test_ok_when_created_then_is_ok_and_has_value() -> None:
    result: Result[int, str] = Ok(42)
    assert result.is_ok()
    assert not result.is_err()
    assert result.ok() == 42
    assert result.err() is None


def test_err_when_created_then_is_err_and_has_error() -> None:
    result: Result[int, str] = Err("error")
    assert not result.is_ok()
    assert result.is_err()
    assert result.ok() is None
    assert result.err() == "error"


def test_is_ok_and_when_ok_and_predicate_true_then_returns_true() -> None:
    result: Result[int, str] = Ok(42)
    assert result.is_ok_and(lambda x: x > 40)


def test_is_ok_and_when_err_then_returns_false() -> None:
    result: Result[int, str] = Err("error")
    assert not result.is_ok_and(lambda x: x > 3)


def test_is_ok_and_when_ok_and_predicate_false_then_returns_false() -> None:
    result: Result[int, str] = Ok(42)
    assert not result.is_ok_and(lambda x: x < 40)


def test_is_err_and_when_err_and_predicate_true_then_returns_true() -> None:
    result: Result[int, str] = Err("error")
    assert result.is_err_and(lambda x: len(x) > 3)


def test_is_err_and_when_err_and_predicate_false_then_returns_false() -> None:
    result: Result[int, str] = Err("error")
    assert not result.is_err_and(lambda x: len(x) < 3)


def test_is_err_and_when_ok_then_returns_false() -> None:
    result: Result[int, str] = Ok(42)
    assert not result.is_err_and(lambda x: len(x) > 3)


def test_expect_when_ok_then_returns_value() -> None:
    result: Result[int, str] = Ok(42)
    assert result.expect("Should not fail") == 42


def test_expect_when_err_then_raises_unwrap_exception() -> None:
    with pytest.raises(UnwrapFailedException):
        Err("error").expect("Should fail")


def test_expect_err_when_err_then_returns_error() -> None:
    result: Result[int, str] = Err("error")
    assert result.expect_err("Should not fail") == "error"


def test_expect_err_when_ok_then_raises_unwrap_exception() -> None:
    with pytest.raises(UnwrapFailedException):
        Ok(42).expect_err("Should fail")


def test_or_when_ok_then_returns_value() -> None:
    assert Ok(42).or_(0) == 42


def test_or_when_err_then_returns_default() -> None:
    assert Err("error").or_(0) == 0


def test_map_when_ok_then_applies_function() -> None:
    result: Result[int, str] = Ok(42)
    mapped = result.map(lambda x: x * 2)
    assert mapped.ok() == 84


def test_map_when_err_then_preserves_error() -> None:
    result: Result[int, str] = Err("error")
    mapped = result.map(lambda x: x * 2)
    assert mapped.err() == "error"


def test_map_err_when_ok_then_preserves_value() -> None:
    result: Result[int, str] = Ok(42)
    mapped = result.map_err(lambda e: e.upper())
    assert mapped.ok() == 42


def test_map_err_when_err_then_applies_function() -> None:
    result: Result[int, str] = Err("error")
    mapped = result.map_err(lambda e: e.upper())
    assert mapped.err() == "ERROR"


def test_map_or_when_ok_then_applies_function() -> None:
    assert Ok(42).map_or(0, lambda x: x * 2) == 84


def test_map_or_when_err_then_returns_default() -> None:
    assert Err("error").map_or(0, lambda x: x * 2) == 0


def test_map_or_else_when_ok_then_applies_function() -> None:
    assert Ok(42).map_or_else(lambda: 0, lambda x: x * 2) == 84


def test_or_else_when_ok_then_returns_value() -> None:
    assert Ok(42).or_else(lambda err: Err(len(err))) == Ok(42)


def test_or_else_when_err_then_computes_default() -> None:
    assert Err("error").or_else(lambda err: Err(len(err))) == Err(5)


def test_map_or_else_when_err_then_applies_default_function() -> None:
    assert Err("error").map_or_else(lambda: 5, lambda x: x * 2) == 5


def test_and_then_when_ok_and_function_returns_ok_then_chains_result() -> None:
    result: Result[int, str] = Ok(42)
    chained = result.and_then(lambda x: Ok(x * 2) if x > 40 else Err("Too small"))
    assert chained.ok() == 84


def test_and_then_when_ok_and_function_returns_err_then_returns_err() -> None:
    result: Result[int, str] = Ok(30)
    chained = result.and_then(lambda x: Ok(x * 2) if x > 40 else Err("Too small"))
    assert chained.err() == "Too small"


def test_and_then_when_err_then_preserves_error() -> None:
    result: Result[int, str] = Err("Initial error")
    chained = result.and_then(lambda x: Ok(x * 2))
    assert chained.err() == "Initial error"


def test_ok_raises_attribute_null_error_when_value_is_none():
    with pytest.raises(ArgumentException, match="Argument cannot be none.") as exc:
        Ok(None)

    assert exc.value.message == "Argument cannot be none. (Parameter 'Ok.value')"
    assert exc.value.param_name == "Ok.value"


def test_err_raises_attribute_none_error_when_error_is_none():
    with pytest.raises(ArgumentException, match="Argument cannot be none.") as exc:
        Err(None)

    assert exc.value.message == "Argument cannot be none. (Parameter 'Err.error')"
    assert exc.value.param_name == "Err.error"


def test_result_equality_when_ok_results_with_same_value_then_returns_true() -> None:
    assert Ok(42) == Ok(42)
    assert Ok("test") == Ok("test")


def test_result_equality_when_ok_results_with_different_values_then_returns_false() -> (
    None
):
    assert Ok(42) != Ok(43)


def test_result_equality_when_ok_and_err_results_then_returns_false() -> None:
    assert Ok(42) != Err("error")


def test_result_equality_when_err_results_with_same_error_then_returns_true() -> None:
    assert Err("error") == Err("error")
    assert Err(42) == Err(42)


def test_result_equality_when_err_results_with_different_errors_then_returns_false() -> (
    None
):
    assert Err("error1") != Err("error2")


def test_result_hash_when_ok_results_with_same_value_then_returns_same_hash() -> None:
    assert hash(Ok(42)) == hash(Ok(42))
    assert hash(Ok("test")) == hash(Ok("test"))


def test_result_hash_when_ok_results_with_different_values_then_returns_different_hash() -> (
    None
):
    assert hash(Ok(42)) != hash(Ok(43))


def test_result_hash_when_err_results_with_same_error_then_returns_same_hash() -> None:
    assert hash(Err("error")) == hash(Err("error"))
    assert hash(Err(42)) == hash(Err(42))


def test_result_hash_when_err_results_with_different_errors_then_returns_different_hash() -> (
    None
):
    assert hash(Err("error1")) != hash(Err("error2"))


def test_result_repr_when_ok_result_then_returns_expected_string() -> None:
    assert repr(Ok(42)) == "Result(is_ok=True, value=42, error=None)"
    assert repr(Ok("test")) == "Result(is_ok=True, value=test, error=None)"


def test_result_repr_when_err_result_then_returns_expected_string() -> None:
    assert repr(Err("error")) == "Result(is_ok=False, value=None, error=error)"
    assert repr(Err(42)) == "Result(is_ok=False, value=None, error=42)"


def test_result_str_when_ok_result_then_returns_expected_string() -> None:
    assert str(Ok(42)) == "Result(42, None)"
    assert str(Ok("test")) == "Result(test, None)"


def test_result_str_when_err_result_then_returns_expected_string() -> None:
    assert str(Err("error")) == "Result(None, error)"
    assert str(Err(42)) == "Result(None, 42)"


def test_result_hash_and_equality_when_equal_results_then_have_same_hash() -> None:
    r1 = Ok(42)
    r2 = Ok(42)
    r3 = Err("error")
    r4 = Err("error")

    assert r1 == r2 and hash(r1) == hash(r2)
    assert r3 == r4 and hash(r3) == hash(r4)
    assert r1 != r3 and hash(r1) != hash(r3)


def test_result_with_complex_objects_when_comparing_and_hashing_then_behaves_correctly() -> (
    None
):
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

    assert Ok(obj1) == Ok(obj2)
    assert Ok(obj1) != Ok(obj3)
    assert hash(Ok(obj1)) == hash(Ok(obj2))
    assert hash(Ok(obj1)) != hash(Ok(obj3))


def test_result_repr_and_str_with_complex_objects_when_converted_then_uses_object_repr() -> (
    None
):
    class ComplexObject:
        def __repr__(self):
            return "ComplexObject()"

    obj = ComplexObject()

    assert repr(Ok(obj)) == "Result(is_ok=True, value=ComplexObject(), error=None)"
    assert str(Ok(obj)) == "Result(ComplexObject(), None)"
    assert repr(Err(obj)) == "Result(is_ok=False, value=None, error=ComplexObject())"
    assert str(Err(obj)) == "Result(None, ComplexObject())"
