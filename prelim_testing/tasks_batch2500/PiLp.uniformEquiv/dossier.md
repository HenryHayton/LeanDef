## Object

`VTask.uniformEquiv p β` is the canonical uniform isomorphism (a uniform equivalence, i.e., a bijection that is uniformly continuous in both directions) between the **Lp product space** `PiLp p β` and the ordinary **dependent product type** `Π i, β i` equipped with the product uniform structure. It witnesses that, as uniform spaces, the Lp-weighted pi-type and the plain pi-type are indistinguishable—their uniform structures coincide up to the canonical re-labelling of points.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.uniformEquiv : (p : ENNReal) -> {ι : Type u_2} -> (β : ι → Type u_4) -> [(i : ι) → UniformSpace (β i)] -> PiLp p β ≃ᵤ ((i : ι) → β i)
<!-- PINNED-SIGNATURE:END -->


`VTask.uniformEquiv : (p : ENNReal) -> {ι : Type u_2} -> (β : ι → Type u_4) -> [(i : ι) → UniformSpace (β i)] -> PiLp p β ≃ᵤ ((i : ι) → β i)`

The first argument `p` is the exponent in `[1, ∞]` that parameterises the Lp structure on the product; it is an extended non-negative real. The implicit argument `ι` is the index type whose elements name the factors of the product. The argument `β` is the family of types indexed by `ι`, giving the fibre over each index. The instance argument requires each fibre `β i` to carry a uniform space structure, which is then assembled into the product uniform structure on both sides.

## Conventions

The underlying equivalence of types (forgetting uniform continuity) is exactly `WithLp.equiv p (Π i, β i)`, the canonical type-level identification between `PiLp p β` and `Π i, β i`.

## Worked examples

- Claim: For any `p` and any family `β` of uniform spaces over a finite index type, the coercion of `VTask.uniformEquiv p β` to an equivalence of types equals `WithLp.equiv p (Π i, β i)`.

- Claim: The map `(VTask.uniformEquiv p β).toFun` sends a term `x : PiLp p β` to the function `fun i => x i`, and it does so uniformly continuously.

- Claim: The inverse map `(VTask.uniformEquiv p β).invFun` sends a term `f : Π i, β i` back to the corresponding element of `PiLp p β`, and it too is uniformly continuous.

- Claim: For `ι = Fin 2`, `β = fun _ => ℝ`, and `p = 2`, the uniform equivalence `VTask.uniformEquiv 2 (fun _ : Fin 2 => ℝ)` is a valid term of type `PiLp 2 (fun _ : Fin 2 => ℝ) ≃ᵤ ((i : Fin 2) → ℝ)`.

## Boundaries

- The construction is valid for **all** extended non-negative real exponents `p : ENNReal`, including `p = 0`, `p = 1`, `p = ∞` (`⊤`), and non-integer values. No restriction on `p` is imposed.
- The index type `ι` is completely arbitrary (it need not be finite, non-empty, or have decidable equality). When `ι` is infinite, `PiLp p β` and `Π i, β i` still carry uniform structures and the equivalence remains valid.
- Each fibre `β i` merely needs a `UniformSpace` instance; no metric, norm, or topological group structure is required.
- When `ι` is empty, the equivalence degenerates to the trivial isomorphism between two one-point types.

## Not to be confused with

- `WithLp.equiv p (Π i, β i)`: the bare type equivalence without any continuity or uniform-continuity data; `VTask.uniformEquiv` bundles the additional structure asserting uniform continuity in both directions.
- `PiLp.homeomorph` (or the analogous topological isomorphism): a homeomorphism records continuity in both directions but is weaker than a uniform equivalence, which also preserves Cauchy filters and uniform covers.
- `PiLp.linearEquiv` or `PiLp.isometryEquiv`: linear or isometric equivalences between Lp product spaces that carry additional algebraic or metric structure beyond uniform continuity.