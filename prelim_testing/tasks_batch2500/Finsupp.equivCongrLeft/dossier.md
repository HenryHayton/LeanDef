## Object

`VTask.equivCongrLeft f` is the canonical bijection between two spaces of finitely-supported functions that arises by relabelling the domain index set. Given an equivalence `f : α ≃ β`, it produces an equivalence `(α →₀ M) ≃ (β →₀ M)`: the forward direction reindexes a finitely-supported function on `α` along `f` to get one on `β`, and the inverse direction reindexes along `f.symm`. This is the finitely-supported analogue of the classical change-of-variables bijection between dependent-function spaces `(∀ a : α, M) ≃ (∀ b : β, M)` induced by a type equivalence.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.equivCongrLeft : {α : Type u_1} -> {β : Type u_2} -> {M : Type u_5} -> [Zero M] -> (f : α ≃ β) -> (α →₀ M) ≃ (β →₀ M)
<!-- PINNED-SIGNATURE:END -->


`VTask.equivCongrLeft : {α : Type u_1} -> {β : Type u_2} -> {M : Type u_5} -> [Zero M] -> (f : α ≃ β) -> (α →₀ M) ≃ (β →₀ M)`

The implicit type arguments `α` and `β` are the source and target index types, and `M` is the value type. The `Zero M` instance is required because finitely-supported functions need a chosen zero value so that "finite support" is well-defined. The explicit argument `f` is the type equivalence used to relabel indices.

## Conventions

No junk-value or edge conventions are declared: the definition is total over all type equivalences and all zero-equipped value types, and every finitely-supported function has a well-defined image under the relabelling.

## Worked examples

- Claim: Applying `VTask.equivCongrLeft f` to a finitely-supported function `l : α →₀ M` equals `equivMapDomain f l`, i.e., the forward map is exactly domain-relabelling by `f`.

- Claim: The inverse of `VTask.equivCongrLeft f` is `VTask.equivCongrLeft f.symm`, meaning symmetry is obtained by flipping the underlying equivalence rather than constructing a fresh one.

- Claim: If `f : Fin 2 ≃ Fin 2` is the identity equivalence, then `VTask.equivCongrLeft f` acts as the identity on `(Fin 2 →₀ ℕ)`, sending every finitely-supported function to itself.

- Claim: For any `φ : α →₀ M` and `b : β`, the value of `(VTask.equivCongrLeft f φ) b` equals `φ (f.symm b)`, reflecting that the support is carried over and values at relabelled points match via the inverse of `f`.

## Boundaries

- When `f` is the identity equivalence `Equiv.refl α`, the resulting equivalence `VTask.equivCongrLeft (Equiv.refl α)` is the identity on `(α →₀ M)`.
- The construction requires only a `Zero` instance on `M`, not any algebraic structure; the equivalence is purely set-theoretic/type-theoretic and does not depend on `M` being a group or module.
- Composition of two relabellings respects transitivity: `VTask.equivCongrLeft (f.trans g)` coincides with the composition of `VTask.equivCongrLeft f` followed by `VTask.equivCongrLeft g`.
- The definition is well-defined for any finite or infinite types `α`, `β`; the finiteness lives inside the finitely-supported functions themselves, not in `α` or `β`.

## Not to be confused with

- `Finsupp.equivMapDomain f` — this is the bare function `(α →₀ M) → (β →₀ M)` (the forward direction only), not packaged as a two-sided equivalence.
- `Finsupp.domCongr` — a related but distinct operation that changes the domain of a finsupp via a `MulEquiv` or `AddEquiv` in an algebraic context, rather than a plain type equivalence.
- `Equiv.piCongrLeft` — the analogous equivalence for *all* functions `(α → M) ≃ (β → M)`, without the finitely-supported restriction; there is no zero requirement there.