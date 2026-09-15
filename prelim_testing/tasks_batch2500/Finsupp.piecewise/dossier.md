## Object

`VTask.piecewise f g` constructs a finitely supported function on `α` by gluing together two finitely supported functions: `f`, which lives on the subtype `{a : α // P a}` of elements satisfying a predicate, and `g`, which lives on the complementary subtype `{a : α // ¬P a}`. At each point `a : α`, the value is taken from `f` if `P a` holds, and from `g` otherwise. The result has finite support because both `f` and `g` individually have finite support.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.piecewise : {α : Type u_1} -> {M : Type u_12} -> [Zero M] -> {P : α → Prop} -> [DecidablePred P] -> (f : Subtype P →₀ M) -> (g : { a // ¬P a } →₀ M) -> α →₀ M
<!-- PINNED-SIGNATURE:END -->


`VTask.piecewise : {α : Type u_1} -> {M : Type u_12} -> [Zero M] -> {P : α → Prop} -> [DecidablePred P] -> (f : Subtype P →₀ M) -> (g : { a // ¬P a } →₀ M) -> α →₀ M`

- `α` is the ambient type on which the combined finitely supported function is defined.
- `M` is the codomain type, which must carry a distinguished zero element (used to define finite support).
- The `Zero M` instance supplies the zero used to identify elements of finite support.
- `P` is the predicate that partitions `α` into two complementary subtypes.
- The `DecidablePred P` instance allows case-splitting on `P a` computably.
- `f` is the finitely supported function on the subtype where `P` holds; it supplies values at points satisfying `P`.
- `g` is the finitely supported function on the complementary subtype where `P` fails; it supplies values at points not satisfying `P`.

## Conventions

The support of the result is exactly the disjoint union of the images of the supports of `f` and `g` under the respective subtype inclusion embeddings into `α`; there are no junk values or edge conventions beyond what is forced by the finitely supported function structure.

## Worked examples

- Claim: For `f : {n : Fin 5 // n.val < 3} →₀ ℕ` and `g : {n : Fin 5 // ¬(n.val < 3)} →₀ ℕ`, evaluating `VTask.piecewise f g` at a point `a` with `P a` gives `f ⟨a, h⟩`.

- Claim: Restricting `VTask.piecewise f g` back to the subtype `{a // P a}` via `subtypeDomain` recovers `f` exactly.

- Claim: Restricting `VTask.piecewise f g` back to the complementary subtype `{a // ¬P a}` via `subtypeDomain` recovers `g` exactly.

- Claim: If both `f` and `g` are the zero finsupp, then `VTask.piecewise f g` is the zero finsupp on `α`.

## Boundaries

- If `f = 0` and `g = 0`, the result is the zero finitely supported function on `α`, with empty support.
- If `P` holds for every element of `α` (i.e., the `¬P` subtype is empty), then `g` must be zero and the result is entirely determined by `f`; symmetrically, if `P` holds nowhere, the result is entirely determined by `g`.
- The supports of `f` and `g` map into disjoint parts of `α` (elements satisfying `P` vs. those not satisfying `P`), so the support of the result is the disjoint union of the two mapped supports with no overlap.
- There is no restriction on the size or shape of `f` and `g` individually; both can have support of any finite cardinality up to the size of their respective subtypes.

## Not to be confused with

- `Finsupp.subtypeDomain`: this is a *restriction* of a finsupp on `α` to a subtype, going in the opposite direction from `VTask.piecewise`.
- `Finsupp.comapDomain`: this maps a finsupp along a function into the index type, which is a reindexing rather than a predicate-based gluing.
- `Set.piecewise` (for ordinary functions): the analogous construction for plain functions `α → M` without any finiteness constraint on the support.