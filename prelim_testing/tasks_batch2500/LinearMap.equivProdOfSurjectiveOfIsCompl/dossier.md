## Object

Given two surjective linear maps `f : E →ₗ[R] F` and `g : E →ₗ[R] G` whose kernels are complementary submodules of `E` (i.e., their kernels intersect trivially and together span all of `E`), this construction produces a linear equivalence `E ≃ₗ[R] F × G` whose underlying map is `x ↦ (f x, g x)`. In other words, the two maps together "coordinatise" `E` by the two quotient spaces `F` and `G`, and the hypothesis that the kernels are complementary is precisely what makes this coordinatisation bijective.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.equivProdOfSurjectiveOfIsCompl : {R : Type u_1} -> [Ring R] -> {E : Type u_2} -> [AddCommGroup E] -> [Module R E] -> {F : Type u_3} -> [AddCommGroup F] -> [Module R F] -> {G : Type u_4} -> [AddCommGroup G] -> [Module R G] -> (f : E →ₗ[R] F) -> (g : E →ₗ[R] G) -> (hf : f.range = ⊤) -> (hg : g.range = ⊤) -> (hfg : IsCompl f.ker g.ker) -> E ≃ₗ[R] F × G
<!-- PINNED-SIGNATURE:END -->


`VTask.equivProdOfSurjectiveOfIsCompl : {R : Type u_1} -> [Ring R] -> {E : Type u_2} -> [AddCommGroup E] -> [Module R E] -> {F : Type u_3} -> [AddCommGroup F] -> [Module R F] -> {G : Type u_4} -> [AddCommGroup G] -> [Module R G] -> (f : E →ₗ[R] F) -> (g : E →ₗ[R] G) -> (hf : f.range = ⊤) -> (hg : g.range = ⊤) -> (hfg : IsCompl f.ker g.ker) -> E ≃ₗ[R] F × G`

The implicit type arguments `R`, `E`, `F`, `G` are the scalar ring and the three module types; their algebraic structure instances are inferred automatically. `f` is the first linear map, into `F`, which will become the first component of the product. `g` is the second linear map, into `G`, which becomes the second component. `hf` is the proof that `f` is surjective (equivalently, its range equals the top submodule of `F`). `hg` is the analogous surjectivity proof for `g`. `hfg` is the proof that the kernel of `f` and the kernel of `g` are complementary submodules of `E`, meaning their meet is the zero submodule and their join is all of `E`.

## Conventions

There are no junk-value conventions to declare: the construction is only exposed when all five hypotheses (`hf`, `hg`, `hfg`) are explicitly supplied, so the result is always a well-defined linear equivalence. No sentinel or degenerate output is produced for edge inputs.

## Worked examples

- Claim: Applying `VTask.equivProdOfSurjectiveOfIsCompl f g hf hg hfg` to any element `x : E` yields `(f x, g x)` in `F × G`.

  This follows directly from the apply lemma `equivProdOfSurjectiveOfIsCompl_apply`: for every `x`, the value of the equivalence at `x` is the pair `(f x, g x)`.

- Claim: The underlying linear map (coercion to `E →ₗ[R] F × G`) of `VTask.equivProdOfSurjectiveOfIsCompl f g hf hg hfg` equals the product map `f.prod g`.

  This is recorded as `coe_equivProdOfSurjectiveOfIsCompl`: the bundled equivalence, when coerced to a linear map, is exactly the product linear map `f.prod g` sending `x` to `(f x, g x)`.

- Claim: When `R = ℝ`, `E = ℝ²`, `F = ℝ`, `G = ℝ`, `f = fst` (projection onto first coordinate), and `g = snd` (projection onto second coordinate), the resulting equivalence `VTask.equivProdOfSurjectiveOfIsCompl fst snd hf hg hfg` sends `(a, b)` to `((a), (b))`, recovering the identity (up to the canonical isomorphism `ℝ² ≃ ℝ × ℝ`).

- Claim: If the two linear maps `f` and `g` each have kernels that are complementary, then the linear equivalence produced is bijective, i.e., both injective and surjective as a function `E → F × G`.

  Bijectivity is the defining property of a linear equivalence; surjectivity of `f.prod g` follows from surjectivity of each component, and injectivity follows from the complementary-kernel condition `hfg` (the intersection of the kernels being zero means the joint kernel is trivial).

## Boundaries

- When `E = 0` (the zero module), both `f` and `g` are trivially surjective only if `F = 0` and `G = 0` as well, and `IsCompl ⊥ ⊥` holds in the lattice of submodules of `0`. In this degenerate case the equivalence is the unique map from the zero module to `0 × 0`.
- The condition `IsCompl f.ker g.ker` is strictly necessary: if the kernels overlap non-trivially, injectivity of `x ↦ (f x, g x)` fails; if their join falls short of `E`, surjectivity fails. Both defects are excluded by hypothesis.
- The construction works for any ring `R` (not necessarily commutative or a field); no finite-dimensionality or Noetherian hypothesis is assumed.
- There is no assumption that `f.ker` and `g.ker` are each individually trivial; they merely need to be complementary.

## Not to be confused with

- `LinearMap.prod f g : E →ₗ[R] F × G` — this is just the underlying linear map `x ↦ (f x, g x)` without the equivalence structure; it requires no surjectivity or complementary-kernel hypotheses.
- `Submodule.IsCompl` / direct-sum decomposition — decomposing `E` itself as a direct sum of two complementary submodules is a different (though related) construction; here the two subspaces involved are the kernels, not summands.
- `LinearEquiv.prodComm` or `LinearEquiv.prod` — these construct equivalences between product types from component equivalences, rather than from a pair of surjective maps with complementary kernels.