## VTask.unitCoeff

### Object

Given a nonzero p-adic integer `x` in `ℤ_[p]`, every such element admits a unique decomposition `x = u · pⁿ` where `n` is the p-adic valuation of `x` and `u` is a unit in `ℤ_[p]` (i.e., an element of p-adic norm exactly 1). `VTask.unitCoeff hx` returns that unit `u`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.unitCoeff : {p : ℕ} -> [hp : Fact (Nat.Prime p)] -> {x : ℤ_[p]} -> (hx : x ≠ 0) -> ℤ_[p]ˣ
<!-- PINNED-SIGNATURE:END -->


The implicit argument `p` is the prime whose associated p-adic integer ring `ℤ_[p]` is the ambient setting; the typeclass `hp` witnesses that `p` is indeed prime. The implicit argument `x` is the p-adic integer being decomposed. The explicit argument `hx` is a proof that `x` is nonzero, which is required because the zero element has no well-defined unit part.

### Conventions

There are no junk-value conventions to declare: the function is total on its stated domain (nonzero p-adic integers), and the output is always a genuine unit in `ℤ_[p]` by construction.

### Worked examples

- Claim: For any nonzero `x : ℤ_[p]`, the unit `VTask.unitCoeff hx` satisfies `x = (VTask.unitCoeff hx : ℤ_[p]) * p ^ x.valuation` (the fundamental decomposition identity).

- Claim: For any nonzero `x : ℤ_[p]`, the coercion of `VTask.unitCoeff hx` to `ℚ_[p]` equals `x * (p : ℚ_[p]) ^ (-x.valuation : ℤ)`.

- Claim: The p-adic norm of `(VTask.unitCoeff hx : ℤ_[p])`, viewed as an element of `ℚ_[p]`, is equal to 1, confirming it is a unit.

### Boundaries

- The input `x` must be nonzero; the zero element of `ℤ_[p]` has valuation `+∞` (or is treated as having valuation larger than any integer), so no finite power of `p` can factor it into a unit times a power of `p`, and the construction is undefined for `x = 0`.
- When `x` is itself already a unit (i.e., `x.valuation = 0`), `VTask.unitCoeff hx` coincides with `x` viewed as a unit.
- When `x = p^n` for some positive integer `n`, `VTask.unitCoeff hx` is the unit `1` (the multiplicative identity of `ℤ_[p]ˣ`).

### Not to be confused with

- `PadicInt.valuation`: the p-adic valuation `x.valuation : ℤ` which gives the exponent `n` in the decomposition, not the unit part.
- `PadicInt.mkUnits`: a lower-level constructor that wraps a p-adic number of norm 1 into a unit; `VTask.unitCoeff` builds on this but adds the conceptual role of extracting the unit factor from a decomposition.
- `Padic.unitCoeff` (if it existed for `ℚ_[p]`): `VTask.unitCoeff` specifically targets the subring `ℤ_[p]` of p-adic integers, not the full field of p-adic numbers.