## VTask.decompEquiv

### Object

A canonical bijection (equivalence of types) between the space of continuous affine maps from a topological `R`-vector space `V` to a topological affine space `Q` (modelled on a topological `R`-module `W`) on the one hand, and the Cartesian product `Q × (V →L[R] W)` on the other. The bijection sends each continuous affine map `f` to the pair consisting of its value at the origin `f(0) ∈ Q` and its continuous linear part `f.contLinear : V →L[R] W`, and reconstructs `f` uniquely from any such pair.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.decompEquiv : (R : Type u_1) -> (V : Type u_3) -> {W : Type u_4} -> (Q : Type u_5) -> [Ring R] -> [AddCommGroup V] -> [Module R V] -> [TopologicalSpace V] -> [IsTopologicalAddGroup V] -> [AddCommGroup W] -> [Module R W] -> [TopologicalSpace W] -> [AddTorsor W Q] -> [TopologicalSpace Q] -> [IsTopologicalAddTorsor Q] -> (V →ᴬ[R] Q) ≃ Q × (V →L[R] W)
<!-- PINNED-SIGNATURE:END -->


`VTask.decompEquiv : (R : Type u_1) -> (V : Type u_3) -> {W : Type u_4} -> (Q : Type u_5) -> [Ring R] -> [AddCommGroup V] -> [Module R V] -> [TopologicalSpace V] -> [IsTopologicalAddGroup V] -> [AddCommGroup W] -> [Module R W] -> [TopologicalSpace W] -> [AddTorsor W Q] -> [TopologicalSpace Q] -> [IsTopologicalAddTorsor Q] -> (V →ᴬ[R] Q) ≃ Q × (V →L[R] W)`

- `R` is the commutative ring of scalars over which the vector and affine spaces are defined.
- `V` is the source topological `R`-module (i.e., a topological vector space over `R`); it carries the domain of the affine maps.
- `W` (implicit) is the model vector space for the affine space `Q`; it is the `R`-module over which `Q` is an affine torsor, and its topology must be compatible with the module structure.
- `Q` is the target topological affine space, viewed as an `AddTorsor` over `W`; continuous affine maps land in `Q`.
- The typeclass instances supply the ring, additive group, module, and topological structure on each of the spaces involved, as well as the compatibility conditions (topological group/torsor requirements).

### Conventions

No special junk-value or out-of-domain conventions are declared: the equivalence is a total bijection defined on all continuous affine maps `V →ᴬ[R] Q` and all pairs in `Q × (V →L[R] W)`, with no edge cases requiring special treatment.

### Worked examples

- Claim: For any continuous affine map `f : V →ᴬ[R] Q`, the forward component of `VTask.decompEquiv R V Q` applied to `f` yields the pair `(f 0, f.contLinear)`.

- Claim: For a continuous affine map `f : V →ᴬ[R] Q`, the composition `(VTask.decompEquiv R V Q).symm ((VTask.decompEquiv R V Q) f) = f` holds, witnessing that the forward and inverse maps are mutual inverses.

- Claim: For any pair `(q, L)` with `q : Q` and `L : V →L[R] W`, applying `(VTask.decompEquiv R V Q).symm (q, L)` and then the forward map recovers `(q, L)`, i.e., the right inverse property holds.

### Boundaries

- When `V = 0` (the trivial module), every continuous affine map is entirely determined by its value at the unique point `0 : V`, so the linear part is the zero map and the bijection reduces to an identification of `(V →ᴬ[R] Q)` with `Q × {0}`.
- When `Q = W` (so `Q` is itself the model vector space, viewed as an affine space over itself), the bijection specialises to an identification of continuous affine maps `V →ᴬ[R] W` with `W × (V →L[R] W)`, recording the translation part and the linear part separately.
- The equivalence is a bijection of bare types (not necessarily of topological spaces or vector spaces), unless additional structure is imposed on top.

### Not to be confused with

- `ContinuousAffineMap.contLinear`: this is merely the projection extracting the linear part of a single affine map, not the full equivalence.
- The decomposition of an affine map in the non-continuous (algebraic) setting: `VTask.decompEquiv` specifically requires and records the continuity of both the affine map and the resulting linear map.
- `ContinuousLinearMap.toAffine` or related coercions: those go from linear maps to affine maps (a one-sided embedding), whereas `VTask.decompEquiv` is a two-sided bijection accounting for all affine maps via both a base point in `Q` and a linear part.