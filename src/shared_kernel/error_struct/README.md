# Error Handling

This module provides a standardized way to represent and handle errors.

## Classes

- `Error`: Represents an error with a code and description.

## Usage

```python
from shared_kernel.error_struct import Error

error = Error("404", "Not Found")
print(error)  # Output: 404:Not Found

# Create from HTTP status
from http import HTTPStatus
error = Error.from_(HTTPStatus.NOT_FOUND)
```

For more details, refer to the `Error` class documentation.