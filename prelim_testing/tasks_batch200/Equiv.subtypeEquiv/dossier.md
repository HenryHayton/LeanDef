## Object

`VTask.subtypeEquiv` constructs an equivalence (a bijection with explicit inverse) between two subtype sets `{a : α // p a}` and `{b : β // q b}`, given an equivalence `e : α ≃ β` between the ambient types and a pointwise correspondence `h` between the predicates: for every `a : α`, `p a` holds if and only if `q (e a)` holds. Intuitively, if you can translate elements of `α` to elements of `β` (and back) while simultaneously respecting membership in the respective subsets, then the subsets themselves are in bijection.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.subtypeEquiv : {α : Sort u_1} -> {β : Sort u_4} -> {p : α → Prop} -> {q : β → Prop} -> (e : α ≃ β) -> (h : ∀ (a : α), p a ↔ q (e a)) -> { a // p a } ≃ { b // q b }
<!-- PINNED-SIGNATURE:END -->


`{α : Sort u_1} -> {β : Sort u_4} -> {p : α → Prop} -> {q : β → Prop} -> (e : α ≃ β) -> (h : ∀ (a : α), p a ↔ q (e a)) -> { a // p a } ≃ { b // q b }`

The implicit arguments `α` and `β` are the two ambient sorts (types or propositions). The implicit arguments `p` and `q` are the predicates carving out the subtypes on `α` and `β` respectively. The explicit argument `e` is the equivalence between `α` and `β`, supplying both a forward map and an inverse. The explicit argument `h` is a proof that, at each point `a : α`, the predicate `p` holds at `a` if and only if the predicate `q` holds at the image `e a`; this ensures that the forward map of `e` restricts to a well-typed map between the subtypes, and dually for the inverse.

## Conventions

No special junk-value or edge-case conventions are declared for this definition: the construction is total and well-defined whenever its inputs are provided, and no degenerate inputs produce underspecified or arbitrarily chosen outputs.

## Worked examples

- Claim: Applying `VTask.subtypeEquiv` with the identity equivalence on `ℕ` and the tautological pointwise iff yields the identity equivalence on `{n : ℕ // n > 0}`.

- Claim: For the equivalence `e : Fin 4 ≃ Fin 4` that is the identity, `VTask.subtypeEquiv e (fun a => Iff.rfl)` is the identity equivalence on `{i : Fin 4 // i.val < 2}`.

- Claim: If `e : α ≃ β` and `h : ∀ a, p a ↔ q (e a)`, then the forward function of `VTask.subtypeEquiv e h` sends a subtype element `⟨a, ha⟩` to `⟨e a, _⟩`, i.e., the underlying element is mapped by `e`.

- Claim: The inverse of `VTask.subtypeEquiv e h` is `VTask.subtypeEquiv e.symm` applied with the reversed pointwise iff; formally `(VTask.subtypeEquiv e h).symm = e.symm.subtypeEquiv (...)` (compatibility with `symm`).

- Claim: `VTask.subtypeEquiv` is compatible with composition: `(VTask.subtypeEquiv e h).trans (VTask.subtypeEquiv f h')` equals `VTask.subtypeEquiv (e.trans f) (...)` where the pointwise iff is chained.

## Boundaries

- When `e` is `Equiv.refl α` (the identity equivalence) and `h` is the trivial pointwise iff `fun _ => Iff.rfl`, the result is `Equiv.refl {a // p a}`, the identity equivalence on the subtype.
- When the predicates `p` and `q` are both `fun _ => True`, every element satisfies both, so the equivalence reduces to the equivalence between the full types `α` and `β` as witnessed by `e`.
- When the predicates are both `fun _ => False`, both subtypes are empty (`PEmpty`-like), and the resulting equivalence is the unique equivalence between two empty types.
- The construction is valid for arbitrary `Sort`s, not merely `Type`s, so it applies to subtypes of propositions (`Subtype` in `Prop`) as well as ordinary sets.
- The hypothesis `h` goes in one direction only (from `α` to `β`), but the inverse direction is recovered automatically by applying `h` at `e.symm b` and using the fact that `e (e.symm b) = b`.

## Not to be confused with

- `Equiv.subtypeEquivRight`: a special case where `α = β` and `e` is `Equiv.refl`; only the predicates differ, not the ambient type.
- `Perm.subtypePerm`: the restriction of a permutation `e : α ≃ α` to a subtype stable under `e`; same ambient type, with a stability condition rather than a general iff.
- `Equiv.subtypeEquivProp`: produces an equivalence between subtypes arising from a proof that the predicates are equal as functions, a strictly stronger hypothesis than a pointwise iff.