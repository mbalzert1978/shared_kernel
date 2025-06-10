## Result Type

The `Result` type is used for returning and propagating errors. It represents either success (`Ok`) or failure (`Err`).

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

-   `Ok(T)`: Represents success and contains a value of type `T`.
-   `Err(E)`: Represents an error and contains an error value of type `E`.

### Querying the Variant

-   `is_ok() -> bool`: Returns `true` if the result is `Ok`.
-   `is_err() -> bool`: Returns `true` if the result is `Err`.
-   `is_ok_and(f: impl FnOnce(T) -> bool) -> bool`: Returns `true` if the result is `Ok` and the value inside of it matches a predicate.
-   `is_err_and(self, f: impl FnOnce(E) -> bool) -> bool`: Returns `true` if the result is `Err` and the value inside of it matches a predicate.

### Adapters for Each Variant

-   `ok() -> Option<T>`: Converts `Result<T, E>` to `Option<T>`, discarding the error if any.
-   `err() -> Option<E>`: Converts `Result<T, E>` to `Option<E>`, discarding the success value if any.

### Transforming Contained Values

-   `map<U, F: FnOnce(T) -> U>(self, op: F) -> Result<U, E>`: Maps a `Result<T, E>` to `Result<U, E>` by applying a function to a contained `Ok` value, leaving an `Err` value untouched.
-   `map_or<U, F: FnOnce(T) -> U>(self, default: U, f: F) -> U`: Returns the provided default (if `Err`), or applies a function to the contained value (if `Ok`).
-   `map_or_else<U, D: FnOnce(E) -> U, F: FnOnce(T) -> U>(self, default: D, f: F) -> U`: Maps a `Result<T, E>` to `U` by applying fallback function `default` to a contained `Err` value, or function `f` to a contained `Ok` value.
-   `map_err<F, O: FnOnce(E) -> F>(self, op: O) -> Result<T, F>`: Maps a `Result<T, E>` to `Result<T, F>` by applying a function to a contained `Err` value, leaving an `Ok` value untouched.
-   `inspect<F: FnOnce(&T)>(self, f: F) -> Self`: Calls a function with a reference to the contained value if `Ok`. Returns the original result.
-   `inspect_err<F: FnOnce(&E)>(self, f: F) -> Self`: Calls a function with a reference to the contained value if `Err`. Returns the original result.

### Extracting Contained Values

-   `expect(self, msg: &str) -> T`: Returns the contained `Ok` value, consuming the `self` value. Panics if the value is an `Err`, with a panic message including the passed message, and the content of the `Err`.
-   `unwrap(self) -> T`: Returns the contained `Ok` value, consuming the `self` value. Panics if the value is an `Err`, with a panic message provided by the `Err`'s value.
-   `unwrap_or_default(self) -> T`: Returns the contained `Ok` value or a default. If `Err`, returns the default value for that type.
-   `expect_err(self, msg: &str) -> E`: Returns the contained `Err` value, consuming the `self` value. Panics if the value is an `Ok`, with a panic message including the passed message, and the content of the `Ok`.
-   `unwrap_err(self) -> E`: Returns the contained `Err` value, consuming the `self` value. Panics if the value is an `Ok`, with a custom panic message provided by the `Ok`'s value.
-   `into_ok(self) -> T`: Returns the contained `Ok` value, but never panics.
-   `into_err(self) -> E`: Returns the contained `Err` value, but never panics.
-   `unwrap_or(self, default: T) -> T`: Returns the contained `Ok` value or a provided default.
-   `unwrap_or_else<F: FnOnce(E) -> T>(self, op: F) -> T`: Returns the contained `Ok` value or computes it from a closure.

### Boolean Operations

-   `and<U>(self, res: Result<U, E>) -> Result<U, E>`: Returns `res` if the result is `Ok`, otherwise returns the `Err` value of `self`.
-   `and_then<U, F: FnOnce(T) -> Result<U, E>>(self, op: F) -> Result<U, E>`: Calls `op` if the result is `Ok`, otherwise returns the `Err` value of `self`.
-   `or<F>(self, res: Result<T, F>) -> Result<T, F>`: Returns `res` if the result is `Err`, otherwise returns the `Ok` value of `self`.
-   `or_else<F, O: FnOnce(E) -> Result<T, F>>(self, op: O) -> Result<T, F>`: Calls `op` if the result is `Err`, otherwise returns the `Ok` value of `self`.

### Iterating over `Result`

-   `iter() -> Iter<'_, T>`: Returns an iterator over the possibly contained value. The iterator yields one value if the result is `Result::Ok`, otherwise none.
-   `iter_mut() -> IterMut<'_, T>`: Returns a mutable iterator over the possibly contained value. The iterator yields one value if the result is `Result::Ok`, otherwise none.
-   `into_iter() -> IntoIter<T>`: Returns a consuming iterator over the possibly contained value. The iterator yields one value if the result is `Result::Ok`, otherwise none.

### Collecting into `Result`

-   `from_iter<I: IntoIterator<Item = Result<A, E>>>(iter: I) -> Result<V, E>`: Takes each element in the `Iterator`: if it is an `Err`, no further elements are taken, and the `Err` is returned. Should no `Err` occur, a container with the values of each `Result` is returned.
```
