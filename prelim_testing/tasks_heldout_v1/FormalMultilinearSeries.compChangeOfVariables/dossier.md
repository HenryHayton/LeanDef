## VTask.compChangeOfVariables

### Object

Given natural numbers `m`, `M`, `N`, an index `i = (n, f)` consisting of a natural number `n` and a function `f : Fin n → ℕ`, plus a proof that `i` belongs to the set `compPartialSumSource m M N`, this function produces a dependent pair `(k, c)` where `k` is a natural number and `c` is a `Composition` of `k`. Concretely, it packages the function `f`'s values as the block sizes of a composition: the integer `k` is the sum of all values `f(j)`, and the composition `c` records `f(0), f(1), …, f(n−1)` as the list of block lengths. This repackaging is the change-of-variables map needed when computing the composition of two partial sums of formal power series — it converts the "source" indexing (a function from a finite set into the naturals) into the "target" indexing (a composition of a natural number).

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.compChangeOfVariables : (m M N : ℕ) -> (i : (n : ℕ) × (Fin n → ℕ)) -> (hi : i ∈ FormalMultilinearSeries.compPartialSumSource m M N) -> (n : ℕ) × Composition n
<!-- PINNED-SIGNATURE:END -->


`(m M N : ℕ) -> (i : (n : ℕ) × (Fin n → ℕ)) -> (hi : i ∈ FormalMultilinearSeries.compPartialSumSource m M N) -> (n : ℕ) × Composition n`

The first three arguments, `m`, `M`, and `N`, are natural-number cutoffs that together determine the finite set `compPartialSumSource m M N` — the domain of summation on the "source" side of the change of variables. The argument `i` is the source index, a sigma-type pair consisting of an arity `n` and a function `f : Fin n → ℕ` that assigns a size to each of `n` slots. The argument `hi` is the membership proof certifying that `i` lies in `compPartialSumSource m M N`; this is needed to verify that every block size is positive (a requirement for a valid `Composition`).

### Conventions

The function is total on its stated domain: the membership hypothesis `hi` is the only restriction, and no junk value convention is needed for out-of-domain inputs because inputs outside the domain simply do not typecheck without a proof `hi`.

### Worked examples

- Claim: For `i = (2, ![1, 3])` with `i ∈ compPartialSumSource m M N` (for appropriate `m M N`), the output composition has length 2 and total sum 4.

- Claim: If `i = (1, ![k])` is in `compPartialSumSource m M N`, then `VTask.compChangeOfVariables m M N i hi` is the sigma pair `(k, composition_with_single_block_k)`, i.e. a composition of `k` into one block of size `k`, and its length is 1.

- Claim: The length of the composition in `VTask.compChangeOfVariables m M N i hi` always equals `i.1` (the arity `n` of the source index).

- Claim: For each `j : Fin i.1`, the `j`-th block size of the resulting composition equals `i.2 j`, i.e. the function value `f(j)` at that slot.

### Boundaries

- When `n = 0` (an empty function), the composition produced has total sum 0 and is the empty composition of 0, provided the membership condition is satisfied (which forces `m = 0` in that case).
- The membership condition `hi` enforces that every value `f(j)` is at least 1 (a block in a `Composition` must be positive), so the output is always a valid `Composition`.
- The map is surjective onto `compPartialSumTargetSet m M N`: every element of the target can be lifted back to a source element that maps to it under this change of variables.

### Not to be confused with

- `FormalMultilinearSeries.compPartialSumSource`: this is the *domain* finite set from which `i` is drawn, not the change-of-variables map itself.
- `FormalMultilinearSeries.compPartialSumTarget`: the *codomain* finite set (of sigma pairs `(n, Composition n)`) into which the change-of-variables maps; this definition produces elements of it but is not the set itself.
- `Composition.ofFn`: a lower-level constructor that turns a function `Fin n → ℕ` into a `Composition`; the present definition additionally computes the total and bundles everything into a sigma type, requiring the membership proof to guarantee positivity of blocks.