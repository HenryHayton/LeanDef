## Object

Given a linear recurrence relation over a commutative semiring `R`, `VTask.mkSol` constructs the unique sequence `ℕ → R` that (a) agrees with prescribed initial values on indices `0, 1, …, order − 1`, and (b) satisfies the recurrence for all subsequent indices. Concretely, if the recurrence has order `d`, the first `d` terms are read directly from `init`, and every later term is the prescribed linear combination of the preceding `d` terms.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mkSol : {R : Type u_1} -> [CommSemiring R] -> (E : LinearRecurrence R) -> (init : Fin E.order → R) -> ℕ → R
<!-- PINNED-SIGNATURE:END -->


`VTask.mkSol : {R : Type u_1} -> [CommSemiring R] -> (E : LinearRecurrence R) -> (init : Fin E.order → R) -> ℕ → R`

The implicit type `R` is the coefficient and value universe; it must carry a `CommSemiring` instance. `E` is the linear recurrence whose structure (order and coefficients) governs the relation. `init` is a finite tuple of length `E.order` supplying the initial values: position `⟨n, h⟩` gives the value the resulting sequence must take at index `n < E.order`. The final argument is the natural-number index at which to evaluate the constructed sequence.

## Conventions

For indices `n` in the range `0 ≤ n < E.order`, the sequence returns exactly `init ⟨n, h⟩`, regardless of what the recurrence coefficients are. For indices `n ≥ E.order`, the sequence is defined recursively by the recurrence relation, using the `E.order` many values at positions `n − E.order, n − E.order + 1, …, n − 1`.

## Worked examples

- Claim: For the Fibonacci recurrence (order 2, coefficients [1, 1]) with `init = ![0, 1]`, `VTask.mkSol E init 0 = 0`.

- Claim: For the Fibonacci recurrence (order 2, coefficients [1, 1]) with `init = ![0, 1]`, `VTask.mkSol E init 1 = 1`.

- Claim: For the Fibonacci recurrence (order 2, coefficients [1, 1]) with `init = ![0, 1]`, `VTask.mkSol E init 2 = 0 * 1 + 1 * 1 = 1` (i.e., the sum of the two preceding values).

- Claim: `VTask.mkSol` is injective: distinct `init` tuples yield distinct sequences. (Formally: `E.mkSol` is an injective function from `Fin E.order → R` to `ℕ → R`.)

- Claim: `VTask.mkSol E init` is a solution of `E` in the sense of `E.IsSolution`.

## Boundaries

- When `E.order = 0`, there are no initial conditions (`Fin 0 → R` is a unique empty function), and every index `n` satisfies `n ≥ 0 = E.order`, so the sequence is defined entirely by the (empty) recurrence sum, which evaluates to `0` for every index.
- When the recurrence coefficients are all zero, `VTask.mkSol E init n = 0` for all `n ≥ E.order`, regardless of `init`.
- The function is total on all `n : ℕ`; there is no partial or undefined case.
- `VTask.mkSol E init` is the *unique* solution agreeing with `init` on the initial segment: any other solution of `E` with the same initial values is pointwise equal to `VTask.mkSol E init`.

## Not to be confused with

- `LinearRecurrence.IsSolution`: a predicate asserting that a given sequence satisfies the recurrence, not a constructor for such a sequence.
- `LinearRecurrence.solSpace`: the full submodule (or space) of all solutions, of which `VTask.mkSol E init` is a particular element parameterised by initial data.
- `LinearRecurrence.coeffs`: the coefficient tuple of the recurrence itself, one of the ingredients consumed by `VTask.mkSol`, not the solution produced by it.