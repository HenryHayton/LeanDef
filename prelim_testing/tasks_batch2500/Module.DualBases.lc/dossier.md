## Object

`VTask.lc e l` computes the **linear combination** of a family of vectors `e : ι → M` weighted by the finitely-supported coefficient function `l : ι →₀ R`. Concretely, it returns the finite sum
$$\sum_{i \in \operatorname{supp}(l)} l(i) \cdot e(i)$$
in the `R`-module `M`, where all but finitely many coefficients `l(i)` are zero, so the sum is well-defined.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lc : {R : Type u_1} -> {M : Type u_2} -> [CommSemiring R] -> [AddCommMonoid M] -> [Module R M] -> {ι : Type u_4} -> (e : ι → M) -> (l : ι →₀ R) -> M
<!-- PINNED-SIGNATURE:END -->


The implicit arguments `R` and `M` are the coefficient semiring and the module type, respectively; the relevant algebraic instances (`CommSemiring R`, `AddCommMonoid M`, `Module R M`) are inferred automatically. The index type `ι` is also implicit. The explicit argument `e` is the **family of vectors**: a function from index type `ι` into the module `M`, giving the "basis-like" vectors being combined. The explicit argument `l` is the **coefficient function**: a finitely-supported function `ι →₀ R`, whose values are the scalar weights assigned to each vector in `e`.

## Conventions

When `l` is the zero finsupp (empty support), the sum is empty and the result is `0 : M`, the additive identity of the module. This follows from the convention that a sum over an empty index set is zero.

## Worked examples

- Claim: For `e : Fin 3 → ℤ` defined by `e i = i`, and `l` the finsupp assigning coefficient `2` to index `1` and `3` to index `2` (and zero elsewhere), `VTask.lc e l = 2 * 1 + 3 * 2 = 8`.

- Claim: For any family `e : ι → M` and the zero finsupp `l = 0`, `VTask.lc e l = 0`.

- Claim: For `e : Fin 2 → ℚ` with `e 0 = 5` and `e 1 = -3`, and `l` assigning coefficient `1` to `0` and `1` to `1`, `VTask.lc e l = 5 + (-3) = 2`.

## Boundaries

- **Empty support**: If `l = 0` (i.e., `l` has empty support), then `VTask.lc e l = 0` regardless of `e`, because the sum is over an empty set.
- **Single-index support**: If `l` is supported only at a single index `i₀` with value `c`, then `VTask.lc e l = c • e i₀`.
- **Index type is `Empty` or uninhabited**: If `ι` is an empty type, there are no indices and `l` must be `0`, so the result is `0`.
- **Zero coefficient at an index**: Any index `i` where `l i = 0` contributes `0 • e i = 0` to the sum and is conventionally excluded from the support, so it does not affect the result.
- **The vectors `e` can be arbitrary**: there is no requirement that `e` be injective, linearly independent, or span `M`; `VTask.lc` is defined for any function `e`.

## Not to be confused with

- `Finsupp.linearCombination R e l`: The parent definition of which `VTask.lc` is a convenient abbreviation; they are propositionally equal but `VTask.lc` drops the explicit `R` argument.
- `Finsupp.sum l f`: The underlying finsupp summation combinator; `VTask.lc e l` is the special case `l.sum (fun i a => a • e i)`, so it is more structured.
- `Submodule.span R (Set.range e)`: The set of all possible linear combinations of the range of `e`; `VTask.lc e l` produces one *particular* element of this span, not the span itself.