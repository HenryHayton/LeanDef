## VTask.Baer

### Object

Baer's criterion for a module. Given a ring `R` and an `R`-module `Q`, `VTask.Baer R Q` asserts that `Q` satisfies *Baer's criterion*: every `R`-linear map from any ideal `I` of `R` into `Q` can be extended to an `R`-linear map defined on all of `R`. In classical homological algebra, this is one of the standard characterisations of an injective module — a module is injective if and only if it satisfies Baer's criterion (under mild set-theoretic hypotheses).

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Baer : (R : Type u) -> [Ring R] -> (Q : Type v) -> [AddCommGroup Q] -> [Module R Q] -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Baer : (R : Type u) -> [Ring R] -> (Q : Type v) -> [AddCommGroup Q] -> [Module R Q] -> Prop`

The first explicit argument `R` is the ring of scalars. The instance argument `[Ring R]` equips `R` with its ring structure. The second explicit argument `Q` is the candidate injective module whose elements receive the extended linear maps. The instance arguments `[AddCommGroup Q]` and `[Module R Q]` equip `Q` with its abelian group structure and its `R`-module structure, respectively.

### Conventions

No special junk-value or boundary conventions are declared: the predicate is a universally quantified statement over all ideals and all linear maps, so it is a well-formed `Prop` for every ring `R` and every `R`-module `Q` without restriction.

### Worked examples

- Claim: Any divisible abelian group (viewed as a `ℤ`-module) satisfies `VTask.Baer ℤ A` whenever `A` is divisible by `ℤ`.

- Claim: If `Q` satisfies `VTask.Baer R Q` and `e : Q ≃ₗ[R] M` is an `R`-linear isomorphism, then `VTask.Baer R M` also holds.

- Claim: Under the assumption `[Small.{v} R]`, `VTask.Baer R Q` is equivalent to `Q` being an injective `R`-module in the sense of `Module.Injective R Q`.

- Claim: For a commutative ring `R` and an `R`-module `M`, `VTask.Baer R M` is equivalent to the restriction map `LinearMap.lcomp R M I.subtype` being surjective for every ideal `I`.

### Boundaries

- When the ideal `I` is the zero ideal `⊥`, the only linear map `I →ₗ[R] Q` is the zero map, which trivially extends; this case places no constraint on `Q`.
- When `I = R` (the whole ring, viewed as an ideal), the criterion requires every `R`-linear map `R →ₗ[R] Q` to extend to one from `R` to itself, which is automatically satisfied since the identity on `R` is such an extension; again no constraint is added in this case alone.
- The criterion is a purely *existential* statement: it requires the existence of *some* extension, not a canonical one.
- Under set-theoretic smallness (`[Small.{v} R]`), Baer's criterion is provably equivalent to module injectivity; without this hypothesis the implication from Baer to injectivity is still proved in Mathlib (one direction always holds), while the converse may require the smallness assumption.

### Not to be confused with

- `Module.Injective R Q` — the categorical notion of an injective `R`-module (the lifting property for injective linear maps); Baer's criterion is equivalent to this under `[Small.{v} R]` but is stated differently.
- Injectivity of a function (`Function.Injective`) — a completely unrelated predicate asserting that a map sends distinct inputs to distinct outputs.
- `Module.Flat` — the flatness condition for modules, which concerns tensor products rather than extension of linear maps.