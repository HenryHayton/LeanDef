## Object

`VTask.mk'` constructs a non-unital subring of a non-unital non-associative ring `R` from three compatible pieces of data: an underlying set `s`, a multiplicative subsemigroup `sm`, and an additive subgroup `sa`, given proofs that both `sm` and `sa` have exactly `s` as their carrier set. The resulting non-unital subring has `s` as its underlying set, inherits its multiplicative closure from `sm`, and inherits its additive structure (closure under addition, negation, and zero) from `sa`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mk' : {R : Type u} -> [NonUnitalNonAssocRing R] -> (s : Set R) -> (sm : Subsemigroup R) -> (sa : AddSubgroup R) -> (hm : ↑sm = s) -> (ha : ↑sa = s) -> NonUnitalSubring R
<!-- PINNED-SIGNATURE:END -->


`{R : Type u} -> [NonUnitalNonAssocRing R] -> (s : Set R) -> (sm : Subsemigroup R) -> (sa : AddSubgroup R) -> (hm : ↑sm = s) -> (ha : ↑sa = s) -> NonUnitalSubring R`

The implicit type argument `R` is the ambient ring. The instance argument supplies the non-unital non-associative ring structure on `R`. The argument `s` is the intended underlying set of the non-unital subring being constructed. The argument `sm` is a subsemigroup of `R` whose carrier is required to equal `s`; it witnesses that `s` is closed under multiplication. The argument `sa` is an additive subgroup of `R` whose carrier is also required to equal `s`; it witnesses that `s` contains zero and is closed under addition and negation. The proof `hm` asserts that the coercion of `sm` to a set equals `s`. The proof `ha` asserts that the coercion of `sa` to a set equals `s`.

## Conventions

There are no junk-value or out-of-domain conventions for this definition: it is a total constructor on well-typed, fully-constrained inputs, and no degenerate input regime produces a conventionally assigned output.

## Worked examples

- Claim: The underlying set of `VTask.mk' s sm sa hm ha` is `s`.

  For any `s`, `sm`, `sa`, `hm`, `ha`, the coercion `(VTask.mk' s sm sa hm ha : Set R) = s` holds, as witnessed by `NonUnitalSubring.coe_mk'`.

- Claim: Membership in `VTask.mk' s sm sa hm ha` is equivalent to membership in `s`.

  For any element `x : R`, `x ∈ VTask.mk' s sm sa hm ha ↔ x ∈ s`, as witnessed by `NonUnitalSubring.mem_mk'`. In particular, membership in the constructed subring is entirely determined by `s`, not by the internal structure of `sm` or `sa`.

- Claim: The `toAddSubgroup` of `VTask.mk' s sm sa hm ha` recovers `sa` exactly.

  The projection `(VTask.mk' s sm sa hm ha).toAddSubgroup = sa` holds, confirming that the additive structure is taken unmodified from `sa`.

- Claim: The `toSubsemigroup` of `VTask.mk' s sm sa hm ha` recovers `sm` exactly.

  The projection `(VTask.mk' s sm sa hm ha).toSubsemigroup = sm` holds, confirming that the multiplicative structure is taken unmodified from `sm`.

## Boundaries

- The construction requires both `hm` and `ha` as hypotheses; if the carriers of `sm` and `sa` were not equal to `s`, the construction would be ill-typed. There is no degenerate or partial case.
- Because both `sm` and `sa` must have the same carrier `s`, the caller must ensure these two pieces of data are mutually consistent before invoking `VTask.mk'`.
- The resulting non-unital subring does not include a multiplicative identity element (it is non-unital), so no unity condition is checked or required.
- The ring `R` is non-associative in general; neither `sm` nor `sa` is required to witness associativity.

## Not to be confused with

- `NonUnitalSubring.mk` (the structure constructor): takes the subring's fields directly, rather than accepting a separate set plus compatibility proofs.
- `Subring.mk'`: the analogous constructor for unital subrings, which additionally requires a proof that the identity element belongs to the set.
- `NonUnitalSubsemiring.mk'`: a similar smart constructor but for non-unital subsemirings, which lack the additive inverse (negation) requirement supplied by the `AddSubgroup` argument here.