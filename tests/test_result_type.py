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
    with pytest.raises(ArgumentException, match="Value cannot be null.") as exc:
        Ok(None)

    assert exc.value.message == "Value cannot be null. (Parameter 'Ok.value')"
    assert exc.value.param_name == "Ok.value"


def test_err_raises_attribute_null_error_when_error_is_none():
    with pytest.raises(ArgumentException, match="Value cannot be null.") as exc:
        Err(None)

    assert exc.value.message == "Value cannot be null. (Parameter 'Err.error')"
    assert exc.value.param_name == "Err.error"
