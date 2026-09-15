## Object

`VTask.IsLeftInversion cs w t` is the proposition that `t` is a **left inversion** of `w` in the Coxeter group `W` associated with the Coxeter system `cs`. Concretely, it asserts two things simultaneously: (1) `t` is a reflection in `W` (i.e., conjugate to some simple generator), and (2) multiplying `w` on the left by `t` strictly decreases the word-length of `w` — formally, `ℓ(t·w) < ℓ(w)`, where `ℓ` denotes the standard length function of the Coxeter system.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsLeftInversion : {B : Type u_1} -> {W : Type u_2} -> [Group W] -> {M : CoxeterMatrix B} -> (cs : CoxeterSystem M W) -> (w t : W) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsLeftInversion : {B : Type u_1} -> {W : Type u_2} -> [Group W] -> {M : CoxeterMatrix B} -> (cs : CoxeterSystem M W) -> (w t : W) -> Prop`

The implicit type `B` is the index type for the simple generators (the nodes of the Coxeter diagram). The implicit type `W` is the Coxeter group itself, equipped with its group structure via the `Group W` instance. The implicit `M` is the Coxeter matrix encoding the braid and order relations. The explicit argument `cs` is the Coxeter system structure tying `W` to `M`, which in particular provides the length function `ℓ`. The argument `w` is the group element whose left inversions are being examined. The argument `t` is the candidate element being tested as a left inversion of `w`.

## Conventions

No special junk-value or boundary conventions have been declared for this definition: it is a well-typed Prop that is meaningful for every group element `w` and every element `t` in `W`; no inputs are "out of domain."

## Worked examples

- Claim: In any Coxeter system, if `s` is a simple generator (a reflection of length 1) and `w = s`, then `s` is a left inversion of `w = s` because `ℓ(s·s) = ℓ(e) = 0 < 1 = ℓ(s)` and `s` is a reflection.

- Claim: In any Coxeter system, the identity element `e` has no left inversions, because for any reflection `t`, `ℓ(t·e) = ℓ(t) ≥ 1 > 0 = ℓ(e)` is false — indeed `ℓ(t) ≥ 1` so `ℓ(t·e) ≥ 1 = ℓ(e) + 1 > ℓ(e)` is the wrong direction; `VTask.IsLeftInversion cs 1 t` is `False` for every `t`.

- Claim: If `t` is a reflection and `ℓ(t·w) = ℓ(w)`, then `VTask.IsLeftInversion cs w t` is `False` because the strict inequality `ℓ(t·w) < ℓ(w)` fails.

- Claim: For a reduced expression `w = s₁ s₂ … sₖ`, every element of the form `s₁ (s₁ s₂ … sᵢ) s₁⁻¹ … sᵢ⁻¹ s₁⁻¹` (the reflections "along the left descent chain") is a left inversion of `w`; in particular, there are exactly `ℓ(w)` left inversions counted with multiplicity.

## Boundaries

- **Identity element**: The identity `1 ∈ W` has length `0`, so `ℓ(t·1) = ℓ(t) ≥ 1` for any non-identity `t`. The condition `ℓ(t·w) < ℓ(w)` becomes `ℓ(t) < 0`, which is impossible. Hence `1` has no left inversions.
- **Elements of length 1 (simple reflections)**: Each simple generator `s` has exactly one left inversion, namely itself: `ℓ(s·s) = 0 < 1`.
- **Non-reflections**: If `t` is not a reflection, then `VTask.IsLeftInversion cs w t` is `False` regardless of `w`, since the first conjunct fails.
- **Reflections that increase length**: A reflection `t` with `ℓ(t·w) > ℓ(w)` is not a left inversion of `w`; such `t` is instead a member of the **left extension set** of `w`.

## Not to be confused with

- **`VTask.IsRightInversion cs w t`** (or its analogue): the analogous notion where `t` acts on the *right*, requiring `ℓ(w·t) < ℓ(w)`; left and right inversion sets generally differ.
- **`VTask.IsReflection cs t`**: a strictly weaker statement — being a reflection is only the *first* conjunct of `IsLeftInversion`; it says nothing about the effect of `t` on the length of a specific `w`.
- **Left descent**: a *simple generator* `s` with `ℓ(s·w) < ℓ(w)` is a left descent; left inversions generalise this to all reflections, not just simple generators.