## Object

`VTask.lift` constructs a single `R`-linear map from a module `M` into the `I`-adic completion of `N`, given a *compatible family* of linear maps from `M` to the successive quotients `N / (I^n • N)`. Compatibility means that as `n` grows the maps fit together coherently: applying the canonical projection that reduces the `n`-th quotient to the `m`-th quotient (for `m ≤ n`) before applying the `n`-th map gives the same result as just applying the `m`-th map. The construction realises the universal property of the inverse limit: a compatible family factors uniquely through the completion.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lift : {R : Type u_1} -> [CommRing R] -> (I : Ideal R) -> {M : Type u_4} -> [AddCommGroup M] -> [Module R M] -> {N : Type u_5} -> [AddCommGroup N] -> [Module R N] -> (f : (n : ℕ) → M →ₗ[R] N ⧸ I ^ n • ⊤) -> (h : ∀ {m n : ℕ} (hle : m ≤ n), AdicCompletion.transitionMap I N hle ∘ₗ f n = f m) -> M →ₗ[R] AdicCompletion I N
<!-- PINNED-SIGNATURE:END -->


`VTask.lift : {R : Type u_1} -> [CommRing R] -> (I : Ideal R) -> {M : Type u_4} -> [AddCommGroup M] -> [Module R M] -> {N : Type u_5} -> [AddCommGroup N] -> [Module R N] -> (f : (n : ℕ) → M →ₗ[R] N ⧸ I ^ n • ⊤) -> (h : ∀ {m n : ℕ} (hle : m ≤ n), AdicCompletion.transitionMap I N hle ∘ₗ f n = f m) -> M →ₗ[R] AdicCompletion I N`

`R` is the commutative base ring; `I` is an ideal of `R` that determines the filtration and hence the completion. `M` is the source `R`-module whose elements are to be mapped. `N` is the target `R`-module whose `I`-adic completion is the codomain. `f` is the compatible family: for each natural number `n`, a linear map from `M` to the quotient `N / (I^n • N)`. `h` is the coherence hypothesis: for each pair of natural numbers `m ≤ n`, composing `f n` with the transition map (which projects the finer quotient `N / I^n • N` onto the coarser `N / I^m • N`) yields `f m`.

## Conventions

No special junk-value or edge conventions are declared for this definition: the map is well-defined for all valid inputs including `n = 0` (where `I^0 • N = N` so the quotient is trivial), and the construction is total on all families satisfying the coherence hypothesis.

## Worked examples

- Claim: For a compatible family `f` and any `x : M`, the `n`-th component of `VTask.lift I f h x` in the completion equals `f n x`.

- Claim: If `f` is constantly the zero map (all `f n = 0`), then `VTask.lift I f h = 0` as a linear map `M →ₗ[R] AdicCompletion I N`, because every component of the image is zero.

- Claim: Composing the evaluation map `eval I N n` (which projects the completion onto the `n`-th quotient) with `VTask.lift I f h` recovers `f n`, i.e., `eval I N n ∘ₗ VTask.lift I f h = f n`.

## Boundaries

- At `n = 0`: the quotient `N / (I^0 • N)` equals `N / N = 0` (since `I^0 = 1` and `1 • N = N`), so `f 0` necessarily lands in the zero module; the compatibility condition at `m = 0 ≤ n` is vacuously satisfied for the zero map component.
- The coherence condition `h` is a strict input requirement; without it, the family does not define a coherent element of the inverse limit. There is no fallback or junk value: the signature requires the proof `h` to be supplied.
- When `M = N` and the maps `f n` are the canonical projections `N → N / I^n • N`, the result is the natural map of `N` into its own `I`-adic completion.

## Not to be confused with

- `AdicCompletion.transitionMap I N hle`: this is a single linear map between two consecutive quotient levels, not a map into the completion.
- `IsAdicComplete.of I N`: this is the canonical map from `N` into its completion when `N` already carries a complete `I`-adic structure; it does not take a compatible family.
- `AdicCompletion.liftRingHom`: an analogous universal construction for *ring* maps into the `I`-adic completion of a ring, rather than linear maps between modules.