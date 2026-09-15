## Object

Given a prime `p` and a `p`-adic number `u ∈ ℚ_[p]` whose `p`-adic norm equals 1, `VTask.mkUnits` produces a *unit* of the `p`-adic integers `ℤ_[p]` whose underlying element is `u` (viewed as an element of `ℤ_[p]` via the embedding). In other words, it packages the algebraic fact that any `p`-adic number of norm exactly 1 is both an integer (norm ≤ 1) and invertible inside the ring of `p`-adic integers.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mkUnits : {p : ℕ} -> [hp : Fact (Nat.Prime p)] -> {u : ℚ_[p]} -> (h : ‖u‖ = 1) -> ℤ_[p]ˣ
<!-- PINNED-SIGNATURE:END -->


The implicit argument `p` is a natural number serving as the prime. The instance `hp` witnesses that `p` is prime and is used to furnish the `p`-adic structures. The implicit argument `u` is the `p`-adic number (an element of `ℚ_[p]`) being promoted. The explicit argument `h` is the proof that the `p`-adic norm of `u` is exactly 1; this is the sole condition required to guarantee that `u` lies in `ℤ_[p]` and is a unit there.

## Conventions

When the norm condition `‖u‖ = 1` holds, the resulting unit's underlying `ℤ_[p]`-element coerces back to exactly `u` in `ℚ_[p]` (no information is lost). The inverse of the unit is the `p`-adic inverse of `u`, which also has norm 1 and therefore also lies in `ℤ_[p]`.

## Worked examples

- Claim: For `p = 5`, the `p`-adic number `1 ∈ ℚ_[5]` has norm 1, so `VTask.mkUnits` applied to it yields the multiplicative identity unit of `ℤ_[5]`, and its coercion to `ℚ_[5]` is `1`.

- Claim: For any prime `p` and any `u : ℚ_[p]` with `h : ‖u‖ = 1`, the coercion `((VTask.mkUnits h : ℤ_[p]) : ℚ_[p])` equals `u`.

- Claim: For any prime `p` and any `u : ℚ_[p]` with `h : ‖u‖ = 1`, the value `(VTask.mkUnits h).val` equals `(⟨u, h.le⟩ : ℤ_[p])`.

## Boundaries

- The norm must be **exactly** 1, not merely ≤ 1. Elements of `ℤ_[p]` with norm strictly less than 1 (i.e., elements of the maximal ideal) are *not* units, so the strict equality is essential.
- The prime `p` must be a genuine prime (enforced by the `Fact (Nat.Prime p)` instance); the definition is not meaningful for composite or zero values of `p`, but this is handled by the typeclass system.
- There are no other domain restrictions: every `u : ℚ_[p]` satisfying `‖u‖ = 1` is accepted, including `p`-adic numbers whose rational representative is not an ordinary integer.

## Not to be confused with

- `PadicInt.unitCoercion` or inclusion of `ℤˣ` into `ℤ_[p]ˣ`: those start from ordinary integers or rational units, not from arbitrary `p`-adic numbers of norm 1.
- The coercion `ℤ_[p] → ℚ_[p]`: that goes in the opposite direction (from integers to rationals), whereas `VTask.mkUnits` starts in `ℚ_[p]` and lands in `ℤ_[p]ˣ`.
- Elements of `ℤ_[p]` with `‖u‖ ≤ 1` (all of `ℤ_[p]`): the strict equality `‖u‖ = 1` is what selects the units, not just the membership condition `‖u‖ ≤ 1`.