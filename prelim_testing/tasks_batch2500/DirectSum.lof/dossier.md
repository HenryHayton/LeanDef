## Object

For each index `i` in an index type `ι`, `VTask.lof R ι M i` is the canonical linear inclusion map that embeds the `i`-th component `M i` into the direct sum `⨁ i, M i`. It sends an element `x : M i` to the element of the direct sum that equals `x` in position `i` and is zero in every other position.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lof : (R : Type u) -> [Semiring R] -> (ι : Type v) -> (M : ι → Type w) -> [(i : ι) → AddCommMonoid (M i)] -> [(i : ι) → Module R (M i)] -> [DecidableEq ι] -> (i : ι) -> M i →ₗ[R] DirectSum ι fun i => M i
<!-- PINNED-SIGNATURE:END -->


The type string is inserted automatically above. `R` is the commutative semiring of scalars. `ι` is the index type over which the direct sum is taken. `M` is the family of `R`-modules indexed by `ι`. The final argument `i : ι` specifies which component is being included; the result is a linear map from the single component `M i` into the whole direct sum.

## Conventions

No special junk-value or boundary conventions are declared for this definition: it is a total construction that is well-defined for every valid choice of `R`, `ι`, `M`, and `i`.

## Worked examples

- Claim: `VTask.lof ℤ (Fin 3) (fun _ => ℤ) 1` is a linear map from `ℤ` to `⨁ _ : Fin 3, ℤ`, and applying it to `5` yields the element that is `5` at index `1` and `0` elsewhere.

- Claim: `VTask.lof ℤ (Fin 2) (fun _ => ℤ) 0` applied to `x` and `VTask.lof ℤ (Fin 2) (fun _ => ℤ) 1` applied to `y` produce two elements of `⨁ _ : Fin 2, ℤ` whose sum has coordinate `0` equal to `x` and coordinate `1` equal to `y`.

- Claim: For any `i : ι`, the `i`-th component of `VTask.lof R ι M i x` is `x`, and for any `j ≠ i`, the `j`-th component is `0`.

- Claim: `VTask.lof R ι M i` is injective as a linear map for any choice of `R`, `ι`, `M`, and `i`.

## Boundaries

- When `ι` has exactly one element, the direct sum `⨁ i, M i` is essentially just `M i`, and `VTask.lof R ι M i` is an isomorphism (though it is typed as an inclusion).
- When `M i` is the trivial module (the zero module), the inclusion map is the zero linear map; it is still well-defined.
- The definition requires `DecidableEq ι` so that the construction can determine whether two indices are equal or not; this is needed to define the zero-elsewhere behavior precisely.
- The map is always `R`-linear regardless of what `M i` or the other components look like.

## Not to be confused with

- `DirectSum.component R ι M i` (or the `i`-th projection): the map going the *opposite* direction, from the direct sum to `M i`.
- `DirectSum.liftAddHom` / `DirectSum.toModule`: the universal property maps that assemble a family of maps *out of* the direct sum, rather than *into* it.
- `DirectSum.of` (the `AddMonoid`-level version): the underlying additive group homomorphism performing the same inclusion but without the `R`-linear structure.