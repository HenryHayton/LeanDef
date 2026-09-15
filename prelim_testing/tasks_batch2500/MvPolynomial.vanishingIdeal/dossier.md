## Object

Given a field extension `k ⊆ K` and a set `V` of `K`-valued points indexed by a type `σ`, the **vanishing ideal** of `V` is the ideal in the multivariate polynomial ring `k[σ]` (polynomials over `k` in variables indexed by `σ`) consisting of all polynomials that evaluate to zero at every point in `V`. It is the algebraic shadow of the geometric set `V`: the collection of all polynomial equations that are simultaneously satisfied by every element of `V`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.vanishingIdeal : (k : Type u_1) -> {K : Type u_2} -> [Field k] -> [Field K] -> [Algebra k K] -> {σ : Type u_3} -> (V : Set (σ → K)) -> Ideal (MvPolynomial σ k)
<!-- PINNED-SIGNATURE:END -->


`VTask.vanishingIdeal : (k : Type u_1) -> {K : Type u_2} -> [Field k] -> [Field K] -> [Algebra k K] -> {σ : Type u_3} -> (V : Set (σ → K)) -> Ideal (MvPolynomial σ k)`

The first argument `k` is the coefficient field for the polynomials (the base field). The implicit argument `K` is the extension field in which the points live and where polynomials are evaluated. The `Field k` and `Field K` instances supply the field structure on `k` and `K` respectively. The `Algebra k K` instance encodes the `k`-algebra structure on `K`, making evaluation of `k`-polynomials at `K`-points well-defined. The implicit type `σ` is the index type for the variables of the polynomial ring (and the domain of each point). The explicit argument `V` is the set of points, where each point is a function `σ → K` assigning a value in `K` to each variable.

## Conventions

There are no special junk-value or edge conventions declared beyond what follows directly from the ideal structure: taking the vanishing ideal of the empty set yields the entire ring (the top ideal), since the universal condition "for all x in ∅" is vacuously true for every polynomial.

## Worked examples

- Claim: A polynomial `p` belongs to `VTask.vanishingIdeal k V` if and only if `aeval x p = 0` for every `x ∈ V`.

- Claim: `VTask.vanishingIdeal k (∅ : Set (σ → K)) = ⊤` — the vanishing ideal of the empty set is the whole polynomial ring, because every polynomial vacuously vanishes on the empty set.

- Claim: For a single point `x : σ → K`, a polynomial `p` belongs to `VTask.vanishingIdeal k {x}` if and only if `aeval x p = 0`, i.e., `p` evaluates to zero at `x`.

- Claim: If `A ⊆ B` as sets of points, then `VTask.vanishingIdeal k B ≤ VTask.vanishingIdeal k A` — the vanishing ideal is inclusion-reversing (anti-monotone) in `V`.

## Boundaries

- **Empty set**: `VTask.vanishingIdeal k ∅ = ⊤` (the top ideal, equal to the whole ring), since every polynomial vacuously satisfies the zero condition on an empty set of points.
- **Single point**: `VTask.vanishingIdeal k {x}` is a maximal ideal when `K` is algebraically closed over `k`; conversely, every maximal ideal of `MvPolynomial σ K` arises this way.
- **Galois connection**: `VTask.vanishingIdeal k` and `zeroLocus K` form a Galois connection between ideals of `MvPolynomial σ k` and sets of points in `σ → K`. In particular, `V ⊆ zeroLocus K I` if and only if `I ≤ VTask.vanishingIdeal k V`.
- **Radical**: For any ideal `I`, `VTask.vanishingIdeal k (zeroLocus K I) = I.radical` (the Nullstellensatz). In particular, `VTask.vanishingIdeal k (zeroLocus K P) = P` when `P` is a prime ideal.
- **Anti-monotonicity**: Larger sets produce smaller (or equal) vanishing ideals; the map `V ↦ VTask.vanishingIdeal k V` is order-reversing.

## Not to be confused with

- `PrimeSpectrum.vanishingIdeal`: the vanishing ideal in the prime spectrum sense, taking a set of prime ideals rather than a set of geometric points; related by the `pointToPoint` map but operates on a different domain.
- `zeroLocus K I`: the zero locus of an ideal, which goes in the opposite direction — from an ideal to a set of points; it is the left adjoint in the Galois connection where `VTask.vanishingIdeal` is the right adjoint.
- `MvPolynomial.aeval x p`: the evaluation of a single polynomial at a single point; `VTask.vanishingIdeal` collects all polynomials vanishing at *all* points of a set, not just one.
