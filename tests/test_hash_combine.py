from shared_kernel import hash_combine


def test_when_given_seed_and_one_argument_should_return_expected_hash():
    assert hash_combine(1, seed=42) == 176365455100


def test_when_given_seed_and_multiple_arguments_should_return_expected_hash():
    assert hash_combine(1, 2, 3, seed=42) == 728965882225371


def test_when_called_multiple_times_with_same_input_and_seed_should_return_consistent_result():
    seed = 200
    assert hash_combine(1, 2, 3, seed=seed) == hash_combine(1, 2, 3, seed=seed)


def test_when_argument_order_changed_should_return_different_result():
    seed = 300
    assert hash_combine(1, 2, 3, seed=seed) != hash_combine(3, 2, 1, seed=seed)


def test_when_using_different_seeds_should_return_different_results():
    assert hash_combine(1, 2, 3, seed=400) != hash_combine(1, 2, 3, seed=500)


def test_when_no_seed_provided_should_return_integer_result():
    result1 = hash_combine(1, 2, 3)
    result2 = hash_combine(1, 2, 3)
    assert isinstance(result1, int)
    assert isinstance(result2, int)


def test_when_given_different_types_should_return_integer_result():
    seed = 600
    result = hash_combine(1, "hello", 3.14, True, seed=seed)
    assert isinstance(result, int)


def test_when_given_no_arguments_should_generate_random_int():
    seed = 700
    assert hash_combine(seed=seed) == 823877051


def test_when_given_large_input_should_return_integer_result():
    seed = 800
    large_list = list(range(1000))
    result = hash_combine(*large_list, seed=seed)
    assert isinstance(result, int)


def test_when_given_same_input_different_seeds_should_return_different_results():
    seed1, seed2 = 900, 901
    assert hash_combine(1, 2, 3, seed=seed1) != hash_combine(1, 2, 3, seed=seed2)
