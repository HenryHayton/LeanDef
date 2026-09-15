## VTask.IsPrimary

### Object

A submodule `S` of an `R`-module `M` is called **primary** if two conditions hold simultaneously: (1) `S` is a proper submodule (i.e., `S ≠ ⊤`, meaning `S` is not the whole module), and (2) whenever a scalar multiple `r • x` belongs to `S`, either the element `x` itself belongs to `S`, or the scalar `r` is "nilpotent on `M` modulo `S`" in the sense that some power `rⁿ` annihilates the entire module modulo `S` (formally, `r^n • ⊤ ≤ S` for some natural number `n`). This is the module-theoretic generalisation of the classical notion of a primary ideal: every element of `R/S` is either zero or has a power that kills every element of `M/S`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsPrimary : {R : Type u_1} -> {M : Type u_2} -> [CommSemiring R] -> [AddCommMonoid M] -> [Module R M] -> (S : Submodule R M) -> Prop
<!-- PINNED-SIGNATURE:END -->


The argument `S` is the submodule of `M` over the commutative semiring `R` whose primaryness is being tested. The surrounding instance arguments supply the algebraic structure: a commutative semiring `R`, an additive commutative monoid `M`, and a scalar multiplication making `M` an `R`-module.

### Conventions

There are no junk-value conventions to declare: `VTask.IsPrimary` is a `Prop`-valued predicate that is well-defined for every submodule of every `R`-module over any commutative semiring; no distinguished output is assigned to degenerate or boundary inputs outside the definition's natural scope.

### Worked examples

- Claim: If `S` is a primary submodule of `M`, then `S ≠ ⊤`.

- Claim: If `S` is a primary submodule and `r • x ∈ S`, then `x ∈ S` or there exists `n : ℕ` such that `r ^ n • (⊤ : Submodule R M) ≤ S`.

- Claim: The whole module `⊤` is never primary (for any `R`-module `M`), since `VTask.IsPrimary` requires the submodule to be proper.

- Claim: For a Noetherian ring `R` viewed as a module over itself, an ideal `I` (as a submodule of `R`) satisfies `VTask.IsPrimary I` if and only if it is a primary ideal in the classical sense.

### Boundaries

- The top submodule `⊤` is never primary, by the explicit `S ≠ ⊤` condition in the definition.
- The zero submodule `⊥` may or may not be primary depending on the ring and module; it is primary when `R` is an integral domain and `M` is torsion-free (since then `r • x = 0` implies `r = 0` or `x = 0`, and the nilpotency condition is vacuous in the torsion-free case only when `r` is nilpotent).
- Every inf-irreducible proper submodule is primary (witnessed by `InfIrred.isPrimary`).
- Primaryness is preserved under finite intersections of primary submodules that share the same associated prime (i.e., the same radical of the colon ideal).
- The definition works over any commutative semiring, not just a Noetherian ring; the Noetherian hypothesis is only needed for existence of primary decompositions.

### Not to be confused with

- `Ideal.IsPrimary`: the ring-theoretic specialisation where `M = R` and the submodule is an ideal; `VTask.IsPrimary` directly generalises this, and both coincide when `S` is an ideal viewed as a submodule.
- `Submodule.IsPrime`: a prime submodule satisfies the sharper condition that `r • x ∈ S` implies `x ∈ S` or `r • ⊤ ≤ S` (without taking powers), making every prime submodule primary but not conversely.
- `Submodule.radical` (of the colon ideal): the radical of `S.colon Set.univ` is the "associated prime" of a primary submodule, and primaryness of `S` implies this radical is a prime ideal, but the radical itself is not the same object as the primary submodule.