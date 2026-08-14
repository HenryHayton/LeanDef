## VTask.subtypePerm

### Object

Given a permutation `f` of a type `α` and a proof that `f` preserves a predicate `p` (i.e., `f` maps every element satisfying `p` to another element satisfying `p`, and vice versa), `VTask.subtypePerm f h` is the permutation of the subtype `{x : α // p x}` induced by `f`. In other words, it is the restriction of `f` to the `p`-subtype, which is well-defined precisely because `f` fixes that subtype setwise.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.subtypePerm : {α : Type u_4} -> {p : α → Prop} -> (f : Equiv.Perm α) -> (h : ∀ (x : α), p (f x) ↔ p x) -> Equiv.Perm { x // p x }
<!-- PINNED-SIGNATURE:END -->


`VTask.subtypePerm : {α : Type u_4} -> {p : α → Prop} -> (f : Equiv.Perm α) -> (h : ∀ (x : α), p (f x) ↔ p x) -> Equiv.Perm { x // p x }`

The implicit argument `α` is the ambient type being permuted. The implicit argument `p` is the predicate that carves out the subtype to be preserved. The argument `f` is the permutation of the full type `α` that one wishes to restrict. The argument `h` is the proof that `f` preserves the predicate `p`: for every element `x : α`, `p (f x)` holds if and only if `p x` holds, ensuring the subtype is invariant under `f` (and hence also under `f⁻¹`).

### Conventions

There are no junk-value conventions to declare: the definition is total, requires explicit proof of invariance, and has no degenerate inputs.

### Worked examples

- Claim: For the identity permutation `1 : Equiv.Perm α`, `VTask.subtypePerm 1 (fun _ => Iff.rfl)` equals the identity permutation on `{x // p x}`.

- Claim: If `f : Equiv.Perm α` preserves `p` via `h`, then for any `x : {x // p x}`, applying `VTask.subtypePerm f h` to `x` yields the subtype element `⟨f x, (h _).2 x.2⟩`.

- Claim: If `f : Equiv.Perm α` preserves `p` via `hf`, and `g : Equiv.Perm α` preserves `p` via `hg`, and `h` is the proof that their composition `g ∘ f` also preserves `p`, then `VTask.subtypePerm (g * f) h` equals `VTask.subtypePerm g hg * VTask.subtypePerm f hf` as permutations of `{x // p x}`.

- Claim: If `f : Equiv.Perm α` preserves `p` via `hf`, then the inverse of `VTask.subtypePerm f hf` in `Equiv.Perm {x // p x}` equals `VTask.subtypePerm f⁻¹ hf'`, where `hf'` is the companion proof that `f⁻¹` also preserves `p`.

### Boundaries

- If `p` is the predicate `fun _ => True`, the subtype is essentially all of `α`, and `VTask.subtypePerm f h` is (up to the trivial coercion) the original permutation `f`.
- If `p` is the predicate `fun _ => False`, the subtype is empty, and `VTask.subtypePerm f h` is the unique permutation of the empty type.
- The hypothesis `h` must be an iff (both directions), not merely an implication in one direction; this ensures that `f⁻¹` also preserves `p`, which is required to construct the inverse of the output permutation.
- When `f` is the identity permutation, the hypothesis `h` is trivially `fun _ => Iff.rfl`, and the result is the identity on the subtype.
- The `n`-th power `(VTask.subtypePerm f hf)^n` equals `VTask.subtypePerm (f^n) h'` for the appropriate proof `h'` that `f^n` preserves `p`.

### Not to be confused with

- `Equiv.Perm.ofSubtype`: Embeds a permutation of a subtype `{x // p x}` back into a permutation of the full type `α` by extending it by the identity outside the subtype — this goes in the opposite direction from `VTask.subtypePerm`.
- `Equiv.subtypeEquiv`: A general equivalence between two subtypes induced by a bijection between ambient types, not specifically a restriction of a permutation to an invariant subtype.
- `Equiv.Perm.subtypePermOfSupport`: A closely related construction specific to the support of a permutation, rather than a general predicate `p`.