## Object

`VTask.mk` constructs an element of the closed unit disc in the complex plane, `Complex.UnitClosedDisc` (also written `𝕔𝔻`), from a complex number `z` together with a proof that `z` lies within or on the unit circle, i.e., that its complex modulus satisfies `‖z‖ ≤ 1`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mk : (z : ℂ) -> (hz : ‖z‖ ≤ 1) -> Complex.UnitClosedDisc
<!-- PINNED-SIGNATURE:END -->


`VTask.mk : (z : ℂ) -> (hz : ‖z‖ ≤ 1) -> Complex.UnitClosedDisc`

The first argument `z` is the complex number to be packaged. The second argument `hz` is a proof that the norm (modulus) of `z` is at most 1, i.e., that `z` lies inside or on the boundary of the closed unit disc.

## Conventions

No junk-value or edge conventions are declared: the constructor is total and well-defined for every complex number whose modulus is at most 1, including the boundary circle `‖z‖ = 1` and the origin `z = 0`.

## Worked examples

- Claim: `VTask.mk 0 (by simp)` is an element of `Complex.UnitClosedDisc` whose underlying complex number is `0`.
  ```lean
  example : (VTask.mk 0 (by simp)).val = 0 := rfl
  ```

- Claim: The complex number `1` (with norm exactly 1) can be placed in `𝕔𝔻` via `VTask.mk 1 (by simp)`.
  ```lean
  example : (VTask.mk 1 (by norm_num)).val = 1 := rfl
  ```

- Claim: Any `z : ℂ` with `‖z‖ ≤ 1` satisfies `‖(VTask.mk z hz).val‖ ≤ 1`.

## Boundaries

- The boundary circle `‖z‖ = 1` is fully included: elements with `‖z‖ = 1` (such as `1`, `−1`, `i`, `−i`) are valid inputs.
- The origin `z = 0` (with `‖z‖ = 0 ≤ 1`) is a valid input.
- There is no open-disc-only restriction; both strict interior points and boundary points are accepted.
- The constructor is simply a packaging operation: the underlying complex number is exactly `z`, unchanged.

## Not to be confused with

- `Complex.UnitClosedDisc` (the type itself, also written `𝕔𝔻`): that is the subtype declaration, not this particular constructor convenience.
- The open unit disc constructor (if any), which would require the strict inequality `‖z‖ < 1` and excludes the boundary.
- `Metric.ball (0 : ℂ) 1`: the open metric ball of radius 1, which excludes the unit circle and is a different set from the closed disc.