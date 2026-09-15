## VTask.univBall

### Object

`VTask.univBall c r` is a smooth open partial homeomorphism from a real normed vector space `E` into an affine torsor `P` modelled on `E`. Its source is all of `E` (i.e., `Set.univ`), and it maps `0 ∈ E` to the centre point `c ∈ P`. When the radius `r` is strictly positive, its target is exactly the open metric ball `Metric.ball c r`, and the map is a smooth diffeomorphism stretching the whole space onto that ball. When `r ≤ 0`, the map degenerates gracefully to the isometric translation by `c` (which sends every vector `v` to `c +ᵥ v`); in this degenerate case the target may extend beyond any ball of radius `r`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.univBall : {E : Type u_1} -> [SeminormedAddCommGroup E] -> [NormedSpace ℝ E] -> {P : Type u_2} -> [PseudoMetricSpace P] -> [NormedAddTorsor E P] -> (c : P) -> (r : ℝ) -> OpenPartialHomeomorph E P
<!-- PINNED-SIGNATURE:END -->


`(c : P) -> (r : ℝ) -> OpenPartialHomeomorph E P`

The first argument `c` is the centre point of the target ball in the torsor `P`. The second argument `r` is the intended radius of the target ball; when positive it determines how the space is compressed, and when non-positive it is ignored and the map falls back to a pure translation.

### Conventions

When `r > 0`, the target of the resulting open partial homeomorphism is precisely `Metric.ball c r`, and the map is a smooth homeomorphism from all of `E` onto that open ball. When `r ≤ 0`, the map is defined as the isometric translation by `c` (the torsor action), and no ball-compression occurs; in this regime the docstring notes the map is "the translation by `c`". In all cases, regardless of the sign of `r`, the map satisfies `VTask.univBall c r 0 = c`.

### Worked examples

- Claim: For any `c` and any `r > 0`, the source of `VTask.univBall c r` is `Set.univ`.

- Claim: For any `c` and any `r > 0`, the target of `VTask.univBall c r` is `Metric.ball c r`.

- Claim: For any `c` and any `r`, the value of `VTask.univBall c r` at `0` equals `c` (the centre is always hit by the origin).

- Claim: The map `VTask.univBall c r` is continuous as a function on all of `E` for every choice of `c` and `r`.

- Claim: The inverse map `(VTask.univBall c r).symm` sends `c` back to `0`, i.e., `(VTask.univBall c r).symm c = 0`.

- Claim: For any `r > 0`, `Metric.ball c r ⊆ (VTask.univBall c r).target`.

### Boundaries

- **`r > 0`**: The standard case. The map is a smooth diffeomorphism from `E` onto the open ball of radius `r` centred at `c`. The source is `Set.univ`, the target is `Metric.ball c r`, and both the forward map and its inverse are infinitely differentiable (smooth).
- **`r = 0`**: The radius is zero, so `Metric.ball c 0` is empty. The map falls back to the isometric translation by `c`; its target is not the empty set but is instead all of `P`. The forward map and its inverse remain continuous.
- **`r < 0`**: Same fallback behaviour as `r = 0`: the map is the isometric translation by `c`. The source is still `Set.univ`.
- **`r` very large**: No issue; the map still smoothly covers `Metric.ball c r` and is well-defined.
- **`c` at any torsor point**: There is no restriction on `c`; the construction works in any `NormedAddTorsor`.

### Not to be confused with

- `Metric.ball c r`: This is merely the open ball as a *set* in `P`; `VTask.univBall c r` is a structured homeomorphism whose *target* equals that set (when `r > 0`).
- The unit-ball homeomorphism (`univUnitBall`): That is the special case mapping `E` onto the unit ball `Metric.ball 0 1`; `VTask.univBall` generalises it to arbitrary centre and radius.
- `IsometryEquiv.vaddConst c`: This is the pure translation isometry by `c`, which is exactly what `VTask.univBall c r` reduces to in the degenerate case `r ≤ 0`, but it is not an `OpenPartialHomeomorph` and carries no ball-targeting structure.