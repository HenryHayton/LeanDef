## VTask.sigma

### Object

`VTask.sigma s t` is the **indexed sum** (or **dependent-pair set**) formed from a set `s` of indices and an index-dependent family `t` of fibre sets. It collects all dependent pairs `⟨i, a⟩` in the sigma-type `Σ i, α i` such that the index `i` belongs to `s` and the value `a` belongs to the fibre set `t i`. It is the set-theoretic analogue of the disjoint union of the family `{t i | i ∈ s}`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sigma : {ι : Type u_1} -> {α : ι → Type u_3} -> (s : Set ι) -> (t : (i : ι) → Set (α i)) -> Set ((i : ι) × α i)
<!-- PINNED-SIGNATURE:END -->


`VTask.sigma : {ι : Type u_1} -> {α : ι → Type u_3} -> (s : Set ι) -> (t : (i : ι) → Set (α i)) -> Set ((i : ι) × α i)`

The implicit argument `ι` is the index type. The implicit argument `α` is a type family indexed by `ι`, so `α i` is the fibre over each index `i`. The explicit argument `s` is the set of permitted indices. The explicit argument `t` assigns to each index `i : ι` a set `t i ⊆ α i`, which is the permitted fibre over that index.

### Conventions

There are no junk-value or out-of-domain conventions to declare: the definition is total over all choices of `s` and `t`, including empty sets and universe-level sets, and every combination yields a well-defined set of dependent pairs without any special sentinel behaviour.

### Worked examples

- Claim: A dependent pair `⟨i, a⟩` belongs to `VTask.sigma s t` if and only if `i ∈ s` and `a ∈ t i`.

- Claim: `VTask.sigma ∅ t = ∅` — when the index set is empty, no pair can have its index in `s`, so the sigma set is empty.

- Claim: `VTask.sigma s (fun _ => ∅) = ∅` — when every fibre set is empty, no pair can satisfy the second condition, so the sigma set is empty regardless of `s`.

- Claim: `VTask.sigma Set.univ t = Set.univ` when each `t i = Set.univ` — every dependent pair qualifies when both the index set and all fibre sets are universal.

- Claim: `VTask.sigma {i} t = Sigma.mk i '' t i` — the sigma set over a singleton index is exactly the image of the fibre `t i` under the constructor `Sigma.mk i`.

- Claim: The first-projection image of `VTask.sigma s t` equals `s` whenever every fibre `t i` is nonempty; more precisely, `Sigma.fst '' (VTask.sigma s t) = s` under those conditions.

### Boundaries

- If `s = ∅`, the result is `∅` regardless of `t`.
- If any fibre `t i = ∅` for all `i ∈ s`, the result is `∅`.
- If `s = Set.univ` and every `t i = Set.univ`, the result is `Set.univ` (the whole sigma type).
- The fibre sets `t i` for indices `i ∉ s` do not affect the result at all; they appear in the family `t` but no pair with such an index can qualify.
- The preimage `Sigma.mk i ⁻¹' (VTask.sigma s t)` equals `t i` when `i ∈ s`, and equals `∅` when `i ∉ s`.
- `VTask.sigma s t` is nonempty if and only if `s` is nonempty and there exists some `i ∈ s` with `t i` nonempty.

### Not to be confused with

- `Set.pi`: also constructs a set of indexed tuples from a family of sets, but collects *functions* `(i : ι) → α i` rather than a single dependent pair; it is a product rather than a sum.
- `Set.iUnion (fun i => Sigma.mk i '' t i)`: the unrestricted union over all indices, which equals `VTask.sigma Set.univ t`; omitting the index restriction `i ∈ s` gives the full sigma set.
- `Sigma.map`: a function-level operation that maps a sigma-type to another sigma-type via index and fibre maps, not a set constructor.
