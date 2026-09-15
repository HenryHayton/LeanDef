## Object

A weight function `w : σ → M` (where `M` is an additive commutative monoid) is called **nontorsion** if none of its values is a torsion element of `M`. Concretely, for every natural number `n` and every index `x`, if `n` times `w x` equals zero in `M`, then `n` itself must be zero. In other words, no nonzero natural-number scalar can annihilate any value of `w`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.NonTorsionWeight : {M : Type u_2} -> {σ : Type u_3} -> [AddCommMonoid M] -> (w : σ → M) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.NonTorsionWeight : {M : Type u_2} -> {σ : Type u_3} -> [AddCommMonoid M] -> (w : σ → M) -> Prop`

`M` is the target additive commutative monoid in which weights live. `σ` is the index type (the set of variables or generators being weighted). The instance `[AddCommMonoid M]` provides the additive monoid structure needed to state scalar multiplication and the zero element. The explicit argument `w` is the weight function whose values are being tested for the nontorsion condition.

## Conventions

No junk-value or edge-case conventions are declared: the property is a universally quantified `Prop` that is vacuously true when `σ` is empty (there are no indices to check) and is well-formed for any `M` and `σ`.

## Worked examples

- Claim: The weight function `w : Fin 3 → ℤ` sending every index to `1` is nontorsion, because `ℤ` is torsion-free and all values are nonzero.

- Claim: If `M` is an add-torsion-free monoid and `w i ≠ 0` for all `i`, then `VTask.NonTorsionWeight w` holds (this is `MvPolynomial.nonTorsionWeight_of`).

- Claim: The constant zero weight function `w : σ → ℤ`, `w x = 0` for all `x`, is **not** nontorsion, because taking `n = 1` gives `1 • 0 = 0` yet `1 ≠ 0`.

- Claim: For `M = ZMod 2` and any weight function `w : σ → ZMod 2` with `w x ≠ 0` for some `x`, `VTask.NonTorsionWeight w` fails because `2 • w x = 0` while `2 ≠ 0`.

## Boundaries

- When `σ` is the empty type, the universal quantifier over `x : σ` is vacuously satisfied, so every weight function on an empty index type is nontorsion.
- When `M = ℕ` (or any torsion-free monoid) and all values `w x` are nonzero, the nontorsion condition holds because the only way `n • m = 0` in a torsion-free monoid with `m ≠ 0` is `n = 0`.
- The condition concerns only the **values** of `w`, not any ordering or algebraic structure beyond the additive monoid. In particular, zero values in `w` automatically violate nontorsion (taking `n = 1` witnesses the failure), so a nontorsion weight must assign nonzero values to every index.
- The scalar `n` ranges over `ℕ` (natural numbers), matching the `n • m` notation for `nsmul` in an additive commutative monoid.

## Not to be confused with

- **`AddMonoid.IsTorsionFree` / `IsAddTorsionFree`**: A property of the monoid `M` itself saying no nonzero element is torsion; `VTask.NonTorsionWeight` is a property of a specific weight function, not the whole monoid.
- **`weightedDegree` being nonzero**: A related but distinct condition on monomials or polynomials, not on the weight function itself.
- **Injective weight functions**: A weight function can be injective without being nontorsion (if `M` has torsion), and nontorsion does not require injectivity.