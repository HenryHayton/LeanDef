## Object

`VTask.piCongrRight` constructs an algebra equivalence between two Pi types `(∀ i, A₁ i) ≃ₐ[R] (∀ i, A₂ i)` from a family of algebra equivalences `∀ i, A₁ i ≃ₐ[R] A₂ i`. The resulting equivalence acts pointwise: applying it to a tuple `x` yields the tuple whose `i`-th component is the image of `x i` under the `i`-th component equivalence. It respects all the algebra structure (addition, multiplication, scalar multiplication by `R`, and the algebra unit map).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.piCongrRight : {R : Type u_3} -> {ι : Type u_4} -> {A₁ : ι → Type u_5} -> {A₂ : ι → Type u_6} -> [CommSemiring R] -> [(i : ι) → Semiring (A₁ i)] -> [(i : ι) → Semiring (A₂ i)] -> [(i : ι) → Algebra R (A₁ i)] -> [(i : ι) → Algebra R (A₂ i)] -> (e : (i : ι) → A₁ i ≃ₐ[R] A₂ i) -> ((i : ι) → A₁ i) ≃ₐ[R] (i : ι) → A₂ i
<!-- PINNED-SIGNATURE:END -->


`VTask.piCongrRight : {R : Type u_3} -> {ι : Type u_4} -> {A₁ : ι → Type u_5} -> {A₂ : ι → Type u_6} -> [CommSemiring R] -> [(i : ι) → Semiring (A₁ i)] -> [(i : ι) → Semiring (A₂ i)] -> [(i : ι) → Algebra R (A₁ i)] -> [(i : ι) → Algebra R (A₂ i)] -> (e : (i : ι) → A₁ i ≃ₐ[R] A₂ i) -> ((i : ι) → A₁ i) ≃ₐ[R] (i : ι) → A₂ i`

- `R` is the commutative semiring of scalars over which all algebras are defined.
- `ι` is the index type parametrising the family of algebras.
- `A₁` and `A₂` are families of types indexed by `ι`, each equipped pointwise with semiring and `R`-algebra structures (supplied via instance arguments).
- `e` is the family of algebra equivalences: for each index `i`, a two-sided inverse `R`-algebra isomorphism from `A₁ i` to `A₂ i`.

The output is a single `R`-algebra equivalence between the product algebra `∀ i, A₁ i` and the product algebra `∀ i, A₂ i`.

## Conventions

No special junk-value or edge-case conventions are declared for this definition: it is a total construction that produces a well-defined algebra equivalence for any valid inputs, including the empty index type and singleton index types.

## Worked examples

- Claim: When `ι` is `Fin 1` and each `A₁ i` and `A₂ i` is `ℤ` with the identity equivalence, `VTask.piCongrRight (fun _ => AlgEquiv.refl)` is the identity equivalence on `Fin 1 → ℤ`.

- Claim: The forward map of `VTask.piCongrRight e` applied to a tuple `x : ∀ i, A₁ i` yields the tuple whose `i`-th component equals `(e i) (x i)`. That is, for each `i : ι`, `(VTask.piCongrRight e) x i = e i (x i)`.

- Claim: The inverse of `VTask.piCongrRight e` is `VTask.piCongrRight (fun i => (e i).symm)`. In other words, taking the pointwise family of symms and lifting to a Pi equivalence gives the inverse.

- Claim: The underlying `Equiv` of `VTask.piCongrRight e` coincides with `Equiv.piCongrRight (fun i => (e i).toEquiv)`, meaning the two constructions agree on the level of bare bijections.

## Boundaries

- When `ι` is the empty type `Empty` (or `Fin 0`), the Pi types `∀ i, A₁ i` and `∀ i, A₂ i` are each the one-element type, and `VTask.piCongrRight e` is the unique algebra equivalence between them regardless of the (vacuous) family `e`.
- When `ι` is a singleton, `VTask.piCongrRight e` is essentially the single equivalence `e ⟨0, ...⟩` re-packaged as an equivalence of Pi types.
- The construction makes no finiteness assumption on `ι`; it works for countably or uncountably infinite index types.
- The algebraic identity `VTask.piCongrRight (fun i => AlgEquiv.refl) = AlgEquiv.refl` holds (the family of identity maps yields the identity on Pi types).

## Not to be confused with

- `Equiv.piCongrRight`: the analogous construction for bare equivalences of types, with no algebraic structure.
- `AlgEquiv.arrowCongr`: the non-dependent version, which constructs an algebra equivalence `(α → A₁) ≃ₐ[R] (α → A₂)` from a single equivalence `A₁ ≃ₐ[R] A₂`, rather than a pointwise family.
- `RingEquiv.piCongrRight`: the same pointwise-Pi construction but for ring equivalences only, without tracking the scalar `R`-algebra structure.
