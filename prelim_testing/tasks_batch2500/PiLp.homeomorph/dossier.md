## Object

`VTask.homeomorph` is the canonical homeomorphism between the *Lp-weighted product type* `PiLp p β` and the ordinary dependent product type `(i : ι) → β i`. Both types carry the same underlying set of dependent functions, but `PiLp p β` is a type synonym whose topology is deliberately chosen to make certain Lp-norm estimates work out; `VTask.homeomorph` witnesses that this topology nevertheless coincides with the standard product topology on `(i : ι) → β i`, packaging that fact as a homeomorphism (a bicontinuous bijection).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.homeomorph : (p : ENNReal) -> {ι : Type u_2} -> (β : ι → Type u_4) -> [(i : ι) → TopologicalSpace (β i)] -> PiLp p β ≃ₜ ((i : ι) → β i)
<!-- PINNED-SIGNATURE:END -->


`VTask.homeomorph : (p : ENNReal) -> {ι : Type u_2} -> (β : ι → Type u_4) -> [(i : ι) → TopologicalSpace (β i)] -> PiLp p β ≃ₜ ((i : ι) → β i)`

The first argument `p` is the extended non-negative real exponent (an element of `ENNReal`, allowing values such as `0`, `1`, `2`, `∞`, etc.) that parameterises the Lp type synonym. The implicit argument `ι` is the index type over which the product is taken. The argument `β` is the family of types being multiplied together — a function assigning to each index `i : ι` a type `β i`. The instance argument `[(i : ι) → TopologicalSpace (β i)]` supplies a topological space structure on each factor `β i`, which is needed to speak about continuity of the homeomorphism.

## Conventions

No special junk-value or edge-case conventions have been declared for this definition: it is a total construction that produces a valid homeomorphism for every choice of `p`, `ι`, `β`, and topological space instances, including the boundary values `p = 0` and `p = ∞`.

## Worked examples

- Claim: `VTask.homeomorph 2 (fun _ : Fin 3 => ℝ)` is a homeomorphism from `PiLp 2 (fun _ : Fin 3 => ℝ)` to `(Fin 3 → ℝ)`, i.e., its `toEquiv` sends a vector to the underlying function.

- Claim: For any `p : ENNReal` and any family `β : ι → Type*` with `[∀ i, TopologicalSpace (β i)]`, applying `VTask.homeomorph p β` to an element `x : PiLp p β` and then applying its inverse gives back `x`; that is, the composition `(VTask.homeomorph p β).symm ∘ (VTask.homeomorph p β)` is the identity on `PiLp p β`.

- Claim: The underlying `Equiv` of `VTask.homeomorph p β` agrees with `WithLp.equiv p ((i : ι) → β i)`, so the forward map sends `x : PiLp p β` to the same function `(i : ι) → β i` that `WithLp.equiv` would produce.

## Boundaries

- When `ι` is the empty type, the homeomorphism still makes sense: both `PiLp p (fun i : Empty => β i)` and `(i : Empty) → β i` are singleton types with the trivial topology, and the homeomorphism is the unique map between them.
- When `p = 0` or `p = ∞`, the definition is still well-formed; `ENNReal` includes these values, and the Lp type synonym `PiLp` is defined for all `p : ENNReal`.
- When `β` is a constant family `fun _ => α`, the homeomorphism specialises to a homeomorphism between `PiLp p (fun _ : ι => α)` and the function type `ι → α`.
- No continuity conditions on `p` itself are required; `p` is purely a type-level tag.

## Not to be confused with

- `WithLp.equiv p ((i : ι) → β i)`: this is the underlying *set-theoretic* equivalence (a `≃`, i.e., a bijection without topology), of which `VTask.homeomorph` is the topological upgrade.
- `EuclideanSpace.equiv` or norm-isometry variants: those package the homeomorphism together with metric or norm-preserving data; `VTask.homeomorph` only asserts topological (not metric) equivalence.
- `PiLp.linearEquiv`: this is a *linear* equivalence between `PiLp p β` and `∏ i, β i` in the vector-space sense, not a homeomorphism in the topological sense.