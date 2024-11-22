# Protocol Interfaces

This module provides protocol interfaces for common patterns in type conversions and default values.

## Interfaces

- `ITryFrom`: For types that can be conditionally converted from another type.
- `ITryInto`: For types that can be conditionally converted into another type.
- `IFrom`: For types that can be unconditionally converted from another type.
- `IInto`: For types that can be unconditionally converted into another type.
- `IDefault`: For types that have a default value.

## Usage

```python
from shared_kernel.abstractions import ITryFrom, IInto, IDefault

class MyType(ITryFrom[str], IInto[int], IDefault):
    @classmethod
    def try_from(cls, source: str) -> Result[Self, Exception]:
        # Implementation here

    def into(self) -> int:
        # Implementation here

    @classmethod
    def default(cls) -> Self:
        # Implementation here
```

Implement these interfaces in your classes to standardize type conversions and default value creation.