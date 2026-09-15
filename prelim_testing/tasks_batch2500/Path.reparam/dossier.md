## VTask.reparam

### Object

Given a continuous path `γ` from `x` to `y` in a topological space, and a continuous function `f` from the unit interval to itself satisfying `f(0) = 0` and `f(1) = 1`, the reparametrization `γ.reparam f` is the path obtained by precomposing `γ` with `f`. That is, it traverses the same image as `γ` but potentially at a different speed or rhythm determined by `f`. The result is again a path from `x` to `y`, since the endpoint conditions `f(0)=0` and `f(1)=1` ensure the new path starts at `x` and ends at `y`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.reparam : {X : Type u_1} -> [TopologicalSpace X] -> {x y : X} -> (γ : Path x y) -> (f : ↑unitInterval → ↑unitInterval) -> (hfcont : Continuous f) -> (hf₀ : f 0 = 0) -> (hf₁ : f 1 = 1) -> Path x y
<!-- PINNED-SIGNATURE:END -->


The implicit argument `X` is the ambient topological space, with its topology supplied by the typeclass instance. The arguments `x` and `y` are the shared start and end points of all paths involved. The argument `γ` is the path being reparametrized. The argument `f` is the reparametrizing map from the unit interval to itself. The argument `hfcont` is a proof that `f` is continuous. The argument `hf₀` is a proof that `f` sends `0` to `0` (ensuring the new path starts at `x`). The argument `hf₁` is a proof that `f` sends `1` to `1` (ensuring the new path ends at `y`).

### Conventions

There are no junk-value or boundary-convention issues: the definition is total and every valid input produces a well-typed path. No special sentinel or default behavior is needed.

### Worked examples

- Claim: Reparametrizing any path `γ` by the identity function returns a path with the same underlying function as `γ`.

- Claim: Reparametrizing the constant path at `x` by any admissible `f` returns the constant path at `x` (i.e., `(Path.refl x).reparam f hfcont hf₀ hf₁ = Path.refl x`).

- Claim: The image (range) of `γ.reparam f hfcont hf₀ hf₁` equals the image of `γ` as a set in `X`, because `f` is surjective onto the part of `I` that `γ` uses (both endpoints are hit and `f` is continuous), so the range is preserved.

- Claim: Evaluating `γ.reparam f hfcont hf₀ hf₁` at a point `t : I` gives `γ(f(t))`, i.e., the underlying function is exactly `γ ∘ f`.

### Boundaries

- At `t = 0`: the reparametrized path evaluates to `γ(f(0)) = γ(0) = x`, matching the source of the original path.
- At `t = 1`: the reparametrized path evaluates to `γ(f(1)) = γ(1) = y`, matching the target of the original path.
- When `f` is the identity, the reparametrized path is definitionally equal to `γ` (as a path, including its source and target proofs).
- The definition does not require `f` to be injective or surjective beyond the two endpoint conditions; a constant-speed or backtracking `f` is permitted, potentially producing a path that retraces portions of `γ`.

### Not to be confused with

- `Path.trans`: concatenates two paths end-to-end rather than reparametrizing a single path.
- `Path.map`: post-composes a path with a continuous map between spaces, changing the ambient space, rather than pre-composing with a time reparametrization.
- Homotopy of paths: a homotopy rel endpoints deforms a path through a family of paths, whereas reparametrization changes only the speed of traversal along a fixed image.