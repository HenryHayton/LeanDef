## Object

`VTask.cast` is a type equivalence (a bijection with explicit inverse) between two symmetric power types `Sym α n` and `Sym α m` whose lengths `n` and `m` are known to be equal. It reindexes a symmetric collection of exactly `n` elements of type `α` to one officially carrying length `m`, without changing the underlying multiset.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.cast : {α : Type u_1} -> {n m : ℕ} -> (h : n = m) -> Sym α n ≃ Sym α m
<!-- PINNED-SIGNATURE:END -->


`VTask.cast : {α : Type u_1} -> {n m : ℕ} -> (h : n = m) -> Sym α n ≃ Sym α m`

The type `α` is the element type, inferred implicitly. The natural numbers `n` and `m` are the source and target lengths, also implicit. The explicit argument `h` is a proof that `n = m`; it is the only piece of data needed to reindex. The result is a bundled equivalence `Sym α n ≃ Sym α m`, packaging both the forward map and its inverse.

## Conventions

The simp normal form pushes `VTask.cast` outward (towards the leaves of an expression) rather than inward, so rewriting with simp will bubble casts to the outside of compound expressions. When the equality proof is `rfl` (i.e., `n = n`), applying `VTask.cast` returns the original element unchanged.

## Worked examples

- Claim: For any `s : Sym α n`, the underlying multiset of `VTask.cast h s` equals the underlying multiset of `s` — the cast changes only the length annotation, not the data.

- Claim: Applying `VTask.cast rfl` to any `s : Sym α n` yields `s` itself, i.e., `VTask.cast rfl s = s`.

- Claim: Two consecutive casts compose: for `h : n = n'` and `h' : n' = n''`, we have `VTask.cast h' (VTask.cast h s) = VTask.cast (h.trans h') s`.

- Claim: Membership is preserved: `a ∈ VTask.cast h s ↔ a ∈ s` for any element `a`.

## Boundaries

- When `n = m` is `rfl`, the equivalence is the identity: both the forward and inverse maps return their input unchanged.
- The underlying multiset (the `val` field) is identical before and after the cast; only the length witness changes.
- The inverse of `VTask.cast h` is `VTask.cast h.symm`, and composing them in either order gives the identity.
- The function is well-defined for all types `α` and all natural numbers `n`, `m` with a proof of equality; there are no domain restrictions.

## Not to be confused with

- `Sym.equiv` or other `Sym`-level equivalences: those relate different element types or structural reformulations, not a length reindexing.
- `Fin.cast` / `Finset.cast`: analogous length-reindexing casts for finite index types or finite sets, not for symmetric powers.
- `Multiset.card_eq` proofs: a bare proof that two multisets have equal cardinality, which does not produce a bundled equivalence or reindex the type.