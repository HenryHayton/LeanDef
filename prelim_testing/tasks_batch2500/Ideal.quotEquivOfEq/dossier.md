## Object

Given a ring `R` and two two-sided ideals `I` and `J` of `R` that are equal as ideals, `VTask.quotEquivOfEq h` is the canonical ring isomorphism from the quotient ring `R ⧸ I` to the quotient ring `R ⧸ J`. It witnesses the trivial but useful fact that quotienting a ring by equal ideals yields canonically isomorphic quotient rings.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.quotEquivOfEq : {R : Type u} -> [Ring R] -> {I J : Ideal R} -> [I.IsTwoSided] -> [J.IsTwoSided] -> (h : I = J) -> R ⧸ I ≃+* R ⧸ J
<!-- PINNED-SIGNATURE:END -->


`VTask.quotEquivOfEq : {R : Type u} -> [Ring R] -> {I J : Ideal R} -> [I.IsTwoSided] -> [J.IsTwoSided] -> (h : I = J) -> R ⧸ I ≃+* R ⧸ J`

The ambient ring `R` is the ring being quotiented. The two ideals `I` and `J` are the ideals being quotiented by; both are required to be two-sided (each carries an implicit `IsTwoSided` instance). The argument `h` is a proof that `I` and `J` are equal as ideals; this equality is the sole datum from which the isomorphism is constructed.

## Conventions

There are no junk-value or edge conventions to declare: the definition is total over all rings and pairs of equal two-sided ideals, and the proof of equality `h` completely determines the isomorphism.

## Worked examples

- Claim: When `I = J` with `h : I = J` being `rfl`, `VTask.quotEquivOfEq h` acts on a coset `⟦r⟧` by sending it to `⟦r⟧` in `R ⧸ J`.

- Claim: The isomorphism `VTask.quotEquivOfEq h` is a ring homomorphism, meaning it preserves both addition and multiplication.

- Claim: The inverse of `VTask.quotEquivOfEq h` is `VTask.quotEquivOfEq h.symm` (up to definitional equality), since `(R ⧸ J) ≃+* (R ⧸ I)` is obtained by swapping the roles of `I` and `J`.

## Boundaries

- When `I = J` holds with `h = rfl`, the resulting isomorphism is the identity ring isomorphism on `R ⧸ I`.
- The definition requires both `I` and `J` to carry `IsTwoSided` instances; without those instances the quotient ring structure `R ⧸ I` and `R ⧸ J` would not exist as rings, so the two-sidedness hypotheses are not restrictions but prerequisites.
- The isomorphism is uniquely determined by `h`: since it must send `⟦r⟧_I` to `⟦r⟧_J` for every `r : R`, there is exactly one sensible ring map in this situation.

## Not to be confused with

- `Submodule.quotEquivOfEq`: the analogous equivalence at the level of `R`-modules (or additive groups), which does not track the multiplicative ring structure.
- `Ideal.quotientEquivAlgOfEq`: the analogous isomorphism in the algebraic (algebra map) setting, which carries additional `Algebra` structure.
- `Ideal.quotEquiv` or `Ideal.quotientEquiv`: more general ring isomorphisms between quotients by possibly distinct ideals, requiring an explicit ring isomorphism between the ambient rings rather than mere equality of ideals.