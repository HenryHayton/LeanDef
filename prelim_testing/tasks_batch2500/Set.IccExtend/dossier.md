## Object

`VTask.IccExtend h f` is the canonical "constant-outside, honest-inside" extension of a function `f : [a, b] → β` to all of `α`. For any point `x` in `α`, the extended function evaluates `f` at the nearest endpoint if `x` lies outside the closed interval `[a, b]`, and evaluates `f` directly at `x` if `x` lies inside the interval. Concretely: if `x ≤ a` the value is `f(a)`, if `a ≤ x ≤ b` the value is `f(x)`, and if `x ≥ b` the value is `f(b)`. The construction retains the same range as `f`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IccExtend : {α : Type u_1} -> {β : Type u_2} -> [LinearOrder α] -> {a b : α} -> (h : a ≤ b) -> (f : ↑(Set.Icc a b) → β) -> α → β
<!-- PINNED-SIGNATURE:END -->


`VTask.IccExtend : {α : Type u_1} -> {β : Type u_2} -> [LinearOrder α] -> {a b : α} -> (h : a ≤ b) -> (f : ↑(Set.Icc a b) → β) -> α → β`

`α` is the linearly-ordered type serving as the domain; `β` is the codomain (no order is required on it). `a` and `b` are the left and right endpoints of the closed interval, respectively. `h` is the proof that `a ≤ b`, which is needed to ensure the interval `[a, b]` is non-empty. `f` is the function defined on the closed interval `[a, b]` that is to be extended. The final `α` argument is the point at which the extended function is evaluated.

## Conventions

For any point `x ≤ a`, the extended function returns the value `f(a)` (left-endpoint clamping). For any point `x ≥ b`, the extended function returns the value `f(b)` (right-endpoint clamping). For any `x` lying in `[a, b]`, the extended function agrees with `f` at `x`. The range of the extended function equals the range of the original function `f`.

## Worked examples

- Claim: For `f : Set.Icc (0 : ℤ) 10 → ℤ` defined by `f ⟨x, _⟩ = x * x`, `VTask.IccExtend (by norm_num : (0 : ℤ) ≤ 10) f (-3)` equals `f ⟨0, _⟩ = 0`, because `-3 ≤ 0 = a`.

- Claim: For `f : Set.Icc (0 : ℤ) 10 → ℤ` defined by `f ⟨x, _⟩ = x * x`, `VTask.IccExtend (by norm_num : (0 : ℤ) ≤ 10) f 5` equals `f ⟨5, _⟩ = 25`, because `5 ∈ [0, 10]`.

- Claim: For `f : Set.Icc (0 : ℤ) 10 → ℤ` defined by `f ⟨x, _⟩ = x * x`, `VTask.IccExtend (by norm_num : (0 : ℤ) ≤ 10) f 15` equals `f ⟨10, _⟩ = 100`, because `15 ≥ 10 = b`.

- Claim: The range of `VTask.IccExtend h f` equals the range of `f` for any `f : Set.Icc a b → β`.

## Boundaries

- At `x = a`: the extended function returns `f ⟨a, _⟩`, the value of `f` at the left endpoint.
- At `x = b`: the extended function returns `f ⟨b, _⟩`, the value of `f` at the right endpoint.
- For `x < a`: the extended function is constantly equal to `f ⟨a, _⟩`.
- For `x > b`: the extended function is constantly equal to `f ⟨b, _⟩`.
- When `a = b` (a degenerate interval of a single point, permitted since `h : a ≤ b` allows equality): the entire extended function is the constant `f ⟨a, _⟩`.
- The extended function's image never exceeds the image of `f`; in particular, `range (VTask.IccExtend h f) = range f`.

## Not to be confused with

- `Set.projIcc a b h : α → Set.Icc a b` — this is the clamping/projection map itself, not the extension; `VTask.IccExtend` is `f` composed with `projIcc`.
- `Set.Icc.extend` or similar piecewise-linear interpolation — `VTask.IccExtend` performs no interpolation; it simply clamps the input before evaluating `f`.
- `Function.restrict` — that restricts a function on `α` to a subset, while `VTask.IccExtend` goes the other direction, enlarging the domain from `[a, b]` to all of `α`.