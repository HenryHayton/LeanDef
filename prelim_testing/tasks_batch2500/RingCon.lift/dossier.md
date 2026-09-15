## Object

Given a ring congruence relation `c` on a semiring `M` and a semiring homomorphism `f : M →+* P` whose kernel contains `c` (i.e., any two `c`-related elements are identified by `f`), `VTask.lift` produces the unique semiring homomorphism `c.Quotient →+* P` that makes the obvious triangle commute: applying `VTask.lift` after the quotient map `c.mk'` recovers `f`.

This is the universal property of the quotient: `f` is constant on each equivalence class of `c`, so it factors through the quotient ring `c.Quotient`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lift : {M : Type u_1} -> {P : Type u_3} -> [NonAssocSemiring M] -> [NonAssocSemiring P] -> (c : RingCon M) -> (f : M →+* P) -> (H : c ≤ RingCon.ker f) -> c.Quotient →+* P
<!-- PINNED-SIGNATURE:END -->


`VTask.lift : {M : Type u_1} -> {P : Type u_3} -> [NonAssocSemiring M] -> [NonAssocSemiring P] -> (c : RingCon M) -> (f : M →+* P) -> (H : c ≤ RingCon.ker f) -> c.Quotient →+* P`

The implicit arguments `M` and `P` are the source and target semirings; the two typeclass arguments equip them with semiring structure. The argument `c` is the congruence relation on `M` whose equivalence classes form the quotient ring `c.Quotient`. The argument `f` is a semiring homomorphism from `M` to `P`. The proof `H` witnesses that `c` is contained in the kernel congruence of `f`, i.e., whenever `c m n` holds, `f m = f n`; this is the condition that allows `f` to descend to the quotient.

## Conventions

The definition is total: no junk values arise because the well-definedness hypothesis `H` is required explicitly as a proof argument rather than being checked lazily.

## Worked examples

- Claim: For any congruence `c` and homomorphism `f` with `H : c ≤ RingCon.ker f`, applying `VTask.lift c f H` to the image of `x` under the quotient map `c.mk'` gives `f x`.

- Claim: The lifted map `VTask.lift c f H` is injective if and only if `c` equals the kernel congruence of `f`.

- Claim: The lifted map `VTask.lift c f H` is surjective if and only if `f` itself is surjective.

- Claim: The lifted map is the unique ring homomorphism `g : c.Quotient →+* P` satisfying `g.comp c.mk' = f`.

## Boundaries

- When `H` witnesses that `c` equals `RingCon.ker f` exactly (rather than just `c ≤ RingCon.ker f`), the lifted map is injective; combined with surjectivity of `f`, it becomes an isomorphism (the first isomorphism theorem for rings).
- When `c` is the trivial congruence (equality), the quotient is isomorphic to `M` itself, and `VTask.lift` essentially recovers `f`.
- When `c` is the total congruence (everything related to everything), `c.Quotient` is the zero ring, and the lifted map sends the unique element to `0 = 1` in `P` (which is only consistent when `P` is also the zero ring, a case forced by the homomorphism axioms).
- The hypothesis `H` is essential: without it the map would not be well-defined on equivalence classes.

## Not to be confused with

- `RingCon.mk'`: the quotient map `M →+* c.Quotient` going in the opposite direction; `VTask.lift` goes from the quotient to the target, not from the source to the quotient.
- `RingCon.ker`: the kernel congruence of a ring homomorphism, which is an input ingredient to `VTask.lift` rather than the lift itself.
- `RingCon.map`: a ring congruence map induced between two quotients by an inequality of congruences, a special case that uses `VTask.lift` internally but has a different signature.