## Object

`VTask.mkContinuous` promotes a multilinear map to a *continuous* multilinear map by supplying a bound that certifies continuity. Given a multilinear map `f : MultilinearMap 𝕜 E G` over a finitely-indexed family of normed spaces, together with a real constant `C` and a proof that the norm of every output is at most `C` times the product of the input norms, it returns the corresponding `ContinuousMultilinearMap 𝕜 E G` whose underlying multilinear map is exactly `f`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mkContinuous : {𝕜 : Type u} -> {ι : Type v} -> {E : ι → Type wE} -> {G : Type wG} -> [NontriviallyNormedField 𝕜] -> [(i : ι) → SeminormedAddCommGroup (E i)] -> [(i : ι) → NormedSpace 𝕜 (E i)] -> [SeminormedAddCommGroup G] -> [NormedSpace 𝕜 G] -> [Fintype ι] -> (f : MultilinearMap 𝕜 E G) -> (C : ℝ) -> (H : ∀ (m : (i : ι) → E i), ‖f m‖ ≤ C * ∏ i, ‖m i‖) -> ContinuousMultilinearMap 𝕜 E G
<!-- PINNED-SIGNATURE:END -->


VTask.mkContinuous : {𝕜 : Type u} -> {ι : Type v} -> {E : ι → Type wE} -> {G : Type wG} -> [NontriviallyNormedField 𝕜] -> [(i : ι) → SeminormedAddCommGroup (E i)] -> [(i : ι) → NormedSpace 𝕜 (E i)] -> [SeminormedAddCommGroup G] -> [NormedSpace 𝕜 G] -> [Fintype ι] -> (f : MultilinearMap 𝕜 E G) -> (C : ℝ) -> (H : ∀ (m : (i : ι) → E i), ‖f m‖ ≤ C * ∏ i, ‖m i‖) -> ContinuousMultilinearMap 𝕜 E G

The scalar field `𝕜` must be a nontrivially normed field (e.g. `ℝ` or `ℂ`). The index type `ι` is required to be finite. Each `E i` is a seminormed additive commutative group carrying a normed `𝕜`-module structure; `G` is the seminormed target space, also a normed `𝕜`-module. The argument `f` is the multilinear map to be promoted. The argument `C` is a real-valued bound constant. The argument `H` is the proof that for every tuple of inputs `m`, the output norm satisfies `‖f m‖ ≤ C * ∏ i, ‖m i‖`, which is exactly what is needed to guarantee continuity.

## Conventions

The constant `C` is allowed to be any real number, including negative values; a negative `C` still makes the bound trivially valid when the left-hand side is non-negative, but the resulting operator norm of the continuous multilinear map will satisfy `‖f.mkContinuous C H‖ ≤ max C 0`. When `C` is assumed non-negative, the sharper bound `‖f.mkContinuous C H‖ ≤ C` holds.

The coercion of the resulting `ContinuousMultilinearMap` back to a function is definitionally equal to `f` itself — that is, `⇑(f.mkContinuous C H) = f` — so the promoted map evaluates identically to the original.

## Worked examples

- Claim: For the zero multilinear map `(0 : MultilinearMap ℝ (fun _ : Fin 2 => ℝ) ℝ)`, calling `VTask.mkContinuous` with constant `C = 0` and the trivial bound proof yields a continuous multilinear map that still evaluates to zero on every input.

- Claim: For a multilinear map `f` satisfying `‖f m‖ ≤ 3 * ∏ i, ‖m i‖`, the operator norm of `f.mkContinuous 3 H` is at most `3`.

- Claim: When the bound constant `C` supplied to `VTask.mkContinuous` is negative, the operator norm of the result satisfies `‖f.mkContinuous C H‖ ≤ max C 0 = 0`.

## Boundaries

- **Negative `C`:** The definition accepts any real `C`. Because norms are non-negative, a negative bound is still logically consistent if `f` is the zero map, but the resulting operator norm estimate only gives `‖result‖ ≤ max C 0`.
- **`C = 0`:** Valid; the resulting continuous multilinear map must be identically zero.
- **Empty index type `ι`:** When `ι` is empty (`Fintype` with zero elements), the product `∏ i, ‖m i‖` is `1`, so the bound becomes `‖f m‖ ≤ C`, and the single input tuple is the unique element of `(i : Fin 0) → E i`.
- **Singleton `ι`:** Reduces to a bounded linear map situation; the product is just `‖m 0‖`.

## Not to be confused with

- `ContinuousMultilinearMap.mk` — the raw structure constructor for `ContinuousMultilinearMap`, which requires you to supply continuity as a hypothesis in a different form rather than deriving it from a norm bound.
- `MultilinearMap.mkContinuousLinear` — a related constructor that promotes a *linear map into multilinear maps* to a continuous object, using a bound involving an extra linear factor `‖x‖`.
- `MultilinearMap.mkContinuousMultilinear` — promotes a multilinear map whose values are themselves multilinear maps, using a product-of-products norm bound.
