## Object

`VTask.cast` produces a canonical equivalence (a bijection with explicit inverse) between the "element types" of two equal multisets. Given multisets `s` and `t` over a type with decidable equality, and a proof that `s = t`, it constructs a term of type `s.ToType ≃ t.ToType`. Here `s.ToType` (written `Multiset.ToType s` in Mathlib) is the finite type whose elements represent the individual occurrences of elements in `s` — concretely, pairs `(a, i)` where `a : α` and `i` witnesses that the `i`-th copy of `a` belongs to `s`. Because `s` and `t` are literally equal, these element types are canonically identified.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.cast : {α : Type u_1} -> [DecidableEq α] -> {s t : Multiset α} -> (h : s = t) -> s.ToType ≃ t.ToType
<!-- PINNED-SIGNATURE:END -->


`VTask.cast : {α : Type u_1} -> [DecidableEq α] -> {s t : Multiset α} -> (h : s = t) -> s.ToType ≃ t.ToType`

The ambient type `α` is the element type of the multisets, inferred implicitly. The `DecidableEq α` instance is needed because membership and counting in multisets require decidable equality. The implicit arguments `s` and `t` are the two multisets being identified. The explicit argument `h` is the proof of equality `s = t`; it is the sole justification for the identification, and the resulting equivalence transports elements of `s.ToType` to elements of `t.ToType` along `h`.

## Conventions

There are no junk-value or default-output conventions to declare: the definition is total (every well-typed input produces a genuine equivalence) and there are no degenerate inputs producing unspecified or arbitrary outputs.

## Worked examples

- Claim: For any multiset `s`, `VTask.cast (rfl : s = s)` is the identity equivalence — it sends every element of `s.ToType` to itself.

- Claim: If `h : s = t` and `h' : t = u`, then `VTask.cast (h.trans h')` agrees with `(VTask.cast h).trans (VTask.cast h')` on every element of `s.ToType`.

- Claim: For any `h : s = t`, the forward function of `VTask.cast h` applied to an element `x : s.ToType` yields an element of `t.ToType` with the same underlying value `x.1 : α`.

- Claim: For any `h : s = t`, `(VTask.cast h).symm` equals `VTask.cast h.symm` up to the same underlying action on elements.

## Boundaries

- When `h` is `rfl` (i.e., `s` and `t` are definitionally identical), the equivalence is essentially the identity: both the forward and backward functions leave the underlying element and its membership witness unchanged.
- The type `s.ToType` is empty exactly when `s` is the empty multiset `0`; in that case `VTask.cast h` is the unique equivalence between two empty types, regardless of what `h` says.
- For a singleton multiset the type `s.ToType` has exactly one element, so `VTask.cast h` is again forced to be trivial.
- The definition is fully symmetric: `VTask.cast h` and `(VTask.cast h.symm)` are mutual inverses, reflecting that `≃` is itself symmetric.

## Not to be confused with

- `Equiv.cast` (the general universe-level `Equiv` built from a proof that two *types* are equal, via `congr`): `VTask.cast` works at the level of multiset equality and produces an equivalence between derived `ToType` types, not between arbitrary types.
- `Multiset.ToType` itself: that is the *type* of occurrences in a single multiset; `VTask.cast` is the *equivalence* between two such types when the multisets coincide.
- `Finset.orderIsoOfFin` or similar order-isomorphism constructions: those impose extra ordering structure, whereas `VTask.cast` is a plain bijection with no ordering guarantees.