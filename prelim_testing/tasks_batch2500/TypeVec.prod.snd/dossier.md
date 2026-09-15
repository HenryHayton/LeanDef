## Object

`VTask.snd` is the right-projection morphism for product type-vectors. Given an `n`-tuple of types formed by pairing two type-vectors `α` and `β` component-wise (i.e., the product `α.prod β`), `VTask.snd` is the natural "arrow" (component-wise family of functions) that, at each index `i : Fin2 n`, extracts the second component of the pair living at that position.

In other words, if `α ⊗ β` is the type-vector whose `i`-th component is `α i × β i`, then `VTask.snd` is the arrow `α ⊗ β ⟹ β` whose `i`-th component is the ordinary Cartesian `Prod.snd : α i × β i → β i`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.snd : {n : ℕ} -> {α β : TypeVec.{u} n} -> (α.prod β).Arrow β
<!-- PINNED-SIGNATURE:END -->


`VTask.snd : {n : ℕ} -> {α β : TypeVec.{u} n} -> (α.prod β).Arrow β`

The implicit argument `n` is the length (arity) of the type-vectors involved — the number of component types in each vector. The implicit arguments `α` and `β` are the two type-vectors of length `n` being paired: `α` supplies the left (first) components, and `β` supplies the right (second) components. The result is an arrow from the product `α ⊗ β` to `β`, i.e., a family of functions indexed by `Fin2 n`, each projecting onto the second component.

## Conventions

There are no junk-value or default-value conventions for this definition: it is a total, recursively well-defined morphism for every valid combination of `n`, `α`, and `β`, including `n = 0` (where `Fin2 0` is empty and the arrow is vacuously defined).

## Worked examples

- Claim: For a single-component product vector (n = 1), `VTask.snd` at the unique index `Fin2.fz` applied to a pair `(a, b)` returns `b`.

- Claim: Composing `VTask.snd` with the product arrow `f ⊗' g` (where `f : α ⟹ β` and `g : α' ⟹ β'`) equals `g` composed with `VTask.snd`; in symbols, `VTask.snd ⊚ (f ⊗' g) = g ⊚ VTask.snd`.

- Claim: Composing `VTask.snd` with the diagonal arrow `prod.diag : α ⟹ α ⊗ α` yields the identity: `VTask.snd ⊚ prod.diag = id`.

- Claim: At any index `i : Fin2 n`, for elements `a : α i` and `b : β i`, `VTask.snd i (prod.mk i a b) = b`.

## Boundaries

- When `n = 0`, the type `Fin2 0` is empty, so `VTask.snd` is the unique (vacuous) function from an empty domain; it is well-defined and poses no issues.
- When `n = 1`, the only index is `Fin2.fz`, and `VTask.snd` reduces to the standard binary `Prod.snd`.
- For larger `n`, the definition recurses through the `drop` operation (which removes the last component), applying the same projection at each level, so behavior at all indices is exactly ordinary `Prod.snd`.

## Not to be confused with

- `VTask.fst` (`TypeVec.prod.fst`): the symmetric left-projection arrow `α ⊗ β ⟹ α`, extracting the first component instead of the second.
- `Prod.snd` (the plain Cartesian projection): operates on a single pair type `A × B → B`, whereas `VTask.snd` is an arrow between type-vectors and acts component-wise at every index.
- `TypeVec.prod.mk`: the pairing arrow that *constructs* product type-vectors from two arrows `f : γ ⟹ α` and `g : γ ⟹ β`, as opposed to projecting out of one.