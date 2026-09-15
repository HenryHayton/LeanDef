## VTask.liftAddHom

### Object

`VTask.liftAddHom` is an isomorphism of additive monoids between two kinds of "multilinear-like" data:
- A family of additive monoid homomorphisms, one from each fibre `β i` to a common target `γ`, and
- A single additive monoid homomorphism from the direct sum `Π₀ i, β i` (the type of finitely-supported dependent functions, also called `DFinsupp`) to `γ`.

The isomorphism says that giving an additive monoid hom out of the direct sum is *exactly the same data* as giving a compatible family of additive monoid homs out of each summand — and this correspondence itself respects the additive structure on the hom-sets.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.liftAddHom : {ι : Type u} -> {γ : Type w} -> {β : ι → Type v} -> [DecidableEq ι] -> [(i : ι) → AddZeroClass (β i)] -> [AddCommMonoid γ] -> ((i : ι) → β i →+ γ) ≃+ ((Π₀ (i : ι), β i) →+ γ)
<!-- PINNED-SIGNATURE:END -->


`VTask.liftAddHom : {ι : Type u} -> {γ : Type w} -> {β : ι → Type v} -> [DecidableEq ι] -> [(i : ι) → AddZeroClass (β i)] -> [AddCommMonoid γ] -> ((i : ι) → β i →+ γ) ≃+ ((Π₀ (i : ι), β i) →+ γ)`

- `ι` is the index type ranging over the summands; it is implicit.
- `γ` is the common target additive commutative monoid; it is implicit.
- `β` is the family of types, one for each index in `ι`, forming the fibres of the direct sum; it is implicit.
- The `DecidableEq ι` instance is needed to work with elements of the direct sum, which have finite support indexed by `ι`.
- The `(i : ι) → AddZeroClass (β i)` instance equips each fibre with an additive zero-class structure.
- The `AddCommMonoid γ` instance equips the target with its additive commutative monoid structure.
- The result is a specific additive equivalence (an `AddEquiv` that is also an `AddMonoidHom` isomorphism) between the two hom-types, taking a family of homs to the unique hom from the direct sum that restricts to each family member on the corresponding summand.

### Conventions

No junk-value or edge conventions are declared for this definition: it is a total isomorphism between two well-formed algebraic structures, and every valid input (a family of additive monoid homs) yields a well-defined additive monoid hom out of the direct sum, with no degenerate or boundary cases to specify.

### Worked examples

- Claim: For the trivial family `β i = ℤ` indexed by `Fin 2` with both component homs being the identity, `VTask.liftAddHom` sends this family to the hom from `Π₀ i : Fin 2, ℤ` that sums all components.

- Claim: Applying `VTask.liftAddHom` to the family of inclusion maps `β i →+ ⊕ β i` (the canonical injections into the direct sum) yields the identity homomorphism on `Π₀ i, β i`.

- Claim: The inverse of `VTask.liftAddHom` applied to an additive monoid hom `F : (Π₀ i, β i) →+ γ` recovers the family of homs given by precomposing `F` with each single-element inclusion `β i →+ Π₀ i, β i`.

- Claim: `VTask.liftAddHom` preserves addition: for two families `F` and `G`, `VTask.liftAddHom (F + G) = VTask.liftAddHom F + VTask.liftAddHom G`.

### Boundaries

- When `ι` is empty, `Π₀ i, β i` has a single element (the zero function), and the only additive monoid hom from it to `γ` is the zero hom. Correspondingly, the only family of homs indexed by an empty type is the empty family. The isomorphism holds trivially.
- When `ι` is a singleton `{i₀}`, the direct sum `Π₀ i, β i` is isomorphic to `β i₀`, and `VTask.liftAddHom` reduces to the bijection between homs out of `β i₀` and homs out of its one-element direct sum.
- The definition is stated for `AddCommMonoid γ` as the target; commutativity is needed to ensure the summation over the finite support is well-defined and independent of order.
- The fibres `β i` need only be `AddZeroClass` (they do not need to be commutative or even full monoids), which is the minimal structure for additive monoid homs from them to make sense.

### Not to be confused with

- `Finsupp.liftAddHom`: the analogous isomorphism for `Finsupp` (finitely-supported functions into a *fixed* type `M`), rather than `DFinsupp` (finitely-supported dependent functions into a *family* of types `β i`).
- `DFinsupp.sumAddHom`: the forward direction of `VTask.liftAddHom` as a bare function (not packaged as an additive equivalence); `VTask.liftAddHom` is the bundled, invertible version.
- `DFinsupp.liftEquiv`: a related construction that lifts multiplicative or other algebraic structure, not the additive-monoid-hom version.