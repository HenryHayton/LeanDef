## Object

Given a predicate `p` on a type `α` and a finitely supported function `f : α →₀ M`, `VTask.subtypeDomain p f` is the finitely supported function on the subtype `{a : α // p a}` obtained by restricting `f` to those elements of `α` satisfying `p`. The resulting function sends each `⟨a, ha⟩ : Subtype p` to the value `f a`, and its support consists precisely of those elements of `Subtype p` whose image in `α` belongs to the support of `f`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.subtypeDomain : {α : Type u_1} -> {M : Type u_5} -> [Zero M] -> (p : α → Prop) -> (f : α →₀ M) -> Subtype p →₀ M
<!-- PINNED-SIGNATURE:END -->


`VTask.subtypeDomain : {α : Type u_1} -> {M : Type u_5} -> [Zero M] -> (p : α → Prop) -> (f : α →₀ M) -> Subtype p →₀ M`

The type `α` is the index type of the original finitely supported function. The type `M` is the value type, which must carry a `Zero` instance so that finitely supported functions make sense (values are zero outside a finite support). The argument `p` is the predicate defining the subtype to which we restrict: only elements of `α` satisfying `p` are retained. The argument `f` is the original finitely supported function being restricted.

## Conventions

No junk-value or edge conventions are declared: the definition is total and well-behaved for all inputs, including the case where no element of `f`'s support satisfies `p` (yielding the zero function on `Subtype p`) and the case where `p` is identically true (yielding a function on `Subtype (fun _ => True)` isomorphic to `f` itself).

## Worked examples

- Claim: For the finitely supported function on `Fin 3` sending `0 ↦ 1, 1 ↦ 0, 2 ↦ 2`, restricting via `p = (· ≠ 1)` retains only the elements `0` and `2` in the support of the restricted function.

- Claim: If `f : α →₀ M` is the zero function (empty support), then `VTask.subtypeDomain p f` is also the zero function for any predicate `p`, since no element of the empty support can satisfy `p`.

- Claim: For a finitely supported function `f` and predicate `p` such that every element of `f.support` satisfies `p`, the support of `VTask.subtypeDomain p f` has the same cardinality as `f.support`.

- Claim: The value of `VTask.subtypeDomain p f` at a subtype element `⟨a, ha⟩` equals `f a`.

## Boundaries

- If the support of `f` is entirely disjoint from the subtype defined by `p` (no element of `f.support` satisfies `p`), then `VTask.subtypeDomain p f` has empty support and is the zero function on `Subtype p`.
- If `p` is the always-false predicate, the subtype is empty (`Subtype p` is an empty type), and the restricted function is vacuously defined on that empty domain.
- If `p` is the always-true predicate, every element of `α` satisfies `p`, and the restricted function on `Subtype (fun _ => True)` mirrors `f` exactly (up to the canonical equivalence `Subtype (fun _ => True) ≃ α`).
- The definition does not require `p` to be decidable at the point of use; decidability is introduced locally via `Classical.decPred` for the support computation.

## Not to be confused with

- `Finsupp.filter`: restricts the *values* of a finitely supported function by zeroing out those indices not satisfying a predicate, rather than changing the domain type to a subtype.
- `Finsupp.comapDomain`: pulls back a finitely supported function along an arbitrary map between index types, rather than restricting to a subtype of the original index type.
- `Finset.subtype`: restricts a *finite set* to a subtype, the analogous operation on the support alone without the function values.