from functools import reduce

from shared_kernel.design_by_contract import ArgumentException

GOLDEN_RATIO = 0x9E3779B9
LEFT_SHIFT = 6
RIGHT_SHIFT = 2
ACC = 0


def hash_combine(*args: object) -> int:
    """
    Combine multiple hash values into one using a Boost-like approach with reduce().

    Args:
        *args: Any number of hashable objects to combine.

    Returns:
        int: The combined hash value.
    """
    ArgumentException.raise_if_none_or_empty(args, "args")

    return reduce(
        lambda acc, arg: acc
        ^ (hash(arg) + GOLDEN_RATIO + (acc << LEFT_SHIFT) + (acc >> RIGHT_SHIFT)),
        args,
        ACC,
    )
