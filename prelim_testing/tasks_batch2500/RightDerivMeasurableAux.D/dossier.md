## Object

`VTask.D f K` is a subset of the real line constructed by a countable intersection-union-intersection procedure using auxiliary approximation sets. Its defining property — the reason it is introduced — is that it serves as a measurability-friendly proxy for the set of right-differentiability points of `f` whose right derivative lands in `K`. When `K` is a complete subset of `F`, the set `VTask.D f K` coincides exactly with `{ x | f is right-differentiable at x and derivWithin f (Ici x) x ∈ K }`; for general `K` it is a superset of that set.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.D : {F : Type u_1} -> [NormedAddCommGroup F] -> [NormedSpace ℝ F] -> (f : ℝ → F) -> (K : Set F) -> Set ℝ
<!-- PINNED-SIGNATURE:END -->


`VTask.D : {F : Type u_1} -> [NormedAddCommGroup F] -> [NormedSpace ℝ F] -> (f : ℝ → F) -> (K : Set F) -> Set ℝ`

The implicit type `F` is the Banach-space-valued codomain; the two instance arguments equip it with a norm and with scalar multiplication by reals. The argument `f` is the function from `ℝ` into `F` whose right-differentiability is being studied. The argument `K` is a subset of `F` that restricts which derivative values are admitted — the returned set only contains points where the right derivative of `f` (when it exists) belongs to `K`.

## Conventions

There are no junk-value conventions declared for this definition: it is a total function on all inputs `f` and `K`, and the countable-intersection-union construction produces a well-defined subset of `ℝ` for every choice of `f` and `K` without any side conditions.

## Worked examples

- Claim: For any `f : ℝ → F` and any complete set `K : Set F`, the set `VTask.D f K` equals `{ x | DifferentiableWithinAt ℝ f (Ici x) x ∧ derivWithin f (Ici x) x ∈ K }`.

- Claim: For any `f : ℝ → F` and any (possibly non-complete) `K : Set F`, every point `x` at which `f` is right-differentiable with derivative in `K` belongs to `VTask.D f K`; that is, `{ x | DifferentiableWithinAt ℝ f (Ici x) x ∧ derivWithin f (Ici x) x ∈ K } ⊆ VTask.D f K`.

- Claim: If `K = ∅`, then `VTask.D f K` may still be nonempty in general (because the inclusion direction `D ⊆ differentiable set` requires `K` to be complete); once `K = ∅` is given the discrete (hence complete) topology the equality `VTask.D f ∅ = ∅` holds.

- Claim: If `f` is the constant function `fun _ => (0 : F)` and `K` is any complete set containing `0`, then every `x : ℝ` belongs to `VTask.D f K`.

## Boundaries

- When `K` is complete, `VTask.D f K` is precisely the right-differentiability set of `f` with derivative constraint `K`; completeness is the exact threshold for the two inclusions to combine into an equality.
- When `K` is not complete, `VTask.D f K` is still a well-defined set of reals and contains the right-differentiability set with derivative in `K`, but may be strictly larger.
- The set `VTask.D f K` is always a Borel-measurable subset of `ℝ` (it is built by countable intersections and unions of open sets, or of sets obtained from open sets by similar operations), which is its primary motivation.
- The construction uses only right-differentiability (differentiability within `[x, ∞)`), not two-sided differentiability.

## Not to be confused with

- The auxiliary set `B f K r s e` (the building block used inside the countable operations): `VTask.D f K` is the global set assembled from those approximation pieces, not a single piece.
- `{ x | DifferentiableAt ℝ f x }` (two-sided differentiability set): `VTask.D f K` tracks one-sided (right) differentiability within `Ici x`, not full Fréchet differentiability.
- `VTask.D f Set.univ`: removing the derivative constraint by taking `K = Set.univ` gives the full right-differentiability set, but this is a special case; in general `K` can be any subset of `F`.