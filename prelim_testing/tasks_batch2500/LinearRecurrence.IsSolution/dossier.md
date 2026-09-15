## VTask.IsSolution

### Object

Given a linear recurrence relation `E` of order `d` over a commutative semiring `R`, `VTask.IsSolution E u` is the proposition that the sequence `u : ℕ → R` is a **solution** of `E`. This means that for every natural number `n`, the value `u` takes at position `n + d` equals the prescribed linear combination of the preceding `d` values: specifically, `u(n + d)` equals the sum over `i = 0, …, d−1` of `coeffs(i) · u(n + i)`. In other words, `u` obeys the recurrence at every index without exception.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsSolution : {R : Type u_1} -> [CommSemiring R] -> (E : LinearRecurrence R) -> (u : ℕ → R) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsSolution : {R : Type u_1} -> [CommSemiring R] -> (E : LinearRecurrence R) -> (u : ℕ → R) -> Prop`

The implicit type `R` is the coefficient domain, which is required to be a commutative semiring. The instance argument supplies the commutative semiring structure on `R`. The argument `E` is the linear recurrence being considered — it packages the order (the number of previous terms the recurrence depends on) together with its coefficient sequence. The argument `u` is the candidate sequence whose membership as a solution is being asserted.

### Conventions

No special junk-value or boundary conventions are declared for this predicate: it is a universally quantified statement over all natural numbers, and the universal quantifier over an empty range (e.g., when `E.order = 0`) is vacuously true, making every sequence a solution of a zero-order recurrence.

### Worked examples

- Claim: The constant-zero sequence `fun n => (0 : ℤ)` is a solution of any linear recurrence over ℤ, since both sides of the recurrence equation equal zero.

- Claim: For the Fibonacci recurrence of order 2 with `coeffs 0 = 1` and `coeffs 1 = 1`, the sequence `fun n => Nat.fib n` (cast to a suitable ring) satisfies `VTask.IsSolution E (fun n => Nat.fib n)` because `fib(n + 2) = fib(n) + fib(n + 1)` holds for all `n`.

- Claim: If `q` is a root of the characteristic polynomial of `E`, then the geometric sequence `fun n => q ^ n` satisfies `VTask.IsSolution E (fun n => q ^ n)` — this is precisely the content of `geom_sol_iff_root_charPoly`.

- Claim: A sequence `u` is a solution of `E` if and only if it belongs to the solution space `E.solSpace` (a submodule of `ℕ → R`), reflecting that the set of solutions is closed under addition and scalar multiplication.

- Claim: Two solutions `u` and `v` of `E` are equal as sequences if and only if they agree on the initial segment `{0, 1, …, E.order − 1}`, so a solution is uniquely determined by its first `E.order` values.

### Boundaries

- **Order 0**: When `E.order = 0`, the recurrence body is an empty sum (equal to zero), so `VTask.IsSolution E u` requires `u n = 0` for all `n`, i.e., only the zero sequence is a solution.
- **Order 0 coefficients**: If `E.order > 0` but all coefficients are zero, the recurrence requires `u(n + order) = 0` for all `n`; sequences satisfying this are exactly those that vanish from index `order` onward and are otherwise unconstrained on `{0, …, order−1}`.
- **Constant sequences**: A constant sequence `fun _ => c` satisfies the recurrence precisely when `c = c · (sum of all coefficients)`, i.e., either `c = 0` or the coefficients sum to 1.
- **No upper-index restriction**: The predicate is a universal statement over all `n : ℕ`, so there is no finite approximation; a sequence that satisfies the recurrence only for `n < N` is not a solution.

### Not to be confused with

- **`E.mkSol init`**: This is the *construction* of the unique solution with prescribed initial values, rather than the predicate asserting that a given sequence is a solution.
- **`E.solSpace`**: This is the submodule of all solutions viewed as a linear subspace; `VTask.IsSolution E u` is equivalent to membership in `E.solSpace`, but the predicate and the submodule are distinct objects.
- **`E.charPoly.IsRoot q`**: This is the root condition for the characteristic polynomial, which characterises exactly when the geometric sequence `q^n` is a solution, but it applies only to geometric sequences, not arbitrary ones.