## VTask.sigmaLift

### Object

Given a family of binary functions `f` that, for each index `i`, maps a pair of fibre-elements `α i` and `β i` to a finite set of `γ i`-elements, `VTask.sigmaLift f a b` lifts this family to a single binary function on dependent-pair (sigma) types. It takes two sigma-typed inputs — one from `Σ i, α i` and one from `Σ i, β i` — and returns a finite set of elements of `Σ i, γ i`. The result is non-empty only when the two inputs share the same index, in which case it applies `f` at that common index and packages every result back as a sigma element tagged with that index. If the two inputs have different indices, the result is the empty finset.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sigmaLift : {ι : Type u_1} -> {α : ι → Type u_2} -> {β : ι → Type u_3} -> {γ : ι → Type u_4} -> [DecidableEq ι] -> (f : ⦃i : ι⦄ → α i → β i → Finset (γ i)) -> (a : Sigma α) -> (b : Sigma β) -> Finset (Sigma γ)
<!-- PINNED-SIGNATURE:END -->


`VTask.sigmaLift : {ι : Type u_1} -> {α : ι → Type u_2} -> {β : ι → Type u_3} -> {γ : ι → Type u_4} -> [DecidableEq ι] -> (f : ⦃i : ι⦄ → α i → β i → Finset (γ i)) -> (a : Sigma α) -> (b : Sigma β) -> Finset (Sigma γ)`

- `ι` is the shared index type that parametrises all the fibres.
- `α`, `β`, `γ` are type families over `ι`, providing the fibre types for the two inputs and the output, respectively.
- The `DecidableEq ι` instance is needed so that equality of indices can be decided computably.
- `f` is the family of fibre-wise binary operations: for each index `i`, it maps a value in `α i` and a value in `β i` to a finite set of `γ i` values.
- `a` is the first sigma-typed argument, i.e., a dependent pair whose first component is an index in `ι` and whose second component lives in the corresponding fibre of `α`.
- `b` is the second sigma-typed argument, a dependent pair in `Σ i, β i`.

### Conventions

When the index of `a` differs from the index of `b`, the result is defined to be the empty finset; there is no partial-function or error signal — the function is total and returns `∅` in that case.

### Worked examples

- Claim: For `a = ⟨i, x⟩` and `b = ⟨i, y⟩` sharing the same index `i`, the element `⟨i, z⟩` belongs to `VTask.sigmaLift f a b` if and only if `z ∈ f x y`. In other words, the lift is transparent at matching indices.

- Claim: For `a = ⟨i, x⟩` and `b = ⟨j, y⟩` with `i ≠ j`, the result `VTask.sigmaLift f a b` is the empty finset, regardless of `f`, `x`, and `y`.

- Claim: The cardinality of `VTask.sigmaLift f a b` equals `(f (h ▸ a.2) b.2).card` when `h : a.1 = b.1`, and equals `0` when `a.1 ≠ b.1`.

- Claim: If `f a_val b_val ⊆ g a_val b_val` for every fibre and every pair of inputs, then `VTask.sigmaLift f a b ⊆ VTask.sigmaLift g a b` for every sigma pair `a`, `b`.

### Boundaries

- **Unequal indices**: When `a.1 ≠ b.1`, the output is always `∅`, even if `f` would produce a non-empty set at some compatible fibre.
- **Equal indices**: When `a.1 = b.1`, the result is exactly the image of `f` applied to the fibres, re-tagged with the common index. No fibre elements from other indices appear.
- **Membership test**: An element `x : Σ i, γ i` belongs to the result only when `a.1 = x.1`, `b.1 = x.1`, and `x.2` belongs to `f` applied to the appropriately coerced second components of `a` and `b`.
- **Empty `f`**: If `f` returns `∅` at the relevant fibre even when indices match, the overall result is `∅`.

### Not to be confused with

- `Finset.sigma` (or `Finset.sigmaFinset`): constructs a finset of sigma-pairs from an index finset and a family of fibre finsets, not a lifted binary operation.
- `Sigma.map`: a function-level map on sigma types that transforms each component, rather than a finset-valued binary lift.
- `Finset.product` or `Finset.pi`: forms Cartesian products of finsets across fibres, not a fibre-wise conditional lift.
