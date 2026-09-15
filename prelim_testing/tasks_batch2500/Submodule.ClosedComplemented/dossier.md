## 1. Object

A submodule `p` of a topological module `M` is **closed-complemented** if there exists a continuous (i.e., bounded) linear retraction from the ambient module `M` onto `p` — that is, a continuous linear map `f : M → p` whose restriction to `p` is the identity. Geometrically, this means `M` splits, in a topologically compatible way, as a direct sum of `p` and a closed complementary submodule.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ClosedComplemented : {R : Type u_1} -> [Ring R] -> {M : Type u_2} -> [TopologicalSpace M] -> [AddCommGroup M] -> [Module R M] -> (p : Submodule R M) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.ClosedComplemented : {R : Type u_1} -> [Ring R] -> {M : Type u_2} -> [TopologicalSpace M] -> [AddCommGroup M] -> [Module R M] -> (p : Submodule R M) -> Prop`

The ring `R` is the scalar ring over which both the ambient module and the submodule are defined. The type `M` is the ambient topological module (with its ring action, additive group structure, and topology supplied by the instance arguments). The argument `p` is the specific submodule of `M` whose closed-complementedness is being asserted.

## 3. Conventions

No special junk-value or edge-case conventions are declared for this definition: it is a `Prop`-valued predicate and its truth value is determined entirely by the existence of the required continuous projection.

## 4. Worked examples

- Claim: Every finite-dimensional submodule of a locally convex Hausdorff topological vector space over a nondiscrete normed field is closed-complemented (by `VTask.ClosedComplemented.of_finiteDimensional`).

- Claim: If `f₁ : M →L[R] N` and `f₂ : N →L[R] M` satisfy `f₂ ∘ f₁ = id` (i.e., `f₂` is a left inverse of `f₁`), then the range of `f₁` is closed-complemented.

- Claim: If `p` and `q` are both closed submodules of a normed space and they are algebraically complementary (i.e., `IsCompl p q`), then `p` is closed-complemented.

- Claim: A submodule that admits a topological complement (in the sense of `IsTopCompl`) is closed-complemented.

## 5. Boundaries

- **Closed submodule:** Under mild topological separation assumptions (e.g., `T1Space` and `ContinuousSub`), a closed-complemented submodule is automatically closed as a subset of `M`. So `VTask.ClosedComplemented` implicitly forces closedness in these settings.
- **Finite-dimensional ambient space:** In finite-dimensional spaces over complete normed fields, every submodule is closed-complemented, so the predicate is vacuously true for all submodules there.
- **Finite-dimensional quotient:** If the quotient `M ⧸ p` is finite-dimensional and `p` is closed, then `p` is closed-complemented regardless of the dimension of `p` itself.
- **Submodule of a complemented submodule:** If `A` is a finite-dimensional closed-complemented submodule and `B ≤ A`, then `B` is also closed-complemented.
- **The whole module and zero submodule:** The whole module `M` and the trivial submodule `{0}` are both closed-complemented (the identity and zero maps serve as projections, respectively).

## 6. Not to be confused with

- **`IsCompl p q`**: A purely lattice-theoretic (algebraic) notion saying `p` and `q` together span `M` and intersect trivially — it does not require any topological continuity of the projection.
- **`IsTopCompl p q`**: States that a specific submodule `q` is a topological complement to `p`, meaning the two together decompose `M` continuously; `VTask.ClosedComplemented p` only asserts existence of some such complement without naming it.
- **`IsClosed (p : Set M)`**: The statement that `p` is merely a closed subset of `M`, which is a weaker condition than closed-complementedness (every closed-complemented submodule is closed, but not vice versa in general).