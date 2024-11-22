# Result Type

This module implements the Result pattern for better error handling and control flow.

## Classes

- `Result`: Represents either a success (`Ok`) or a failure (`Err`).
- `Ok`: Represents a successful result.
- `Err`: Represents a failed result.

## Usage

```python
from shared_kernel.result_type import Result, Ok, Err

def divide(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Err("Division by zero")
    return Ok(a / b)

result = divide(10, 2)
if result.is_ok():
    print(f"Result: {result.expect('Should not fail')}")
else:
    print(f"Error: {result.err()}")
```

For more details on available methods, refer to the `Result` class documentation.