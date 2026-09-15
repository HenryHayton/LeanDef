## 1. Object

This function computes the $n$-th power of an element in a type equipped with a multiplication and a multiplicative identity (1). Specifically, `VTask.npowRec' n m` returns $m^n$: the $n$-fold product of $m$ with itself, using $1$ as the zeroth power. Unlike a naive left-folding recursion, this variant is structured so that, for $n \geq 1$, it acts as a semigroup homomorphism from the positive natural numbers to $M$ — in particular, the recurrence builds the product from the left so that the associativity-sensitive ordering is compatible with semigroup laws.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.npowRec' : {M : Type u_2} -> [One M] -> [Mul M] -> ℕ → M → M
<!-- PINNED-SIGNATURE:END -->


`VTask.npowRec' : {M : Type u_2} -> [One M] -> [Mul M] -> ℕ → M → M`

The type `M` is the carrier of the algebraic structure. The `One M` instance provides the multiplicative identity element `1`. The `Mul M` instance provides the binary multiplication. The first explicit argument is the natural number exponent $n$. The second explicit argument is the base element $m \in M$ to be raised to the $n$-th power.

## 3. Conventions

When the exponent is $0$, the result is $1$ regardless of the base — the standard convention for empty products. When the exponent is $1$, the result is the base element $m$ itself, with no multiplication performed. For exponents of the form $k + 2$, the result is computed recursively as `VTask.npowRec' (k + 1) m * m`, i.e., the $(k+1)$-th power multiplied on the right by $m$.

## 4. Worked Examples

- Claim: `VTask.npowRec' 0 m = 1` for any `m : M` (base case, exponent zero gives the identity).
  ```lean
  example {M : Type*} [One M] [Mul M] (m : M) : VTask.npowRec' 0 m = 1 := rfl
  ```

- Claim: `VTask.npowRec' 1 m = m` for any `m : M` (exponent one returns the base unchanged).
  ```lean
  example {M : Type*} [One M] [Mul M] (m : M) : VTask.npowRec' 1 m = m := rfl
  ```

- Claim: `VTask.npowRec' 3 m = m * m * m` in a semigroup — three-fold product.

- Claim: In `ℕ` with its usual multiplication and `1`, `VTask.npowRec' 4 2 = 16`.
  ```lean
  example : VTask.npowRec' 4 2 = 16 := by decide
  ```

- Claim: For $k \neq 0$, `VTask.npowRec' (k + 1) m = VTask.npowRec' k m * m` (successor step for positive exponents).

## 5. Boundaries

- At exponent $0$: the result is always $1$, independent of the base. This means `VTask.npowRec' 0 m = 1` even if `m` is a zero-divisor, an absorbing element, or any other unusual element.
- At exponent $1$: the result is exactly `m`, no multiplication is performed, so no associativity or identity law is invoked.
- The recursion for exponent $k + 2$ multiplies on the right by $m`, so in a non-commutative setting the order matters. The function is designed so that for $n \geq 1$, increasing the exponent appends `m` on the right.
- The function is total on all natural numbers and all types with `One` and `Mul`; no restrictions are required.

## 6. Not to be confused with

- `npowRec`: a related power function that does NOT satisfy the semigroup homomorphism property from positive naturals — it differs from `VTask.npowRec'` for exponent $k+1$ by a leading factor of $1 \cdot (-)$.
- `HPow.hPow` / `Monoid.npow`: the canonical, potentially-optimised power operation in Mathlib monoids, which may use binary exponentiation internally rather than a simple recursion.
- `npowBinRec`: a binary-recursive (fast exponentiation) power function, related to `VTask.npowRec'` via a connecting theorem but structurally different.