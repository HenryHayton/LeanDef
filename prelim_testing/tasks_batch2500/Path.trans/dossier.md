## Object

`VTask.trans` constructs the **concatenation** of two continuous paths: given a path `γ` from `x` to `y` and a path `γ'` from `y` to `z` in a topological space `X`, it produces a new path from `x` to `z`. The resulting path traverses `γ` at double speed on the first half of the unit interval `[0, 1/2]`, then traverses `γ'` at double speed on the second half `[1/2, 1]`. This is the standard "path concatenation" or "path composition" operation used in algebraic topology (e.g., to define the fundamental group).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.trans : {X : Type u_1} -> [TopologicalSpace X] -> {x y z : X} -> (γ : Path x y) -> (γ' : Path y z) -> Path x z
<!-- PINNED-SIGNATURE:END -->


VTask.trans : {X : Type u_1} -> [TopologicalSpace X] -> {x y z : X} -> (γ : Path x y) -> (γ' : Path y z) -> Path x z

The implicit type argument `X` is the topological space in which the paths live. The instance argument supplies the topology on `X`. The implicit points `x`, `y`, and `z` are the start, intermediate, and end points, respectively. The first explicit argument `γ` is a path from `x` to `y` (the "first leg"). The second explicit argument `γ'` is a path from `y` to `z` (the "second leg"). The result is a path from `x` to `z`.

## Conventions

The two paths meet at the common midpoint parameter value `1/2`: for parameter `t ≤ 1/2`, the concatenated path evaluates to `γ` reparametrised to run twice as fast, and for `t ≥ 1/2` it evaluates to `γ'` reparametrised to run twice as fast starting from `0`. At the junction point `t = 1/2`, both formulas agree (since `γ(1) = y = γ'(0)`), so no junk value convention is needed there. The operation is not strictly associative as a path (only up to reparametrisation/homotopy), and does not form a group but rather a groupoid structure on points.

## Worked examples

- Claim: The range of `VTask.trans γ₁ γ₂` equals the union of the ranges of `γ₁` and `γ₂`.

- Claim: The symmetry/reversal of `VTask.trans γ γ'` equals `VTask.trans γ'.symm γ.symm`.

- Claim: Concatenating the constant (refl) path at `a` with itself returns the constant path at `a`, i.e., `(Path.refl a).trans (Path.refl a) = Path.refl a`.

- Claim: If `f : X → Y` is continuous, then mapping `f` over `VTask.trans γ γ'` equals `VTask.trans (γ.map h) (γ'.map h)`, i.e., concatenation commutes with continuous maps.

- Claim: For `t ≤ 1/2`, evaluating the extension of `VTask.trans γ₁ γ₂` at `t` gives `γ₁.extend (2 * t)`.

## Boundaries

- At `t = 0`: the concatenated path evaluates to `γ(0) = x`, matching the required source.
- At `t = 1`: the concatenated path evaluates to `γ'(1) = z`, matching the required target.
- At `t = 1/2`: the path is continuous through the junction because `γ(1) = y = γ'(0)`; both the left-hand formula `γ.extend(1)` and the right-hand formula `γ'.extend(0)` equal `y`.
- The operation is defined for all pairs of composable paths in any topological space; there is no restriction on the space being Hausdorff or the paths being injective.
- For paths in a product space, concatenation distributes over the product: `(γ₁.prod γ₂).trans (δ₁.prod δ₂) = (γ₁.trans δ₁).prod (γ₂.trans δ₂)`.
- Concatenation of paths in a `Pi`-type distributes pointwise similarly.

## Not to be confused with

- `Path.symm`: the *reversal* of a single path (traversing it backwards), not a composition of two paths.
- `Path.refl`: the *constant* (identity) path at a point, which acts as a unit for concatenation only up to homotopy.
- `SimpleGraph.Walk.IsPath.transfer`: a graph-theoretic path concept, entirely unrelated to topological paths and their concatenation.