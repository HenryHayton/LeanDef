## Object

`VTask.gnpowRec` computes the *n*-th power of a homogeneous element in a graded monoid by naive recursion on the natural number `n`. Given an element of grade `i`, it returns an element of grade `n • i` (the *n*-fold sum of `i` in the index monoid). Concretely, the zeroth power returns the graded unit (of grade `0`), and the `(n+1)`-th power multiplies the *n*-th power of the element by the element itself, with the grade bookkeeping handled by the smul arithmetic in `ι`. This is the graded analogue of the plain `npowRec` for monoids.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.gnpowRec : {ι : Type u_1} -> {A : ι → Type u_2} -> [AddMonoid ι] -> [GradedMonoid.GMul A] -> [GradedMonoid.GOne A] -> (n : ℕ) -> {i : ι} -> A i → A (n • i)
<!-- PINNED-SIGNATURE:END -->


`VTask.gnpowRec : {ι : Type u_1} -> {A : ι → Type u_2} -> [AddMonoid ι] -> [GradedMonoid.GMul A] -> [GradedMonoid.GOne A] -> (n : ℕ) -> {i : ι} -> A i → A (n • i)`

The index type `ι` is the grading monoid (e.g., `ℕ` or a free abelian group). The family `A` assigns a type to each grade; its elements are the homogeneous pieces of the graded structure. The `AddMonoid ι` instance provides the grade arithmetic, `GMul A` provides graded multiplication, and `GOne A` provides the graded unit. The explicit argument `n : ℕ` is the exponent. The implicit argument `i : ι` is the grade of the base element. The final argument is the base element itself, of grade `i`, and the result has grade `n • i`.

## Conventions

At `n = 0`, the output is the graded unit element (grade `0`), regardless of the input element; the input element is ignored entirely in this branch. At `n = k + 1`, the output is the graded product of `VTask.gnpowRec k a` (of grade `k • i`) and `a` (of grade `i`), placed in grade `(k+1) • i` via the smul identity `(k+1) • i = k • i + i`.

## Worked examples

- Claim: For the zeroth power, `VTask.gnpowRec 0 a` lands in grade `0 • i = 0` and equals the graded unit at the level of `GradedMonoid`.

- Claim: For `n = 1`, `VTask.gnpowRec 1 a` has grade `1 • i = i` and equals (in `GradedMonoid`) the product of the graded unit with `a`, which is the same as `a` up to the monoid laws.

- Claim: `GradedMonoid.mk _ (VTask.gnpowRec 0 a.snd) = 1` holds for any `a : GradedMonoid A` (this is `gnpowRec_zero`).

- Claim: `GradedMonoid.mk _ (VTask.gnpowRec n.succ a.snd) = ⟨_, VTask.gnpowRec n a.snd⟩ * a` holds for any `n` and `a : GradedMonoid A` (this is `gnpowRec_succ`).

## Boundaries

- At `n = 0`: the input element of grade `i` is completely ignored; the result is the graded one element, cast to grade `0 • i` (which equals `0` by `zero_nsmul`). This mirrors `npowRec 0 _ = 1` in an ordinary monoid.
- At `n = 1`: the result lives in grade `1 • i = i` and is (up to graded monoid axioms) equal to the original element `a`.
- There is no restriction on the grading monoid `ι` beyond it being an `AddMonoid`, so `ι` need not be cancellative, ordered, or torsion-free.
- This function is a *reference implementation* for correctness reasoning; for actual use in algebraic structures, `GMonoid.gnpow` (which may be overridden with an efficient implementation) should be preferred.
- The function is total: it is defined for all `n : ℕ` and all `a : A i`.

## Not to be confused with

- `GradedMonoid.GMonoid.gnpow`: the field of a `GMonoid` instance providing an optimised or overridden version of graded powering; `VTask.gnpowRec` is its default/fallback definition.
- `npowRec`: the analogous naive power recursion for *ordinary* (ungraded) monoids, which does not track grades.
- `GradedMonoid.GMul.mul`: a single graded multiplication step; `VTask.gnpowRec` iterates this `n` times, whereas `GMul.mul` performs exactly one multiplication.