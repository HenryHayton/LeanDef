## VTask.normFromConst

### Object

Given a field `K`, a ring seminorm `g` on `K`, a distinguished element `k` of `K`, and the hypotheses that `g(1) ≤ 1`, that `g(k) ≠ 0`, and that `g` is power-multiplicative, `VTask.normFromConst` produces a genuine ring norm on `K`. The underlying function of this norm is the "seminorm from constant" construction: for each `x ∈ K`, the value is the limit of the antitone sequence `n ↦ g(x · kⁿ) / g(k)ⁿ`. The key upgrade from seminorm to norm is guaranteed by the non-vanishing hypothesis on `k`: because `g(k) ≠ 0`, the element `k` witnesses that the constructed seminorm is non-degenerate (it does not send any nonzero element to zero), hence it qualifies as a full ring norm.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.normFromConst : {K : Type u_1} -> [Field K] -> {k : K} -> {g : RingSeminorm K} -> (hg1 : g 1 ≤ 1) -> (hg_k : g k ≠ 0) -> (hg_pm : IsPowMul ⇑g) -> RingNorm K
<!-- PINNED-SIGNATURE:END -->


`VTask.normFromConst : {K : Type u_1} -> [Field K] -> {k : K} -> {g : RingSeminorm K} -> (hg1 : g 1 ≤ 1) -> (hg_k : g k ≠ 0) -> (hg_pm : IsPowMul ⇑g) -> RingNorm K`

- `K` is the field on which the norm is constructed; it is an implicit universe-polymorphic type argument.
- The `Field K` instance supplies the field structure used throughout the construction.
- `k` is the "constant" element of `K` whose orbit under `g` drives the limiting construction; it is implicit and inferred from context.
- `g` is the ring seminorm on `K` from which the norm is built; it is implicit and inferred from context.
- `hg1` is the proof that `g` maps the multiplicative identity to a value at most `1`, i.e., `g(1) ≤ 1`.
- `hg_k` is the proof that `g` does not vanish at the chosen constant `k`, i.e., `g(k) ≠ 0`; this is the hypothesis that promotes the output from a seminorm to a genuine norm.
- `hg_pm` is the proof that `g` is power-multiplicative, meaning `g(xⁿ) = g(x)ⁿ` for all `x ∈ K` and all natural numbers `n`.

### Conventions

There are no junk-value or edge conventions to declare: the definition is a bundled construction whose every input is a hypothesis, so it is only ever invoked when all three proof arguments are satisfied; there is no undefined or degenerate regime to document.

### Worked examples

- Claim: The value of `VTask.normFromConst hg1 hg_k hg_pm` at the constant `k` equals `g k`. That is, the constructed norm agrees with the original seminorm when evaluated at the element used to drive the construction.

- Claim: The constructed norm `VTask.normFromConst hg1 hg_k hg_pm` is power-multiplicative: for every `x : K` and every `n : ℕ`, the norm of `xⁿ` equals the `n`-th power of the norm of `x`.

- Claim: For every `x : K`, the value of the constructed norm at `x` is at most `g x`. That is, the "seminorm from constant" construction can only decrease the seminorm values, never increase them.

- Claim: The constructed norm satisfies `VTask.normFromConst hg1 hg_k hg_pm 1 = 1`. Because `g(1) ≤ 1` and the norm is power-multiplicative with the unit element, the norm of the multiplicative identity is exactly `1`.

### Boundaries

- The definition requires all three proof arguments to be provided. If any hypothesis fails — e.g., if `g(1) > 1`, or `g(k) = 0`, or `g` is not power-multiplicative — the construction is simply not applicable and cannot be invoked.
- When `k = 1` satisfies `g(1) ≠ 0` (which together with `g(1) ≤ 1` means `0 < g(1) ≤ 1`), the element `1` may serve as the constant. In this case the resulting norm still evaluates to `g(1) = 1` at `1` (since `seminormFromConst_one` holds).
- The hypothesis `g(k) ≠ 0` ensures that the infimum defining the seminorm is achieved away from zero, so the resulting function is nondegenerate. Without this, one would only obtain a seminorm.
- The output is a `RingNorm K`, meaning it is a ring seminorm that additionally satisfies `‖x‖ = 0 → x = 0`.

### Not to be confused with

- `seminormFromConst`: the precursor construction that produces only a `RingSeminorm` (not necessarily nondegenerate), from the same data but without the full norm guarantee.
- `algNormFromConst`: a variant of this construction specialized to algebraic extensions and the spectral norm, producing an algebra norm rather than a plain ring norm.
- `RingSeminorm.toRingNorm`: the general mechanism that upgrades any nontrivial ring seminorm to a ring norm, of which this definition is a specific instance applied to the seminorm-from-constant construction.