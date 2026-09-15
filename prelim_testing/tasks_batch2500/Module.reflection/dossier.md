## Object

A **reflection** in a module is the linear automorphism determined by an element `x` of a module `M` and a linear functional `f : M → R` satisfying `f(x) = 2`. It is the map `y ↦ y − (f y) · x`. This is an involution (applying it twice is the identity) that fixes every element of the kernel of `f` and sends `x` to `−x`. The normalization condition `f(x) = 2` is the standard one coming from root-system theory (it ensures the map is genuinely an involution rather than merely idempotent or trivial).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.reflection : {R : Type u_1} -> {M : Type u_2} -> [CommRing R] -> [AddCommGroup M] -> [Module R M] -> {x : M} -> {f : Module.Dual R M} -> (h : f x = 2) -> M ≃ₗ[R] M
<!-- PINNED-SIGNATURE:END -->


`VTask.reflection : {R : Type u_1} -> {M : Type u_2} -> [CommRing R] -> [AddCommGroup M] -> [Module R M] -> {x : M} -> {f : Module.Dual R M} -> (h : f x = 2) -> M ≃ₗ[R] M`

`R` is the commutative ring of scalars. `M` is the module over `R` in which the reflection lives. `x` is the distinguished element of `M` that gets sent to `−x` (the "root" direction). `f` is the linear functional on `M` whose kernel is the hyperplane fixed by the reflection. `h` is the proof of the normalization condition `f x = 2`, which is required to make the map an involution.

## Conventions

The normalization `f x = 2` (rather than `f x = 1`) is the standard algebraic convention matching root-system usage; it is baked in as a hypothesis rather than rescaling automatically.

## Worked examples

- Claim: For `R = ℤ`, `M = ℤ²`, `x = (1, 0)`, and `f = (a, b) ↦ 2a` (so `f x = 2`), the reflection sends `(a, b)` to `(a − 2a, b) = (−a, b)`, i.e., it is reflection across the second coordinate axis.

- Claim: For `R = ℝ`, `M = ℝ`, `x = 1`, `f = (· * 2)` (so `f x = 2`), the reflection map is `y ↦ y − 2y = −y`, which is the negation map on `ℝ`.

- Claim: Applying `VTask.reflection h` twice to any element `y : M` returns `y`, i.e., the map is an involution (its own inverse).

- Claim: For any `y : M` with `f y = 0`, the reflection fixes `y`, since `y − (f y) • x = y − 0 • x = y`.

## Boundaries

- The condition `f x = 2` is not automatic; the caller must supply the proof `h`. If `f x ≠ 2` the construction is simply unavailable (the type of `h` cannot be inhabited).
- When `x = 0` (the zero element), the reflection is always the identity map (since `(f y) • 0 = 0` for all `y`), but this case requires `f 0 = 2`, which in a linear functional is impossible because `f 0 = 0`; so `x = 0` cannot arise.
- The map is a linear *equivalence* (`M ≃ₗ[R] M`), not merely a linear map; its inverse is itself (involutivity).
- Elements in `ker f` are exactly the fixed points of the reflection.

## Not to be confused with

- `Module.Dual.preReflection`: the underlying linear *map* `y ↦ y − (f y) • x` without the bundled invertibility/involutive structure; `VTask.reflection` packages this map together with its inverse into a linear equivalence.
- Orthogonal reflections in inner-product spaces: those require an inner product to define `f` from `x`; `VTask.reflection` works for any module with any linear functional satisfying the normalization, with no metric structure assumed.
- Transvections (shear maps): those fix a hyperplane but do not send a distinguished vector to its negative; they are not involutions in general.