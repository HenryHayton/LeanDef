## Object

`VTask.insert` is a canonical equivalence (bijection) of types between the subtype `↑(insert a s)` — the set obtained by inserting element `a` into set `s`, viewed as a type — and the disjoint-sum type `↑s ⊕ PUnit`. Informally, it says: if `a` is genuinely new (not already in `s`), then the enlarged set `insert a s` has exactly one more element than `s`, and that extra element corresponds to the unique inhabitant of `PUnit`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.insert : {α : Type u} -> {s : Set α} -> [DecidablePred fun x => x ∈ s] -> {a : α} -> (H : a ∉ s) -> ↑(insert a s) ≃ ↑s ⊕ PUnit.{u + 1}
<!-- PINNED-SIGNATURE:END -->


`{α : Type u} -> {s : Set α} -> [DecidablePred fun x => x ∈ s] -> {a : α} -> (H : a ∉ s) -> ↑(insert a s) ≃ ↑s ⊕ PUnit.{u + 1}`

- `α` is the ambient type whose elements populate the sets.
- `s` is the base set, a `Set α`.
- The `DecidablePred` instance makes membership in `s` decidable, which is needed to route elements to the correct summand.
- `a` is the element being inserted.
- `H` is the proof that `a` does not already belong to `s`; this hypothesis is essential — without it the inserted set would not gain a fresh element and the decomposition would not hold.

The result is a bundled equivalence (an `Equiv`) between the subtype corresponding to `insert a s` and `↑s ⊕ PUnit`.

## Conventions

No junk-value conventions are declared: the definition is only well-typed when the hypothesis `H : a ∉ s` is explicitly supplied, so there is no meaningful "out-of-domain" input case to assign a junk value to.

## Worked examples

- Claim: For `s = ∅` and `a = (0 : ℕ)`, the equivalence `VTask.insert (show (0 : ℕ) ∉ (∅ : Set ℕ) from Set.not_mem_empty 0)` maps the unique element of `↑(insert 0 ∅)` that equals `0` to the right summand `Sum.inr PUnit.unit`, since `0 ∉ ∅` so it is the "new" element corresponding to `PUnit`.

- Claim: For `s = {1, 2}` and `a = 0` (with `0 ∉ {1, 2}`), the forward map sends any element `x : ↑(insert 0 {1, 2})` with `x.val ≠ 0` (i.e. `x.val ∈ {1, 2}`) to the left summand `Sum.inl`, wrapping `x` as an element of `↑{1, 2}`; and it sends the element with value `0` to `Sum.inr PUnit.unit`.

- Claim: The inverse of `VTask.insert H` sends `Sum.inl ⟨x, hx⟩` (an element already in `s`) to `⟨x, Set.mem_insert_of_mem a hx⟩` in `↑(insert a s)`, and sends `Sum.inr PUnit.unit` to `⟨a, Set.mem_insert a s⟩`.

- Claim: When `s` is a `Finset` (viewed as a `Set`) with `n` elements and `a ∉ s`, the equivalence witnesses that `insert a s` has cardinality `n + 1`, since `↑s ⊕ PUnit` has exactly one more element than `↑s`.

## Boundaries

- The hypothesis `H : a ∉ s` is **required** to form the term at all; there is no version of this equivalence defined when `a ∈ s` (in that case `insert a s = s` and no `PUnit` summand should appear).
- When `s = ∅`, the result specialises to an equivalence `↑{a} ≃ PUnit`, consistent with the singleton equivalence.
- The universe level of `PUnit` is `u + 1`, matching the universe level of `α : Type u`, so there is no universe inconsistency.
- The equivalence is **not** symmetric in `s` and `{a}`: the left summand is always `↑s` and the right is always `PUnit` (representing `{a}`).

## Not to be confused with

- `Equiv.Set.union`: the equivalence for a general disjoint union `↑(s ∪ t) ≃ ↑s ⊕ ↑t`; `VTask.insert` is a specialisation where `t = {a}` and `{a} ≃ PUnit`.
- `Equiv.Set.singleton`: the equivalence `↑{a} ≃ PUnit` for a single-element set; `VTask.insert` uses this as a component but also incorporates the base set `s`.
- `Finset.insertEquiv` or cardinality lemmas about `Finset.insert`: those operate on `Finset` rather than `Set` subtypes and produce combinatorial cardinality equalities, not type-level equivalences.