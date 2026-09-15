## Object

`VTask.mk'` constructs a non-unital sub-semiring of a non-unital non-associative semiring `R` by assembling three pieces of data that all describe the same underlying set: an explicit carrier set `s`, a sub-semigroup `sg` (which witnesses closure under multiplication), and an additive sub-monoid `sa` (which witnesses closure under addition and containing zero). The compatibility conditions ensure that `sg` and `sa` have exactly `s` as their carrier, so all three views agree and together supply every axiom needed for a non-unital sub-semiring.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mk' : {R : Type u} -> [NonUnitalNonAssocSemiring R] -> (s : Set R) -> (sg : Subsemigroup R) -> (hg : ↑sg = s) -> (sa : AddSubmonoid R) -> (ha : ↑sa = s) -> NonUnitalSubsemiring R
<!-- PINNED-SIGNATURE:END -->


`VTask.mk' : {R : Type u} -> [NonUnitalNonAssocSemiring R] -> (s : Set R) -> (sg : Subsemigroup R) -> (hg : ↑sg = s) -> (sa : AddSubmonoid R) -> (ha : ↑sa = s) -> NonUnitalSubsemiring R`

The ambient type `R` is the non-unital non-associative semiring inferred from context. The instance argument supplies the semiring structure on `R`. `s` is the desired carrier set of the sub-semiring being constructed. `sg` is a sub-semigroup of `R` (closed under multiplication) whose underlying set is required to equal `s`; the proof `hg` asserts exactly that equality. `sa` is an additive sub-monoid of `R` (closed under addition, containing zero) whose underlying set is required to equal `s`; the proof `ha` asserts that equality.

## Conventions

There are no junk-value or out-of-domain conventions to declare: the constructor is total and all arguments are meaningful — it is simply undefined territory if the compatibility proofs `hg` or `ha` cannot be supplied, which is ruled out by the type system.

## Worked examples

- Claim: The underlying set of `VTask.mk' s sg hg sa ha` is `s` (i.e., coercing to `Set R` recovers the carrier exactly).

- Claim: An element `x` belongs to `VTask.mk' s sg hg sa ha` if and only if it belongs to `s`.

- Claim: The `toSubsemigroup` projection of `VTask.mk' s sg hg sa ha` is exactly `sg`.

- Claim: The `toAddSubmonoid` projection of `VTask.mk' s sg hg sa ha` is exactly `sa`.

## Boundaries

- The constructor requires that both `sg` and `sa` have the same underlying set `s`. If `sg` and `sa` describe different sets, the proofs `hg` and `ha` cannot both be supplied, so no ill-formed construction is possible.
- There is no requirement that `s` be non-empty: an additive sub-monoid always contains zero, so the resulting non-unital sub-semiring automatically contains `0`.
- The ambient ring need not have a multiplicative identity (it is non-unital); consequently the resulting sub-semiring also need not contain a multiplicative unit.
- No closure under negation is assumed or enforced (the semiring need not be a ring).

## Not to be confused with

- `NonUnitalSubsemiring.mk` (the raw structure constructor that takes fields like `zero_mem'`, `add_mem'`, `mul_mem'` directly rather than deriving them from a sub-semigroup and additive sub-monoid).
- `Subsemiring.mk'` — the analogous constructor for unital sub-semirings, which additionally requires a sub-monoid (rather than a sub-semigroup) to handle the multiplicative identity.
- `NonUnitalSubring.mk'` — a similar assembler for non-unital sub-rings, which additionally demands an additive subgroup (closure under negation) rather than merely an additive sub-monoid.