## VTask.pi

### Object

Given an index type `ι` and a family of topological spaces `χ i` (one for each `i : ι`), and given two points `as` and `bs` in the product space `Π i, χ i`, `VTask.pi γ` is the **pointwise product path** in `Π i, χ i` from `as` to `bs`. Concretely, it is the unique path `p : Path as bs` in the product such that for each index `i`, the `i`-th coordinate of `p t` is exactly `γ i t`. In other words, it is the path whose value at each time `t ∈ [0,1]` is the tuple `(γ i t)_{i ∈ ι}`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.pi : {ι : Type u_3} -> {χ : ι → Type u_4} -> [(i : ι) → TopologicalSpace (χ i)] -> {as bs : (i : ι) → χ i} -> (γ : (i : ι) → Path (as i) (bs i)) -> Path as bs
<!-- PINNED-SIGNATURE:END -->


```
VTask.pi : {ι : Type u_3} -> {χ : ι → Type u_4} -> [(i : ι) → TopologicalSpace (χ i)] -> {as bs : (i : ι) → χ i} -> (γ : (i : ι) → Path (as i) (bs i)) -> Path as bs
```

- `ι` is the index type parametrising the family of spaces.
- `χ` is the type family assigning to each index `i` its topological space `χ i`.
- The instance argument `(i : ι) → TopologicalSpace (χ i)` supplies a topology on each component space, which together induce the product topology on `Π i, χ i`.
- `as` is the starting point in the product space, given as a dependent function `(i : ι) → χ i`; its `i`-th component `as i` is the starting point of the `i`-th path.
- `bs` is the ending point in the product space, similarly structured; `bs i` is the endpoint of the `i`-th path.
- `γ` is the family of paths: for each `i : ι`, `γ i` is a path in `χ i` from `as i` to `bs i`.

### Conventions

No special junk-value or boundary conventions are declared beyond the standard `Path` conventions: the constructed path satisfies `p 0 = as` and `p 1 = bs` by definition, and its underlying map is continuous with respect to the product topology.

### Worked examples

- Claim: For a single-index family over `ι = Unit`, `VTask.pi γ` at time `t` equals the single path `γ ()` evaluated at `t`, i.e., the product path is entirely determined by the one component.

- Claim: If each `γ i` is the constant path at `as i` (so `as = bs`), then `VTask.pi γ` is the constant path at `as` in the product space. That is, `(VTask.pi γ).extend t = as` for all `t`.

- Claim: The source of `VTask.pi γ` equals `as`, i.e., `(VTask.pi γ) 0 = as`.

- Claim: The target of `VTask.pi γ` equals `bs`, i.e., `(VTask.pi γ) 1 = bs`.

- Claim: For each index `i`, the composition of `VTask.pi γ` with the `i`-th projection equals `γ i` as a path, i.e., `fun t => (VTask.pi γ t) i = fun t => γ i t`.

### Boundaries

- At time `0`, the path evaluates to `as` (the starting point of the product), consistent with each component path starting at `as i`.
- At time `1`, the path evaluates to `bs` (the ending point of the product), consistent with each component path ending at `bs i`.
- When `ι` is empty, the product space is the unique one-point type `Π i : Empty, χ i`, and `VTask.pi γ` is the unique (constant) path in that space; the family `γ` is vacuously a family over the empty index set.
- When `ι` is infinite (e.g., `ι = ℕ`), the construction still works and yields a path in the countable product; continuity is guaranteed by the product topology.

### Not to be confused with

- `Path.prod` — the product of exactly two paths in `X × Y`; `VTask.pi` generalises this to an arbitrary (possibly infinite) family of spaces.
- `ContinuousMap.pi` — the analogous construction for continuous maps without prescribed endpoints; `VTask.pi` is specifically for paths (with the source/target conditions enforced).
- A pointwise product of the *underlying functions* without topological structure — `VTask.pi` produces a genuine `Path` with continuity and endpoint data, not merely a function `[0,1] → Π i, χ i`.
