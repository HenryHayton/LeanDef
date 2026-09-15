## Object

`VTask.comp f g` is the composition of two continuous affine maps, yielding a new continuous affine map. Given a continuous affine map `g : P →ᴬ[R] Q` and a continuous affine map `f : Q →ᴬ[R] Q₂`, their composition sends each point `p` in the affine space `P` to `f(g(p))` in the affine space `Q₂`. The result is both affine (it preserves the affine structure) and continuous (it preserves the topological structure), since both properties are stable under composition.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {R : Type u_1} -> {V : Type u_2} -> {W : Type u_3} -> {P : Type u_4} -> {Q : Type u_5} -> [Ring R] -> [AddCommGroup V] -> [Module R V] -> [TopologicalSpace P] -> [AddTorsor V P] -> [AddCommGroup W] -> [Module R W] -> [TopologicalSpace Q] -> [AddTorsor W Q] -> {W₂ : Type u_6} -> {Q₂ : Type u_7} -> [AddCommGroup W₂] -> [Module R W₂] -> [TopologicalSpace Q₂] -> [AddTorsor W₂ Q₂] -> (f : Q →ᴬ[R] Q₂) -> (g : P →ᴬ[R] Q) -> P →ᴬ[R] Q₂
<!-- PINNED-SIGNATURE:END -->


`VTask.comp : {R : Type u_1} -> {V : Type u_2} -> {W : Type u_3} -> {P : Type u_4} -> {Q : Type u_5} -> [Ring R] -> [AddCommGroup V] -> [Module R V] -> [TopologicalSpace P] -> [AddTorsor V P] -> [AddCommGroup W] -> [Module R W] -> [TopologicalSpace Q] -> [AddTorsor W Q] -> {W₂ : Type u_6} -> {Q₂ : Type u_7} -> [AddCommGroup W₂] -> [Module R W₂] -> [TopologicalSpace Q₂] -> [AddTorsor W₂ Q₂] -> (f : Q →ᴬ[R] Q₂) -> (g : P →ᴬ[R] Q) -> P →ᴬ[R] Q₂`

The implicit type arguments `R`, `V`, `W`, `W₂` are the scalar ring and the direction vector spaces underlying the respective affine spaces. The implicit type arguments `P`, `Q`, `Q₂` are the source, intermediate, and target affine spaces. The instance arguments provide the ring structure on `R`, the module and group structures on the direction spaces, the topological spaces on the point spaces, and the torsor structures linking each point space to its direction space. The explicit argument `f` is the outer (second-applied) continuous affine map, going from the intermediate affine space `Q` to the target affine space `Q₂`. The explicit argument `g` is the inner (first-applied) continuous affine map, going from the source affine space `P` to the intermediate affine space `Q`.

## Conventions

There are no special junk-value or edge-case conventions for this definition: it is a total construction with no degenerate inputs, and the composition is mathematically standard in all cases.

## Worked examples

- Claim: For continuous affine maps `f : Q →ᴬ[R] Q₂` and `g : P →ᴬ[R] Q`, the composition `VTask.comp f g` applied to a point `p : P` equals `f (g p)` as elements of `Q₂`.

- Claim: For any continuous affine map `f : P →ᴬ[R] Q`, composing with the identity continuous affine map on `P` on the right yields a map that agrees with `f` pointwise; that is, `VTask.comp f (ContinuousAffineMap.id R P)` sends each `p` to `f p`.

- Claim: Composition of continuous affine maps is associative: for `f : Q₂ →ᴬ[R] Q₃`, `g : Q →ᴬ[R] Q₂`, `h : P →ᴬ[R] Q`, the maps `VTask.comp (VTask.comp f g) h` and `VTask.comp f (VTask.comp g h)` agree pointwise.

## Boundaries

- The definition is total: it is defined for any two continuous affine maps whose domain/codomain types are compatible (i.e., the codomain of `g` matches the domain of `f`).
- If either `f` or `g` is a constant map, the composition is also a constant map (to the constant value of `f`).
- If both maps are linear (their affine parts pass through the origin), the composition is also linear, and the result coincides with the continuous linear map composition regarded as an affine map.
- There is no restriction on the ring `R` (other than being a ring) or on the topological structure (other than the minimal instances required).

## Not to be confused with

- `ContinuousLinearMap.comp`: composition of continuous *linear* maps, which requires the spaces to be modules rather than affine spaces (no translation component).
- `AffineMap.comp`: composition of affine maps *without* any continuity requirement; `VTask.comp` is the continuous-affine version and additionally carries a proof of continuity.
- `Function.comp`: plain function composition with no algebraic or topological structure, which does not produce a bundled continuous affine map.