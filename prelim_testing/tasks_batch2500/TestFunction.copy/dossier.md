## Object

`VTask.copy` produces a new test function that is identical to a given test function `f`, but whose underlying function is recorded as `f'` rather than the coercion of `f`. Because `f'` is required to be propositionally equal to `f`, the two test functions represent exactly the same mathematical object; the sole purpose of `copy` is to adjust the *definitional* presentation of the underlying function, which can matter when Lean's kernel must check definitional equality in downstream proofs.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {E : Type u_3} -> [NormedAddCommGroup E] -> [NormedSpace ℝ E] -> {Ω : TopologicalSpace.Opens E} -> {F : Type u_4} -> [NormedAddCommGroup F] -> [NormedSpace ℝ F] -> {n : ℕ∞} -> (f : TestFunction Ω F n) -> (f' : E → F) -> (h : f' = ⇑f) -> TestFunction Ω F n
<!-- PINNED-SIGNATURE:END -->


`VTask.copy : {E : Type u_3} -> [NormedAddCommGroup E] -> [NormedSpace ℝ E] -> {Ω : TopologicalSpace.Opens E} -> {F : Type u_4} -> [NormedAddCommGroup F] -> [NormedSpace ℝ F] -> {n : ℕ∞} -> (f : TestFunction Ω F n) -> (f' : E → F) -> (h : f' = ⇑f) -> TestFunction Ω F n`

`E` is the Euclidean-like domain space (a real normed space), and `Ω` is an open subset of `E` on which the test function lives. `F` is the target normed space. `n` is the order of differentiability (a value in `ℕ∞`, allowing `∞` for the smooth case). The argument `f` is the source test function being copied. The argument `f'` is the new raw function that will be used as the underlying map of the result. The argument `h` is a proof that `f'` is propositionally equal to the coercion of `f` as a function `E → F`; it witnesses that `f'` carries identical values and therefore that all required analytic properties are inherited.

## Conventions

There are no junk-value or edge conventions to declare: the definition is total and every input is constrained by the hypothesis `h`, so no degenerate input regime arises.

## Worked examples

- Claim: The coercion of `VTask.copy f f' h` as a function equals `f'` (given `h : f' = ⇑f`).

- Claim: `VTask.copy f f' h` is equal (as a test function) to the original `f` (given `h : f' = ⇑f`).

- Claim: If `f' = ⇑f` and `f'' = f'`, then `VTask.copy f f'' (h'.trans h)` has coercion `f''`.

## Boundaries

- The hypothesis `h` must hold propositionally (i.e., as a proof term), not merely point-wise; the definition is not available when `f'` is only extensionally equal to `⇑f` without a direct proof.
- When `f' = ⇑f` is supplied by `rfl` (i.e., `f'` is definitionally the coercion), the result is definitionally, not just propositionally, the same object.
- The differentiability order `n` may be `⊤` (representing `C^∞`); the construction works uniformly for every value in `ℕ∞`.
- The open set `Ω` need not be bounded or connected; no such restriction is imposed.

## Not to be confused with

- `TestFunction.mk` / structure constructor: builds a test function from scratch by providing all fields independently, whereas `VTask.copy` reuses every field from an existing test function and only changes how the underlying function is syntactically recorded.
- Function restriction or coercion: `VTask.copy` does not change the values of the function on any point; it is purely a bookkeeping device for the type-theoretic identity of the underlying map.
- `Set.indicator`-style modification: unlike operations that genuinely alter function values outside a domain, `VTask.copy` leaves all values unchanged.