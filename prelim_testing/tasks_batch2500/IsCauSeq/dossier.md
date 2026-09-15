## 1. Object

A predicate asserting that a sequence is Cauchy with respect to a given absolute-value function. Concretely, the sequence `f : ℕ → β` is Cauchy if for every positive tolerance `ε`, there exists an index `i` such that all later terms `f j` (with `j ≥ i`) lie within distance `ε` of `f i`, as measured by `abv`.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsCauSeq : {α : Type u_3} -> [Field α] -> [LinearOrder α] -> [IsStrictOrderedRing α] -> {β : Type u_4} -> [Ring β] -> (abv : β → α) -> (f : ℕ → β) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsCauSeq : {α : Type u_3} -> [Field α] -> [LinearOrder α] -> [IsStrictOrderedRing α] -> {β : Type u_4} -> [Ring β] -> (abv : β → α) -> (f : ℕ → β) -> Prop`

The type `α` is the ordered field in which distances are measured (e.g., the rationals or reals). The type `β` is the ring whose elements are the terms of the sequence (e.g., the rationals, complexes, or a p-adic field). The argument `abv` is the absolute-value function (or more generally any function playing the role of a norm) mapping ring elements to non-negative elements of `α`; it is used to measure the size of differences. The argument `f` is the sequence under scrutiny, indexed by the natural numbers.

## 3. Conventions

No special junk-value or edge conventions are declared for this predicate: it is a universally quantified `Prop`, and its truth value is fully determined by the mathematical content of the quantifiers for every choice of `abv` and `f`.

## 4. Worked examples

- Claim: Every constant sequence satisfies `VTask.IsCauSeq abv` for any absolute-value function `abv`, because all differences `f j - f i` equal zero and `abv 0` is less than any positive `ε` (under the standard axioms for an absolute value).

- Claim: If `f` and `g` both satisfy `VTask.IsCauSeq abv`, then so does their pointwise sum `f + g`.

- Claim: If `f` and `g` both satisfy `VTask.IsCauSeq abv`, then so does their pointwise product `f * g`.

- Claim: Any sequence satisfying `VTask.IsCauSeq abv` is bounded: there exists some `r : α` such that `abv (f i) < r` for all `i`.

## 5. Boundaries

- When `abv` is the zero map (sending every element to `0`), every sequence trivially satisfies the predicate, since `abv (f j - f i) = 0 < ε` for any `ε > 0`.
- The predicate quantifies over `ε > 0` in the ordered field `α`; if `α` has no positive elements (which cannot happen for a field with the strict-order axioms imposed), the condition would be vacuously true.
- The tail-index witness `i` need only work for a single fixed `ε`; the predicate requires such a witness to exist for *every* positive `ε`, which is the essential content.
- The condition is one-sided in the index: it requires `abv (f j - f i) < ε` for all `j ≥ i`, not symmetrically for all `j, k ≥ i`. These two formulations are equivalent for sequences in a ring with a well-behaved absolute value, but the formulation here fixes the basepoint at `i`.

## 6. Not to be confused with

- `CauSeq`: a bundled type pairing a sequence with a proof that it satisfies the Cauchy condition, as opposed to the bare predicate `VTask.IsCauSeq` which simply asserts the property.
- `CauchySeq` (in the metric/topological sense): the topological notion of a Cauchy sequence in a uniform space or metric space, defined via filters or open covers, rather than via an explicit absolute-value function.
- `Filter.Cauchy`: a predicate on filters expressing the Cauchy property at the level of filter bases, which generalises `CauchySeq` but is unrelated to the algebraic absolute-value formulation used here.