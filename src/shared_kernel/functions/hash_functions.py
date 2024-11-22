from functools import reduce
from random import randint
from random import seed as Seed

GOLDEN_RATIO = 0x9E3779B9


def hash_combine(*args: object, seed: int | None = None) -> int:
    """
    Combine multiple hash values into one using a Boost-like approach with reduce().

    Args:
        *args: Any number of hashable objects to combine.
        seed: An optional seed value. If not provided, a random seed will be used.

    Returns:
        int: The combined hash value.
    """
    Seed(seed or GOLDEN_RATIO)
    initial_seed = randint(0, 2**32 - 1)

    def combine(acc: int, arg: object) -> int:
        return acc ^ (hash(arg) + GOLDEN_RATIO + (acc << 6) + (acc >> 2))

    return reduce(combine, args, initial_seed)
