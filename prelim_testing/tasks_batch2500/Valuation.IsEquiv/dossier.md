## VTask.IsEquiv

### Object

Given a commutative ring `R` and two valuations on it, possibly taking values in different totally ordered commutative monoids with zero, `VTask.IsEquiv v₁ v₂` is the proposition that `v₁` and `v₂` are *equivalent valuations*: they induce exactly the same preorder on `R`. Concretely, for every pair of elements `r, s` of `R`, `v₁ r ≤ v₁ s` if and only if `v₂ r ≤ v₂ s`.

Equivalent valuations need not take values in the same ordered monoid, nor need they agree numerically; they merely encode the same ordering information on ring elements.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsEquiv : {R : Type u_3} -> {Γ₀ : Type u_4} -> {Γ'₀ : Type u_5} -> [Ring R] -> [LinearOrderedCommMonoidWithZero Γ₀] -> [LinearOrderedCommMonoidWithZero Γ'₀] -> (v₁ : Valuation R Γ₀) -> (v₂ : Valuation R Γ'₀) -> Prop
<!-- PINNED-SIGNATURE:END -->


The implicit argument `R` is the underlying ring being valued. The implicit arguments `Γ₀` and `Γ'₀` are the target ordered monoids (with zero) in which `v₁` and `v₂` respectively take their values; these two value groups are allowed to differ. The instance arguments supply the ring structure on `R` and the linear ordered commutative monoid-with-zero structures on the two value groups. The explicit argument `v₁` is the first valuation on `R`, and `v₂` is the second valuation on `R`, with which `v₁` is being compared.

### Conventions

No junk-value or edge conventions are declared: the predicate is a universally quantified biconditional with no special treatment at any particular inputs; it is defined uniformly for all `r, s : R`.

### Worked examples

- Claim: Every valuation `v` is equivalent to itself, i.e., `VTask.IsEquiv v v` holds.

- Claim: If `v` and `v'` are valuations with `VTask.IsEquiv v v'`, then `VTask.IsEquiv v' v` also holds (the relation is symmetric).

- Claim: Two equivalent valuations `v` and `v'` satisfy `v x ≤ 1 ↔ v' x ≤ 1` for every `x : R`, characterizing equivalence in terms of the valuation ring.

- Claim: If `f : Γ₀ →*₀ Γ'₀` is a strictly monotone monoid-with-zero homomorphism, then `v.map f` is equivalent to `v` (composing with a strictly monotone map does not change the induced preorder).

### Boundaries

- The two valuations being compared may take values in *different* ordered monoids; the relation still makes sense because the comparison `≤` is performed internally within each monoid.
- When `R` has only one element (the trivial ring), every pair of valuations is trivially equivalent because all comparisons `v r ≤ v s` are vacuously determined.
- The trivial valuation (sending every nonzero element to `1`) and any other trivial valuation on `R` are equivalent to each other.
- Equivalence is an equivalence relation on the class of valuations on a fixed ring `R`: it is reflexive, symmetric, and transitive.

### Not to be confused with

- *Equality of valuations* (`v₁ = v₂`): this requires the value groups and numerical values to coincide, which is strictly stronger than `VTask.IsEquiv`.
- *The valuation subring / valuation ring*: a subring, not a relation between valuations.
- *`Valuation.IsNontrivial`*: a property of a single valuation (existence of an element with value ≠ 0 and ≠ 1), not a relation between two valuations; though `VTask.IsEquiv` does preserve this property.