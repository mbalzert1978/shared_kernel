# Argument Validation

This module provides robust argument validation through the `ArgumentException` and `ArgumentNullException` classes.

## Classes

- `ArgumentException`: For general argument-related errors.
- `ArgumentNullException`: Specifically for null argument errors.

## Usage

```python
from shared_kernel.design_by_contract import ArgumentException, ArgumentNullException

# Raise if argument is None or empty
ArgumentException.raise_if_none_or_empty(some_string, "some_string")

# Raise if argument is None or whitespace
ArgumentException.raise_if_none_or_whitespace(some_string, "some_string")

# Raise if argument is None
ArgumentNullException.raise_if_none(some_object, "some_object")
```

For more details, refer to the class documentation.