## Object

`VTask.IsNontrivial v` is the proposition asserting that the absolute value `v : AbsoluteValue R S` is *nontrivial*: there exists at least one nonzero element of `R` on which `v` does not take the value `1`. In other words, `v` is not the trivial absolute value (which equals `1` on every nonzero element), witnessed constructively by a single element.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsNontrivial : {R : Type u_5} -> [Semiring R] -> {S : Type u_6} -> [Semiring S] -> [PartialOrder S] -> (v : AbsoluteValue R S) -> Prop
<!-- PINNED-SIGNATURE:END -->


`(v : AbsoluteValue R S) -> Prop`

The sole argument `v` is the absolute value being tested for nontriviality. The type `R` is the source semiring (whose elements are measured), `S` is the target ordered semiring (which receives the measured values), and the typeclasses `[Semiring R]`, `[Semiring S]`, `[PartialOrder S]` endow `R` and `S` with their respective algebraic and order structures.

## Conventions

No special junk-value or edge-case conventions are declared for this predicate: it is a universally quantified existential Prop with no distinguished degenerate inputs.

## Worked examples

- Claim: The ordinary real absolute value on `ℤ` is nontrivial, because `v 2 = 2 ≠ 1`.

- Claim: The trivial absolute value on any nontrivial ring (which equals `1` on every nonzero element) does *not* satisfy `VTask.IsNontrivial`; every nonzero element maps to `1`.

- Claim: If `v.IsNontrivial` holds, then there exists an element `x` with `1 < v x` (the absolute value exceeds `1` somewhere).

- Claim: `VTask.IsNontrivial v` is preserved under equivalence of absolute values: if `v` is equivalent to `w` (in the sense of `AbsoluteValue.IsEquiv`), then `v.IsNontrivial ↔ w.IsNontrivial`.

## Boundaries

- If `v` is the trivial absolute value (sending every nonzero element to `1` and zero to `0`), then `VTask.IsNontrivial v` is false. The negation characterises exactly this situation: `¬ VTask.IsNontrivial v` holds if and only if `v x = 1` for all `x ≠ 0`.
- The definition does not require `DecidablePred (· = 0)` on `R` or `NoZeroDivisors R`, giving it broader applicability than the equivalent condition `v ≠ .trivial`.
- When `R` does have no zero divisors and `S` is nontrivial, and decidability of `· = 0` is available, `VTask.IsNontrivial v` is logically equivalent to `v ≠ AbsoluteValue.trivial`.
- If `v` is nontrivial, then both: there exists `x` with `1 < v x`, and there exists `x ≠ 0` with `v x < 1`.

## Not to be confused with

- `AbsoluteValue.trivial`: the specific trivial absolute value itself (the map sending nonzero elements to `1`), as opposed to the *predicate* asserting nontriviality.
- `Ne` applied to `AbsoluteValue.trivial` (i.e., `v ≠ .trivial`): the syntactically stronger condition that requires `DecidablePred (· = 0)` on `R`, whereas `VTask.IsNontrivial` avoids that assumption.
- `AbsoluteValue.IsEquiv`: the relation asserting that two absolute values induce the same topology / ordering, which is a different (relational) notion from the unary predicate of nontriviality.