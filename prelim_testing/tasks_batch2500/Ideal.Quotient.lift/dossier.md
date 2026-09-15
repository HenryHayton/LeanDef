## Object

`VTask.lift` constructs, from a ring homomorphism `f : R →+* S` that kills every element of a two-sided ideal `I` of `R`, the unique ring homomorphism `R ⧸ I →+* S` making the obvious triangle commute: the composite of the canonical quotient map `R → R ⧸ I` followed by the lifted map equals `f`.

This is the universal property of the quotient ring: any ring homomorphism out of `R` that vanishes on `I` factors uniquely through `R ⧸ I`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lift : {R : Type u} -> [Ring R] -> (I : Ideal R) -> {S : Type v} -> [I.IsTwoSided] -> [Semiring S] -> (f : R →+* S) -> (H : ∀ a ∈ I, f a = 0) -> R ⧸ I →+* S
<!-- PINNED-SIGNATURE:END -->


VTask.lift : {R : Type u} -> [Ring R] -> (I : Ideal R) -> {S : Type v} -> [I.IsTwoSided] -> [Semiring S] -> (f : R →+* S) -> (H : ∀ a ∈ I, f a = 0) -> R ⧸ I →+* S

- `R` is the source ring (a `Ring`).
- `I` is the ideal of `R` that is being quotiented out; it must be a two-sided ideal (witnessed by the `IsTwoSided` instance) for the quotient to carry a ring structure.
- `S` is the target semiring.
- `f` is the ring homomorphism from `R` to `S` that one wishes to factor through the quotient.
- `H` is the proof that `f` sends every element of `I` to zero in `S`; this is the necessary and sufficient compatibility condition for the lift to be well defined.

The result is a ring homomorphism from the quotient `R ⧸ I` to `S`.

## Conventions

There are no junk-value or out-of-domain conventions to declare: the definition is total on all inputs satisfying the stated type constraints, and the hypothesis `H` is a genuine mathematical requirement (not a junk fill).

## Worked examples

- Claim: For any ring `R`, ideal `I`, ring homomorphism `f : R →+* S` satisfying `H`, and element `a : R`, the lifted map applied to the coset `⟦a⟧` equals `f a`.
  (This is the commutativity condition: `VTask.lift I f H (mk I a) = f a`.)

- Claim: If `f : R →+* S` is surjective and kills `I`, then `VTask.lift I f H` is also surjective.

- Claim: If additionally the kernel of `f` is contained in `I` (i.e., `ker f ≤ I`), then `VTask.lift I f H` is injective, and hence (when combined with surjectivity) an isomorphism.

- Claim: The composite of `VTask.lift I f H` with the quotient map `mk I : R →+* R ⧸ I` equals `f` as ring homomorphisms `R →+* S`.

## Boundaries

- If `H` is the trivial proof that `f` kills the zero ideal (every ring homomorphism kills `{0}`), the lift is simply a ring homomorphism out of `R ⧸ {0} ≅ R`, and is essentially the same as `f` itself.
- When `I` is the entire ring `R`, the quotient `R ⧸ R` is the zero ring, and the lift is the unique ring homomorphism from the zero ring to `S` (which sends the unique element to `0`).
- The `IsTwoSided` instance is required: for a one-sided ideal the quotient does not form a ring, so the construction would not type-check.
- The hypothesis `H` must be stated for membership in `I` (not merely for generators of `I`); however, in practice one often proves it on generators and extends by linearity.

## Not to be confused with

- `VTask.lift` applied to the zero ideal is not the same as the identity: the quotient by the zero ideal is canonically isomorphic to `R`, but the types differ.
- The algebra version `liftₐ` (for `A →ₐ[R] B`) is a related but distinct construction that additionally tracks the algebra structure over a base ring `R`.
- The quotient map `mk I : R →+* R ⧸ I` is the canonical projection *into* the quotient, not a lift *out of* it.