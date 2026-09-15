## Object

Given a semilinear map `f : M →ₛₗ[σ] M₃` and a bare function `f' : M → M₃` that is provably equal to the underlying function of `f`, `VTask.copy` produces a new semilinear map whose underlying function is definitionally `f'` rather than `⇑f`. The resulting semilinear map is equal to `f` as a semilinear map, but its `toFun` field is filled in by `f'`. This is useful when `f'` and `⇑f` are propositionally but not definitionally equal, and one wants the new map to reduce to `f'` without unfolding.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {R : Type u_1} -> {S : Type u_5} -> {M : Type u_8} -> {M₃ : Type u_11} -> [Semiring R] -> [Semiring S] -> [AddCommMonoid M] -> [AddCommMonoid M₃] -> [Module R M] -> [Module S M₃] -> {σ : R →+* S} -> (f : M →ₛₗ[σ] M₃) -> (f' : M → M₃) -> (h : f' = ⇑f) -> M →ₛₗ[σ] M₃
<!-- PINNED-SIGNATURE:END -->


The first argument `f` is the semilinear map being copied. The second argument `f'` is the new underlying function to install. The third argument `h` is a proof that `f'` equals the coercion of `f` to a function; this proof is used to transfer the linearity properties from `f` to the new map built around `f'`.

## Conventions

There are no junk-value or out-of-domain conventions for this definition: it is total and well-typed for any `f`, `f'`, and proof `h` of the required equality.

## Worked examples

- Claim: For any semilinear map `f`, calling `VTask.copy f (⇑f) rfl` yields a semilinear map whose coercion to a function is `⇑f`.

- Claim: For any semilinear map `f` and any `f'` with `h : f' = ⇑f`, the copy `VTask.copy f f' h` is equal to `f` as a semilinear map (i.e., `VTask.copy f f' h = f`).

- Claim: For any semilinear map `f` and any `f'` with `h : f' = ⇑f`, the coercion `⇑(VTask.copy f f' h)` is definitionally `f'`.

## Boundaries

- The proof `h` must go in the direction `f' = ⇑f` (not `⇑f = f'`); swapping would require `h.symm`.
- When `f' = ⇑f` is chosen as `rfl` (i.e., `f'` is literally `⇑f`), the copy is trivially equal to `f` and the construction adds no real information.
- The copy does not produce a new mathematical object: `VTask.copy f f' h = f` holds unconditionally, so the only effect is on definitional equality of the underlying function field.
- Both the additive and scalar-multiplication structures are inherited from `f` via the proof `h`, so linearity is fully preserved.

## Not to be confused with

- `LinearMap.mk`: constructs a semilinear map from scratch by providing a function and proofs of both linearity axioms, without reference to an existing map.
- `LinearMap.toFun` (coercion `⇑f`): merely extracts the underlying function from a semilinear map; does not produce a new semilinear map.
- `Function.funext_iff`-style extensionality: two semilinear maps are equal iff their coercions agree pointwise; `VTask.copy` is about changing the *definitional* representation of `toFun`, not about a new pointwise-different map.