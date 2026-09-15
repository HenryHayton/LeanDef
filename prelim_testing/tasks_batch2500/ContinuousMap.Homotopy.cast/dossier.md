## Object

Given a homotopy `F` between continuous maps `f₀` and `f₁` from a topological space `X` to a topological space `Y`, together with proofs that `f₀` equals some continuous map `g₀` and `f₁` equals some continuous map `g₁`, `VTask.cast` produces a homotopy between `g₀` and `g₁` that is, as a continuous function on the cylinder `[0,1] × X → Y`, identical to `F`. In other words, it re-labels the endpoint maps of a homotopy using definitional or propositional equalities, without altering the underlying continuous map.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.cast : {X : Type u} -> {Y : Type v} -> [TopologicalSpace X] -> [TopologicalSpace Y] -> {f₀ f₁ g₀ g₁ : C(X, Y)} -> (F : f₀.Homotopy f₁) -> (h₀ : f₀ = g₀) -> (h₁ : f₁ = g₁) -> g₀.Homotopy g₁
<!-- PINNED-SIGNATURE:END -->


`VTask.cast : {X : Type u} -> {Y : Type v} -> [TopologicalSpace X] -> [TopologicalSpace Y] -> {f₀ f₁ g₀ g₁ : C(X, Y)} -> (F : f₀.Homotopy f₁) -> (h₀ : f₀ = g₀) -> (h₁ : f₁ = g₁) -> g₀.Homotopy g₁`

The implicit type arguments `X` and `Y` are the domain and codomain topological spaces. The instance arguments supply the topologies on those spaces. The four implicit continuous maps `f₀`, `f₁`, `g₀`, `g₁` are the source and target endpoint maps: `f₀, f₁` are the original endpoints and `g₀, g₁` are the desired new endpoints. The argument `F` is the homotopy being re-labeled — the actual cylinder map. The argument `h₀` is a proof that the original starting map equals the desired new starting map. The argument `h₁` is a proof that the original ending map equals the desired new ending map.

## Conventions

There are no junk-value or out-of-domain conventions for this definition: it is total and every output is a well-formed homotopy.

## Worked examples

- Claim: Casting a homotopy along `rfl` and `rfl` yields a homotopy between the same pair of maps, and the underlying function is unchanged.

- Claim: If `H : f.Homotopy f` is the constant homotopy (refl) for some continuous map `f`, and `h₀ : f = g`, `h₁ : f = g` are the same equality proof, then `VTask.cast H h₀ h₁` is a homotopy from `g` to `g`.

- Claim: For any homotopy `F : f₀.Homotopy f₁` and equalities `h₀ : f₀ = g₀`, `h₁ : f₁ = g₁`, the evaluation of `VTask.cast F h₀ h₁` at time `0` equals `g₀`, and at time `1` equals `g₁`.

- Claim: If `F : f₀.Homotopy f₁` and `G : f₁.Homotopy f₂`, then casting `F` with `rfl` and some equality `h : f₁ = g` and separately casting `G` with `h.symm` and `rfl` allows the two casts to be composed, since the endpoint maps now agree.

## Boundaries

- When `h₀` and `h₁` are both `rfl`, the result is definitionally equal to the original homotopy `F` (same underlying function, same boundary conditions, just with trivial re-labeling).
- The operation is not restricted: it works for all topological spaces `X`, `Y`, all continuous maps, and all propositional equalities `h₀`, `h₁`, regardless of how they are proved.
- The resulting homotopy has exactly the same underlying continuous function on the cylinder `[0,1] × X` as `F`; only the type-level endpoint annotations differ.
- If `h₀` or `h₁` is a non-trivial proof (e.g., from a chain of equalities), the cast still produces a valid homotopy because it only uses those proofs to discharge the boundary conditions.

## Not to be confused with

- `ContinuousMap.Homotopy.refl`: produces the constant homotopy for a single map, not a re-labeling of an existing homotopy's endpoints.
- `ContinuousMap.Homotopy.symm`: reverses the direction of a homotopy (swapping start and end), whereas `VTask.cast` substitutes both endpoint maps simultaneously using external equality proofs.
- `eqToHom` / `cast` in the category-theoretic or type-theoretic sense: those operate on morphisms or terms at a type level; `VTask.cast` is specifically about homotopies of continuous maps between topological spaces and preserves the cylinder function.
