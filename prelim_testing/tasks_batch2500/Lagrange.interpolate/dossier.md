## Object

Given a finite index set `s`, a nodal map `v` (which should be injective on `s`), and a value function `r`, `VTask.interpolate s v` is the **Lagrange interpolation linear map**: it sends `r` to the unique polynomial of degree strictly less than `#s` whose value at `v i` equals `r i` for every `i ∈ s`. The construction packages the classical Lagrange interpolation formula as an `F`-linear map from value functions to polynomials.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.interpolate : {F : Type u_1} -> [Field F] -> {ι : Type u_2} -> [DecidableEq ι] -> (s : Finset ι) -> (v : ι → F) -> (ι → F) →ₗ[F] Polynomial F
<!-- PINNED-SIGNATURE:END -->


`VTask.interpolate : {F : Type u_1} -> [Field F] -> {ι : Type u_2} -> [DecidableEq ι] -> (s : Finset ι) -> (v : ι → F) -> (ι → F) →ₗ[F] Polynomial F`

- `F` is the coefficient field over which the polynomials are defined and in which the node values live.
- The `Field F` instance supplies the field arithmetic needed for Lagrange basis construction.
- `ι` is the index type labelling the interpolation nodes.
- The `DecidableEq ι` instance enables decidable equality on indices, required for finset membership tests.
- `s` is the finite set of indices whose images under `v` serve as the interpolation nodes.
- `v` is the nodal map assigning to each index `i : ι` its node position `v i : F`; it is required to be injective on `s` for the interpolation to be well-posed and yield the unique low-degree interpolant.
- The result is an `F`-linear map: given a value function `r : ι → F`, it returns the interpolating polynomial in `F[X]`.

## Conventions

When `v` is not injective on `s`, the polynomial produced is still well-defined as a formal sum of Lagrange basis polynomials (the construction does not check injectivity), but the uniqueness and exact-interpolation guarantees no longer hold. The output is still a polynomial, merely not the canonical interpolant.

When `s` is the empty finset, the sum over `s` is empty, so `VTask.interpolate ∅ v r = 0` (the zero polynomial) for every `v` and `r`.

## Worked examples

- Claim: For `s = {0, 1}` with nodes `v 0 = 0`, `v 1 = 1` over `ℚ`, and values `r 0 = 3`, `r 1 = 7`, the interpolating polynomial evaluated at `0` is `3` and at `1` is `7`.

- Claim: For `s = ∅` and any `v`, `r`, the polynomial `VTask.interpolate ∅ v r` equals the zero polynomial `0`.

- Claim: For a singleton `s = {i}` with node `v i = a` and value `r i = c`, the interpolating polynomial is the constant polynomial `C c`.

- Claim: `VTask.interpolate s v` is `F`-linear, meaning `VTask.interpolate s v (r₁ + r₂) = VTask.interpolate s v r₁ + VTask.interpolate s v r₂` for all value functions `r₁`, `r₂`.

## Boundaries

- **Empty index set (`s = ∅`)**: The interpolating polynomial is the zero polynomial `0`, since the sum over the empty set is `0`.
- **Singleton (`#s = 1`)**: The result is a constant polynomial taking value `r i` at node `v i`.
- **Non-injective `v` on `s`**: The map is still defined and `F`-linear, but the output polynomial may not satisfy the interpolation conditions; uniqueness and the evaluation property at nodes can fail.
- **Degree bound**: When `v` is injective on `s`, the output polynomial has degree strictly less than `#s`.
- **Linear structure**: Scaling the value function by a scalar scales the polynomial accordingly; adding value functions adds the polynomials.

## Not to be confused with

- `Lagrange.basis s v i`: The individual Lagrange basis polynomial for a single index `i`; `VTask.interpolate` combines all basis polynomials weighted by the value function into a single interpolant.
- `Polynomial.eval a p`: Evaluating a polynomial at a point; `VTask.interpolate` *constructs* a polynomial from node-value data, rather than evaluating one.
- A bare finset sum of basis polynomials: `VTask.interpolate s v` is the full `F`-linear map packaged with linearity proofs, not merely the underlying function.