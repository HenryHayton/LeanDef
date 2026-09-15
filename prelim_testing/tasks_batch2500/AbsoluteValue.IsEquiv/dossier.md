## Object

`VTask.IsEquiv v w` is the proposition that two absolute values `v` and `w` on a semiring `R` (taking values in an ordered semiring `S`) are *equivalent*: for every pair of elements `x, y` in `R`, the inequality `v x ≤ v y` holds if and only if `w x ≤ w y`. Informally, `v` and `w` induce exactly the same ordering on the "sizes" of ring elements.

This is an equivalence relation on the set of absolute values on `R`. In the classical case where `R = ℝ` and both `v` and `w` are real-valued, the condition is equivalent to the existence of a positive real exponent `c` such that `v x ^ c = w x` for all `x` (i.e., one absolute value is a positive real power of the other).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsEquiv : {R : Type u_1} -> [Semiring R] -> {S : Type u_2} -> [Semiring S] -> [PartialOrder S] -> (v w : AbsoluteValue R S) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsEquiv : {R : Type u_1} -> [Semiring R] -> {S : Type u_2} -> [Semiring S] -> [PartialOrder S] -> (v w : AbsoluteValue R S) -> Prop`

The implicit type `R` is the semiring on which both absolute values are defined. The implicit type `S` is the ordered semiring in which the absolute values take their values. The argument `v` is the first absolute value; the argument `w` is the second. The proposition asserts that `v` and `w` are equivalent in the sense that they induce the same total preorder on `R`.

## Conventions

No edge-value conventions are declared: `VTask.IsEquiv` is a universally quantified proposition over all `x y : R` with no special treatment of boundary or junk inputs.

## Worked examples

- Claim: Every absolute value is equivalent to itself (`VTask.IsEquiv v v` holds for any `v`).

- Claim: If `v` and `w` are equivalent then `w` and `v` are equivalent (symmetry of `VTask.IsEquiv`).

- Claim: If `VTask.IsEquiv v w` and `VTask.IsEquiv w u`, then `VTask.IsEquiv v u` (transitivity).

- Claim: If `VTask.IsEquiv v w` and `v x < 1`, then `w x < 1` for the same `x`.

## Boundaries

- When `v = w` (definitionally), `VTask.IsEquiv v w` is trivially true by reflexivity: every biconditional `v x ≤ v y ↔ v x ≤ v y` holds.
- The relation is symmetric: `VTask.IsEquiv v w` implies `VTask.IsEquiv w v`, since each biconditional can be reversed.
- The relation is transitive, so it is a genuine equivalence relation on absolute values.
- Equivalent absolute values agree on whether any given element has absolute value equal to 1, strictly less than 1, strictly greater than 1, or equal to the absolute value of another element.
- Equivalence of absolute values is preserved under the topological structure: equivalent absolute values define the same notion of convergence to zero (any neighborhood of 0 in one topology maps to a neighborhood of 0 in the other).
- The definition is stated for general semirings and ordered semirings; the classical "power" characterization (`v x ^ c = w x`) requires stronger hypotheses (e.g., real-valued absolute values on a field).

## Not to be confused with

- `AbsoluteValue.eq` (definitional equality of absolute values): two absolute values can be equal as functions without `IsEquiv` being needed, but `IsEquiv` is a strictly coarser relation — equivalent absolute values need not be equal.
- `AbsoluteValue.IsNontrivial`: a property of a single absolute value (being non-trivial), not a relation between two absolute values; though equivalent absolute values share this property.
- Metric space isometry or topological conjugacy: `VTask.IsEquiv` is about the order structure of sizes, not directly about a map being distance-preserving, even though equivalent absolute values do induce homeomorphic topologies.