## Object

`VTask.mkOfNNDistEq` constructs a **dilation** — a map between pseudo-metric spaces that scales all distances by a fixed positive factor — from a bare function together with a proof that the function uniformly scales non-negative distances (expressed via `nndist`, the non-negative-real-valued distance function). Concretely, a dilation `α →ᵈ β` is a bundled map that possesses a nonzero scaling ratio `r : ℝ≥0` such that `nndist (f x) (f y) = r * nndist x y` for every pair of points. This constructor is the `nndist`-flavoured alternative to the primary dilation constructor, which works with the extended distance `edist`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mkOfNNDistEq : {α : Type u_5} -> {β : Type u_6} -> [PseudoMetricSpace α] -> [PseudoMetricSpace β] -> (f : α → β) -> (h : ∃ r, r ≠ 0 ∧ ∀ (x y : α), nndist (f x) (f y) = r * nndist x y) -> α →ᵈ β
<!-- PINNED-SIGNATURE:END -->


The first two implicit arguments fix the source type `α` and target type `β`. The next two instance arguments supply pseudo-metric-space structures on `α` and `β` respectively, providing the `nndist` and `edist` functions used in the construction. The explicit argument `f` is the underlying set-theoretic function from `α` to `β` that one wishes to promote to a dilation. The explicit argument `h` is an existence proof: it asserts that there is a nonzero `r : ℝ≥0` such that `nndist (f x) (f y) = r * nndist x y` holds for every pair of points `x y : α`. This proof is exactly the scaling condition that makes `f` a dilation.

## Conventions

No special junk-value or boundary conventions are declared for this definition: it is a constructor whose inputs are constrained by the hypothesis `h`, so every well-typed application yields a genuine dilation; there are no out-of-domain inputs to assign junk values to.

## Worked examples

- Claim: The underlying function of `VTask.mkOfNNDistEq f h` is definitionally equal to `f`; that is, coercing the resulting dilation back to a bare function recovers `f`.

- Claim: If `f : α →ᵈ β` is already a dilation with `nndist`-scaling witness `h`, then `VTask.mkOfNNDistEq f h` equals `f` as a dilation (round-trip property: packaging an existing dilation's underlying function with its own scaling proof returns the original dilation).

- Claim: For the identity function `id : α → α` on any pseudo-metric space `α`, the pair `⟨1, one_ne_zero, fun x y => (one_mul _).symm⟩` is a valid witness, so `VTask.mkOfNNDistEq id ⟨1, one_ne_zero, fun x y => (one_mul _).symm⟩` constructs the identity dilation on `α`.

## Boundaries

- The ratio `r` in the hypothesis is required to be **nonzero** (`r ≠ 0`). A zero ratio is excluded; the definition is not applicable when `r = 0`.
- If the source space is trivial (all distances are 0), any nonzero `r` satisfies the scaling condition, but `r` must still be supplied and proved nonzero.
- The pseudo-metric spaces need not be metric spaces (the triangle-inequality strictness and point-separation axioms are not required), so constant maps on degenerate spaces can validly be dilations.
- The type of `r` is `ℝ≥0` (non-negative reals), so negative ratios are not representable and cannot appear as the scaling factor.

## Not to be confused with

- `Dilation.mk` (the primary bundled constructor expecting an `edist`-based scaling hypothesis rather than an `nndist`-based one).
- `Isometry` (a map that preserves distances exactly, corresponding to the special case `r = 1`; it is a stronger notion than a general dilation).
- `AffineMap` (a map that preserves affine combinations; in a normed space a dilation is a special affine map, but the two notions are otherwise unrelated).