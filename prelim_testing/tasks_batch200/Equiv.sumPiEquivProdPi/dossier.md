## VTask.sumPiEquivProdPi

### Object

This is the canonical type equivalence that "splits" a dependent function over a sum index type into a pair of dependent functions, one over each summand. More precisely, given a family of types indexed by a disjoint union `ι ⊕ ι'`, the type of dependent functions `(i : ι ⊕ ι') → π i` is in natural bijection with the product `((i : ι) → π (Sum.inl i)) × ((i' : ι') → π (Sum.inr i'))`. This is the dependent-type generalization of the fact that a function out of a disjoint union is the same as a pair of functions, one from each component.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sumPiEquivProdPi : {ι : Type u_10} -> {ι' : Type u_11} -> (π : ι ⊕ ι' → Type u_9) -> ((i : ι ⊕ ι') → π i) ≃ ((i : ι) → π (Sum.inl i)) × ((i' : ι') → π (Sum.inr i'))
<!-- PINNED-SIGNATURE:END -->


`VTask.sumPiEquivProdPi : {ι : Type u_10} -> {ι' : Type u_11} -> (π : ι ⊕ ι' → Type u_9) -> ((i : ι ⊕ ι') → π i) ≃ ((i : ι) → π (Sum.inl i)) × ((i' : ι') → π (Sum.inr i'))`

The first implicit argument `ι` is the left index type of the sum. The second implicit argument `ι'` is the right index type of the sum. The explicit argument `π` is the dependent type family indexed over `ι ⊕ ι'`, assigning to each element of the sum a type; it determines both the domain of dependent functions and the fibers on each summand.

### Conventions

There are no junk-value or edge conventions: the equivalence is defined for all choices of `ι`, `ι'`, and `π`, including the cases where one or both of the index types is empty, in which case the corresponding factor becomes a function type from an empty type (which is a unit type). No special sentinel values or out-of-domain behaviors are involved.

### Worked examples

- Claim: For the constant family `π _ = ℕ`, applying `VTask.sumPiEquivProdPi` to the function `Sum.rec (fun _ => 1) (fun _ => 2)` (where `ι = Unit` and `ι' = Unit`) yields the pair `(fun _ => 1, fun _ => 2)`.

- Claim: For any `π` and any `f : (i : ι ⊕ ι') → π i`, the forward map sends `f` to the pair whose first component is `f ∘ Sum.inl` and whose second component is `f ∘ Sum.inr`.

- Claim: The equivalence `VTask.sumPiEquivProdPi π` is its own inverse in the sense that applying the forward map and then the inverse map recovers the original dependent function definitionally (the left inverse law holds).

- Claim: For the empty index type `ι = Empty`, `VTask.sumPiEquivProdPi π` gives an equivalence between `(i : Empty ⊕ ι') → π i` and `(fun _ => PUnit.unit) × ((i' : ι') → π (Sum.inr i'))` up to the canonical isomorphism, illustrating that the left component collapses to a trivial type.

### Boundaries

- When `ι` is the empty type, the left component of the product is `(i : Empty) → π (Sum.inl i)`, which is a type with exactly one element (vacuous function). The equivalence still holds without any special casing.
- When `ι'` is the empty type, the right component is `(i' : Empty) → π (Sum.inr i')`, again a singleton, and the equivalence holds symmetrically.
- When both `ι` and `ι'` are empty, the full function type is also a singleton (the unique function from `Empty ⊕ Empty ≅ Empty`), and the product of two singletons is again a singleton; the equivalence is still valid.
- The equivalence is definitionally invertible: the round-trip in both directions is definitionally equal to the identity, not just propositionally.

### Not to be confused with

- `Equiv.sumArrowEquivProdArrow`: The non-dependent version of this equivalence, where `π` is a constant family `fun _ => α`; `VTask.sumPiEquivProdPi` strictly generalizes it.
- `Equiv.piEquivPiSubtypeProd`: A different splitting of a pi type, decomposing over a subtype/complement partition of the index rather than a sum-type index.
- `Equiv.prodEquiv` or `Equiv.sigmaPiEquiv`: Equivalences involving sigma types or products of pi types in a different structural way, not arising from splitting over a sum index.
