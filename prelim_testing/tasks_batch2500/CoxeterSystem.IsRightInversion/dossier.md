## VTask.IsRightInversion

### Object

In a Coxeter system, a **right inversion** of a group element $w$ is a reflection $t$ such that multiplying $w$ on the right by $t$ strictly decreases the length of $w$; that is, $\ell(wt) < \ell(w)$. The proposition `IsRightInversion cs w t` asserts exactly that $t$ is a reflection (in the sense of the Coxeter system) and that $t$ is a right inversion of $w$ in this sense.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsRightInversion : {B : Type u_1} -> {W : Type u_2} -> [Group W] -> {M : CoxeterMatrix B} -> (cs : CoxeterSystem M W) -> (w t : W) -> Prop
<!-- PINNED-SIGNATURE:END -->


The implicit argument `B` is the type indexing the simple generators; `W` is the type of group elements carrying a `Group` instance; `M` is the Coxeter matrix on `B` encoding the braid relations; `cs` is the full Coxeter system structure. The first explicit argument `w` is the group element whose right inversions are being considered. The second explicit argument `t` is the candidate reflection being tested as a right inversion of `w`.

### Conventions

No special junk-value or edge-case conventions are declared for this definition: it is a straightforward conjunction of two well-defined predicates (`IsReflection` and a strict inequality on lengths), each of which handles all inputs, so no distinguished behavior on degenerate inputs needs to be specified.

### Worked Examples

- Claim: For the identity element `1` in any Coxeter system, no element `t` satisfies `IsRightInversion cs 1 t`, because `ℓ(1 · t) = ℓ(t) ≥ 0 = ℓ(1)` but in fact `ℓ(1) = 0`, so `ℓ(t) < 0` is impossible.

- Claim: If `s` is a simple generator of a Coxeter system and `t = s`, then `IsRightInversion cs s s` holds if and only if `s` is a reflection (which it is, as every simple generator is a reflection) and `ℓ(s · s) = ℓ(1) = 0 < 1 = ℓ(s)`, so `IsRightInversion cs s s` holds for every simple generator `s`.

- Claim: If `w` is any element and `t` is a reflection with `ℓ(wt) > ℓ(w)`, then `IsRightInversion cs w t` is false, even though `t` is a reflection.

- Claim: The set of right inversions of `w` has cardinality equal to `ℓ(w)`, reflecting that the number of right inversions precisely measures the word length in the Coxeter group.

### Boundaries

- For the identity element `1 : W`, the length is `0`, and since lengths are non-negative, `ℓ(1 · t) < 0` is impossible, so `IsRightInversion cs 1 t` is false for every `t`.
- If `t` is not a reflection (e.g., `t = 1` in a non-trivial Coxeter group, or `t` is a non-reflection group element), then `IsRightInversion cs w t` is false regardless of `w`.
- The condition is not symmetric in `w` and `t`: `IsRightInversion cs w t` concerns multiplication on the right, while the analogous left-hand notion would require `ℓ(tw) < ℓ(w)`.
- Since length is a non-negative integer, the inequality `ℓ(wt) < ℓ(w)` combined with the reflection condition forces `ℓ(wt) = ℓ(w) - 1` (lengths of a group element and its right-reflection-multiple differ by exactly 1).

### Not to be Confused With

- **`IsLeftInversion cs w t`**: the analogous condition where `t` is multiplied on the left of `w`, i.e., `ℓ(tw) < ℓ(w)`; not the same as right inversion in general.
- **`IsReflection cs t`**: the strictly weaker condition asserting only that `t` is a reflection, without any requirement on how it interacts with a particular element `w`.
- **`cs.IsRightDescent`**: a similar but coarser notion where `t` is restricted to be a simple generator (i.e., a Coxeter generator), rather than an arbitrary reflection.
