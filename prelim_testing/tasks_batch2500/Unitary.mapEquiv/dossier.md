## Object

`VTask.mapEquiv` takes a star monoid isomorphism `f : R ≃⋆* S` between two star monoids and produces a star monoid isomorphism `unitary R ≃⋆* unitary S` between their respective unitary subgroups. In other words, if two star monoids are isomorphic (as star monoids), then their unitary subgroups are likewise isomorphic as star monoids — and `mapEquiv` constructs that induced isomorphism explicitly.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mapEquiv : {R : Type u_2} -> {S : Type u_3} -> [Monoid R] -> [StarMul R] -> [Monoid S] -> [StarMul S] -> (f : R ≃⋆* S) -> ↥(unitary R) ≃⋆* ↥(unitary S)
<!-- PINNED-SIGNATURE:END -->


`VTask.mapEquiv : {R : Type u_2} -> {S : Type u_3} -> [Monoid R] -> [StarMul R] -> [Monoid S] -> [StarMul S] -> (f : R ≃⋆* S) -> ↥(unitary R) ≃⋆* ↥(unitary S)`

The implicit type arguments `R` and `S` are the underlying types of the two star monoids. The instance arguments supply the monoid and star-multiplication structures on each type. The explicit argument `f` is the star monoid isomorphism from `R` to `S` that induces the construction; it determines both the forward and inverse maps of the resulting isomorphism on unitary subgroups.

## Conventions

There are no junk-value or boundary conventions for this definition: it is a total construction over well-typed inputs, and every star monoid isomorphism between star monoids induces a well-defined isomorphism of unitary subgroups without any exceptional cases.

## Worked examples

- Claim: For any star monoid isomorphism `f : R ≃⋆* S`, applying `VTask.mapEquiv f` to the identity element of `unitary R` yields the identity element of `unitary S`.

- Claim: For any star monoid isomorphism `f : R ≃⋆* S` and element `u : unitary R`, the inverse of `VTask.mapEquiv f` applied to `VTask.mapEquiv f u` equals `u` (i.e., the forward and inverse maps are mutual inverses on unitary elements).

- Claim: `VTask.mapEquiv` applied to the identity star monoid isomorphism `StarMulEquiv.refl R` yields an isomorphism that acts as the identity on every element of `unitary R`.

- Claim: For star monoid isomorphisms `f : R ≃⋆* S` and `g : S ≃⋆* T`, the composition of `VTask.mapEquiv f` and `VTask.mapEquiv g` agrees pointwise with `VTask.mapEquiv (g.trans f)` (functoriality of the construction).

## Boundaries

- The construction is defined for any two star monoids `R` and `S` connected by a star monoid isomorphism `f`; no additional hypotheses (such as commutativity or involutivity of the star) are required.
- When `R = S` and `f` is the identity isomorphism, `VTask.mapEquiv f` is (up to definitional equality) the identity isomorphism on `unitary R`.
- The inverse of `VTask.mapEquiv f` is `VTask.mapEquiv f.symm`: the construction respects taking symmetric isomorphisms.
- Because `f` is an isomorphism (not merely a homomorphism), the resulting map on unitary subgroups is guaranteed to be bijective; there is no risk of the image missing elements of `unitary S`.

## Not to be confused with

- `Unitary.map` (or a similarly named function): the non-invertible variant that takes a star monoid *homomorphism* and produces only a *morphism* (not necessarily an isomorphism) of unitary subgroups.
- `StarMulEquiv.ofUnitary` or analogues that go in the other direction — constructing a star monoid isomorphism of the ambient monoids from data about their unitary subgroups.
- The coercion of `VTask.mapEquiv f` to its underlying function, which maps elements of `unitary R` to `unitary S` but forgets the isomorphism structure.