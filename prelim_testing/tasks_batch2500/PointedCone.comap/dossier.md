## Object

`VTask.comap f C` is the **preimage pointed cone**: given an `R`-linear map `f : E →ₗ[R] F` and a pointed cone `C` in `F`, it is the set of all vectors `x ∈ E` such that `f x ∈ C`, equipped with the pointed-cone structure inherited from `C`. Because `C` is a pointed cone (closed under non-negative scalar multiplication and containing zero), and `f` is linear, the preimage automatically carries the same structure, making it a legitimate pointed cone in `E`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comap : {R : Type u_1} -> {E : Type u_2} -> {F : Type u_3} -> [Semiring R] -> [PartialOrder R] -> [IsOrderedRing R] -> [AddCommMonoid E] -> [Module R E] -> [AddCommMonoid F] -> [Module R F] -> (f : E →ₗ[R] F) -> (C : PointedCone R F) -> PointedCone R E
<!-- PINNED-SIGNATURE:END -->


`(f : E →ₗ[R] F)` — the `R`-linear map along which the preimage is taken; it is the map whose fibers determine membership in the resulting cone.
`(C : PointedCone R F)` — the pointed cone in the codomain `F` whose preimage is being formed.

The type-class arguments supply the ordered semiring structure on the scalar ring `R`, and the module structures on `E` and `F` needed for linearity and cone axioms to be meaningful.

## Conventions

No special junk-value or edge-case conventions are declared for this definition: it is a total construction on well-typed inputs and every valid pair `(f, C)` yields a well-formed pointed cone.

## Worked examples

- Claim: The zero vector of `E` always belongs to `VTask.comap f C` for any linear map `f` and pointed cone `C`, because every pointed cone contains the origin and `f 0 = 0 ∈ C`.

- Claim: If `C` is the entire space (the top pointed cone in `F`), then `VTask.comap f C` equals the top pointed cone in `E`, since every vector in `E` maps into `C`.

- Claim: For the zero map `f = 0 : E →ₗ[R] F`, the comap of any pointed cone `C` is all of `E` (the top cone), because `f x = 0 ∈ C` for every `x : E`.

- Claim: Membership characterisation — `x ∈ VTask.comap f C` if and only if `f x ∈ C`.

## Boundaries

- When `f` is the zero map, the preimage is the entire module `E` (as a pointed cone), regardless of `C`, because `0` belongs to every pointed cone.
- When `C` is the trivial pointed cone `{0}`, the preimage `VTask.comap f C` is the kernel of `f` (as a pointed cone, i.e. the submodule `ker f`).
- When `f` is the identity map, `VTask.comap f C` equals `C` itself (viewed inside `E = F`).
- The construction is contravariant: if `C ≤ C'` then `VTask.comap f C ≤ VTask.comap f C'`; and for a composition `g ∘ f`, the comap satisfies `VTask.comap (g ∘ f) C = VTask.comap f (VTask.comap g C)`.

## Not to be confused with

- `PointedCone.map f C` — the *image* (direct image / pushforward) of a pointed cone along `f`, which gives the cone spanned by `f '' C` in `F`; comap goes in the opposite direction.
- `Submodule.comap` — the underlying submodule-level preimage; `VTask.comap` lifts this to the pointed-cone layer, preserving the pointed-cone type.
- `ConvexCone.comap` — the analogous preimage construction for convex cones (without the pointed/apex-at-zero requirement); not the same type.