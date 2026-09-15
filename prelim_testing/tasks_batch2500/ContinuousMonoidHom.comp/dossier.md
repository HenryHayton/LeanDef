## Object

`VTask.comp g f` is the composition of two continuous monoid homomorphisms. Given monoids `A`, `B`, and `C` equipped with topologies, and given a continuous monoid homomorphism `f : A →ₜ* B` and another `g : B →ₜ* C`, the composition is the continuous monoid homomorphism `A →ₜ* C` that sends each element `a : A` to `g(f(a))`. It simultaneously witnesses both algebraic compatibility (a monoid homomorphism) and topological compatibility (continuity of the composite map).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {A : Type u_2} -> {B : Type u_3} -> {C : Type u_4} -> [Monoid A] -> [Monoid B] -> [Monoid C] -> [TopologicalSpace A] -> [TopologicalSpace B] -> [TopologicalSpace C] -> (g : B →ₜ* C) -> (f : A →ₜ* B) -> A →ₜ* C
<!-- PINNED-SIGNATURE:END -->


`VTask.comp : {A : Type u_2} -> {B : Type u_3} -> {C : Type u_4} -> [Monoid A] -> [Monoid B] -> [Monoid C] -> [TopologicalSpace A] -> [TopologicalSpace B] -> [TopologicalSpace C] -> (g : B →ₜ* C) -> (f : A →ₜ* B) -> A →ₜ* C`

The implicit type arguments `A`, `B`, and `C` are the source, intermediate, and target types, respectively. The instance arguments supply monoid structures and topologies on each of these types. The first explicit argument `g` is the outer continuous monoid homomorphism from the intermediate monoid `B` to the target monoid `C`. The second explicit argument `f` is the inner continuous monoid homomorphism from the source monoid `A` to the intermediate monoid `B`. The result is the continuous monoid homomorphism from `A` to `C` obtained by applying `f` first and then `g`.

## Conventions

No special junk-value or edge conventions are declared for this definition: it is a total function on all valid continuous monoid homomorphisms `f` and `g`, and the mathematical meaning is unambiguous in all cases, including trivial or identity morphisms.

## Worked examples

- Claim: For the trivial one-element monoid `Unit` with its unique topology, composing any continuous monoid homomorphism `f : A →ₜ* Unit` with any `g : Unit →ₜ* C` yields a morphism whose underlying function sends every element of `A` to the identity of `C`.

- Claim: If `f : A →ₜ* B` and `g : B →ₜ* C` are continuous monoid homomorphisms, then `VTask.comp g f` maps the identity element of `A` to the identity element of `C`, since both `f` and `g` individually preserve the identity.

- Claim: The underlying map of `VTask.comp g f` is the function composition of the underlying maps of `g` and `f`; that is, for every `a : A`, applying the composite morphism to `a` equals `g(f(a))`.

- Claim: Composition is associative: for continuous monoid homomorphisms `f : A →ₜ* B`, `g : B →ₜ* C`, `h : C →ₜ* D`, the composites `VTask.comp h (VTask.comp g f)` and `VTask.comp (VTask.comp h g) f` define the same function `A → D`.

## Boundaries

- When either `f` or `g` is the identity continuous monoid homomorphism on a type, the composition recovers the other morphism (up to definitional or propositional equality of the underlying functions).
- The definition is total: it does not require any non-triviality conditions on the monoids or topological spaces.
- When `A = B = C` and both morphisms are endomorphisms, the result is an endomorphism of the same continuous monoid.
- Because continuity of a composition follows from continuity of each factor, the topological part of the result is always well-formed.

## Not to be confused with

- `MonoidHom.comp`: The purely algebraic composition of monoid homomorphisms, which discards topological data entirely and does not require or assert continuity.
- `ContinuousMap.comp`: Composition of continuous maps between topological spaces, which carries no algebraic (monoid homomorphism) structure.
- Function composition `Function.comp`: Raw function composition with no algebraic or topological conditions whatsoever.