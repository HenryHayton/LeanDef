## VTask.stationaryPoint

### Object

Given a prime `p` and a `p`-adic Cauchy sequence `f` that is not equivalent to the zero sequence, `VTask.stationaryPoint f hf` is a natural number index `N` with the property that the `p`-adic absolute value of `f(n)` is the same for every index `n ≥ N`. In other words, it is a "stabilisation index" beyond which the `p`-adic norm of the sequence's terms no longer changes. Such an index exists because a non-zero `p`-adic Cauchy sequence eventually has terms of constant `p`-adic size.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.stationaryPoint : {p : ℕ} -> [Fact (Nat.Prime p)] -> {f : PadicSeq p} -> (hf : ¬f ≈ 0) -> ℕ
<!-- PINNED-SIGNATURE:END -->


`{p : ℕ}` is the prime base, supplied as an implicit argument; `[Fact (Nat.Prime p)]` is the typeclass witness asserting that `p` is indeed prime. `{f : PadicSeq p}` is the `p`-adic Cauchy sequence whose stabilisation index is sought. `(hf : ¬f ≈ 0)` is the proof that `f` is not equivalent to the zero sequence; this hypothesis is essential because the zero sequence has all norms equal to zero at every index and does not determine a meaningful "eventual norm" in the sense needed here.

### Conventions

The value returned is chosen nonconstructively (via classical choice) from the set of valid stabilisation indices, so its exact numerical value is unspecified beyond satisfying the stabilisation property. No canonical least or greatest such index is guaranteed.

### Worked examples

- Claim: For any non-zero `p`-adic sequence `f` and any `n` and `m` both at least `VTask.stationaryPoint f hf`, the `p`-adic norms `padicNorm p (f n)` and `padicNorm p (f m)` are equal.

- Claim: For any non-zero `p`-adic sequence `f` and any natural numbers `v2` and `v3`, the `p`-adic norm at `VTask.stationaryPoint f hf` equals the `p`-adic norm at `max (VTask.stationaryPoint f hf) (max v2 v3)`, since the max index is ≥ the stationary point.

- Claim: If two non-zero `p`-adic sequences `f` and `g` are equivalent to each other (`f ≈ g`), then `padicNorm p (f (VTask.stationaryPoint f hf)) = padicNorm p (g (VTask.stationaryPoint g hg))`.

### Boundaries

- The hypothesis `hf : ¬f ≈ 0` is mandatory; the definition is not applicable to the zero sequence (or any sequence equivalent to zero), because for such sequences no stabilisation index with a nonzero norm value is guaranteed to exist.
- The stabilisation index itself is a natural number, so it is always finite; there is no sense in which the sequence fails to stabilise eventually (that is guaranteed by the `stationary` lemma underlying the definition).
- The stabilisation index is not unique; there may be many valid choices, and the classical choice may return any one of them.
- Index values strictly below `VTask.stationaryPoint f hf` make no norm-constancy guarantee: the `p`-adic norm of `f(n)` for small `n` may differ from the eventual stable value.

### Not to be confused with

- `PadicSeq.norm`: the eventual `p`-adic norm value of a non-zero `p`-adic sequence, which is the *value* `padicNorm p (f (stationaryPoint f hf))`, not the stabilisation *index*.
- The Cauchy convergence index of a `p`-adic sequence: that is an index beyond which terms are close together in the `p`-adic metric, not beyond which norms are constant.
- `PadicSeq.stationary`: the proposition (an existential statement) asserting that a stabilisation index exists, which `VTask.stationaryPoint` extracts a witness from.