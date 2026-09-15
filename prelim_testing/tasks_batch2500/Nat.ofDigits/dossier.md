## VTask.ofDigits

### Object

`VTask.ofDigits b L` interprets a finite list `L` of natural numbers as the value of a polynomial evaluated at `b`, working in any semiring `α`. The list is treated as little-endian digit representation: the first element of `L` is the units digit, the second is the coefficient of `b`, the third of `b²`, and so on. Concretely, if `L = [d₀, d₁, d₂, …, dₙ₋₁]`, the result is `d₀ + b·(d₁ + b·(d₂ + … + b·dₙ₋₁…))`, which equals `∑ i, dᵢ · bⁱ`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofDigits : {α : Type u_1} -> [Semiring α] -> (b : α) -> List ℕ → α
<!-- PINNED-SIGNATURE:END -->


The implicit type argument `α` is the semiring in which the output lives; the instance argument supplies its ring operations. The explicit argument `b` is the base, an element of `α` at which the digit polynomial is evaluated. The final argument is the list of digit coefficients, given as natural numbers (which are coerced into `α`), in little-endian order (least significant first).

### Conventions

When the digit list is empty, the result is the zero element of the semiring — an empty sum of digit contributions is 0. When the base is 0, any digit beyond the leading one contributes nothing, so `VTask.ofDigits 0 L` equals the first element of `L` (as an element of `α`) if `L` is nonempty, and 0 otherwise. When all digits are 0, regardless of the base, the result is 0. Trailing zero digits do not affect the value: appending zeros to the digit list leaves the result unchanged.

### Worked Examples

- Claim: `VTask.ofDigits 10 [3, 2, 1]` (over `ℕ`) equals 123, since 3 + 10·(2 + 10·1) = 3 + 20 + 100 = 123.

- Claim: `VTask.ofDigits 1 [a, b, c]` (over `ℕ`) equals `a + b + c`, the list sum, because every power of 1 is 1.

- Claim: `VTask.ofDigits 2 [1, 0, 1]` (over `ℕ`) equals 5, since 1 + 2·(0 + 2·1) = 1 + 0 + 4 = 5.

- Claim: `VTask.ofDigits b []` equals `0` in any semiring, by the base case of the recursion.

- Claim: `VTask.ofDigits (-1 : ℤ) [3, 1, 4, 1]` equals `3 - 1 + 4 - 1 = 5`, the alternating sum of the digits.

### Boundaries

- **Empty list**: Returns 0 in the semiring. This is consistent with the polynomial evaluation interpretation (empty sum).
- **Single-element list `[d]`**: Returns `d` (coerced to `α`), since there is no base contribution.
- **Base 0**: Only the first digit survives; all higher-place digits are multiplied by some power of 0 and vanish.
- **Base 1 (over `ℕ`)**: The result equals the sum of the digits, since every `bⁱ = 1`.
- **Trailing zeros**: Appending any number of 0s to the digit list does not change the result.
- **All-zero list of any length**: The result is always 0, regardless of the base.
- **Negative base** (in a ring like `ℤ`): The function is still well-defined; for base `−1` the result is the alternating sum of the digits.
- **No upper bound on digit values**: The function accepts any `ℕ` values as digits and makes no assumption that they are less than the base; such constraints arise only in theorems about digit representations.

### Not to be confused with

- `Nat.digits`: The inverse operation — given a base and a natural number, produces the little-endian list of proper digits. `VTask.ofDigits` goes the other direction (list → semiring element).
- `Polynomial.eval`: Evaluates a polynomial (with coefficients in a ring) at a point; `VTask.ofDigits` is morally the same but works specifically with a `List ℕ` of coefficients and coerces them, rather than using a `Polynomial` type.
- `List.sum`: Computes the plain sum of a list of elements; coincides with `VTask.ofDigits 1 L` but ignores positional weights in general.
