## Object

`VTask.FermatLastTheoremWith R n` is the proposition asserting that Fermat's Last Theorem holds in the semiring `R` at exponent `n`: there are no three nonzero elements `a`, `b`, `c` of `R` satisfying `a^n + b^n = c^n`. It is the natural generalization of the classical FLT statement from the integers to an arbitrary semiring, parameterized by both the ambient algebraic structure and the specific exponent.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.FermatLastTheoremWith : (R : Type u_1) -> [Semiring R] -> (n : ℕ) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.FermatLastTheoremWith : (R : Type u_1) -> [Semiring R] -> (n : ℕ) -> Prop`

The first argument `R` is the semiring in which the equation is to be tested. The implicit `Semiring R` instance endows `R` with the necessary addition, multiplication, and exponentiation. The argument `n` is the natural-number exponent appearing in the equation `a^n + b^n = c^n`.

## Conventions

The nonzero conditions are part of the statement: a triple `(a, b, c)` is only a potential counterexample when all three of `a`, `b`, `c` are nonzero in `R`. There are no junk-value conventions to declare beyond this; the definition is total over all semirings `R` and all natural numbers `n`.

## Worked examples

- Claim: `VTask.FermatLastTheoremWith ℕ n` is equivalent to the classical `FermatLastTheoremFor n` (Fermat's Last Theorem for natural numbers at exponent `n`).

- Claim: `VTask.FermatLastTheoremWith ℤ n` is equivalent to the classical `FermatLastTheoremFor n`, confirming that passing to the integers does not change whether FLT holds at a given exponent.

- Claim: `VTask.FermatLastTheoremWith ℚ n` is also equivalent to the classical `FermatLastTheoremFor n`, so the three rings ℕ, ℤ, ℚ all carry the same instance of this statement.

- Claim: If `m ∣ n` and `VTask.FermatLastTheoremWith R m` holds, then `VTask.FermatLastTheoremWith R n` holds; that is, `VTask.FermatLastTheoremWith R` is monotone with respect to divisibility of the exponent.

## Boundaries

- At `n = 0`: every nonzero element satisfies `a^0 = 1`, so in a semiring where `1 + 1 = 1` (e.g., the zero semiring or certain Boolean algebras) the statement might fail, while in `ℕ`, `ℤ`, or `ℚ` it fails because `1 + 1 = 2 = 1` is false, so the theorem would actually hold vacuously or fail depending on the semiring — the definition itself imposes no restriction and applies uniformly.
- At `n = 1`: the equation `a + b = c` has solutions in nearly every nontrivial semiring with nonzero elements (e.g., `1 + 1 = 2` in ℕ), so `VTask.FermatLastTheoremWith R 1` typically fails.
- At `n = 2`: the Pythagorean equation has solutions over ℕ (e.g., `3^2 + 4^2 = 5^2`), so `VTask.FermatLastTheoremWith ℕ 2` is false.
- For a semiring in which every nonzero element is a unit (a semifield), a related but distinct variant (`FermatLastTheoremWith'`) holds; the two notions differ on whether all nonzero elements or just non-unit elements are excluded.

## Not to be confused with

- `FermatLastTheoremFor n`: the classical statement only over the natural numbers for a fixed exponent, equivalent to `VTask.FermatLastTheoremWith ℕ n` but not parameterized over an arbitrary semiring.
- `FermatLastTheoremWith' R n`: a variant where the hypothesis is that `a`, `b`, `c` are nonzero *non-units* (rather than just nonzero), making it a weaker assumption and a stronger conclusion in domains where units exist.
- `FermatLastTheorem`: the single unparameterized statement asserting FLT for all exponents `n ≥ 3`, rather than for one fixed exponent `n` in one fixed ring `R`.