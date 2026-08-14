## Object

`VTask.strongInductionOn` is the **strong (complete) induction principle for multisets**. Given a multiset `s` and a motive `p` indexed by multisets, it constructs a proof (or term) of `p s` by assuming that `p t` holds for every multiset `t` that is strictly smaller than `s` (with respect to the strict submultiset/cardinality ordering `<`). It is the multiset analogue of strong induction on natural numbers: to establish `p s` it suffices to know `p t` for all proper sub-multisets (by size) `t < s`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.strongInductionOn : {α : Type u_1} -> {p : Multiset α → Sort u_3} -> (s : Multiset α) -> (ih : (s : Multiset α) → ((t : Multiset α) → t < s → p t) → p s) -> p s
<!-- PINNED-SIGNATURE:END -->


VTask.strongInductionOn : {α : Type u_1} -> {p : Multiset α → Sort u_3} -> (s : Multiset α) -> (ih : (s : Multiset α) → ((t : Multiset α) → t < s → p t) → p s) -> p s

- `α` is the element type of the multisets.
- `p` is the motive — a type-valued (or proposition-valued) predicate on multisets that one wishes to prove or construct for all multisets.
- `s` is the particular multiset for which `p s` is being established.
- `ih` is the inductive step: a function that, given any multiset `s` and a proof that `p t` holds for every `t` strictly less than `s`, produces a proof of `p s`. The inner binder `(t : Multiset α) → t < s → p t` is the strong induction hypothesis, giving access to the result for all strictly smaller multisets.

## Conventions

The ordering `<` used here is the strict order on multisets, which for finite multisets coincides with strict inequality of cardinality together with the submultiset relation; in particular the empty multiset `∅` is the `<`-minimum, and the base case (when no `t < s` exists, i.e. `s = ∅`) is handled automatically because the induction hypothesis is vacuously satisfied.

## Worked examples

- Claim: For any multiset `s : Multiset ℕ`, one can derive `s.card = s.card` by strong induction, taking `p s := s.card = s.card` and supplying `ih s _ := rfl`.

- Claim: The unfolding equation holds: `VTask.strongInductionOn s ih = ih s (fun t _ => VTask.strongInductionOn t ih)`. This is the content of `Multiset.strongInductionOn_eq`, which says that evaluating the strong induction at `s` immediately reduces to one application of `ih` whose recursive calls are further `strongInductionOn` invocations.

- Claim: Strong induction on multisets subsumes ordinary case analysis: a proof by cases (empty vs. cons) can be recovered by supplying an `ih` that only uses the hypothesis for multisets of strictly smaller cardinality, as witnessed by `Multiset.case_strongInductionOn`.

## Boundaries

- **Empty multiset**: When `s = ∅`, the strict induction hypothesis `∀ t < ∅, p t` is vacuously true (no multiset is strictly less than `∅`), so `ih ∅ (fun t h => absurd h (not_lt_bot _))` must produce `p ∅` without any recursive calls. The principle handles this correctly because the hypothesis is never invoked.
- **Termination**: The recursion is well-founded because `<` on multisets is a well-founded relation (multisets have finitely many predecessors and `<` is a strict order with no infinite descending chains).
- **Universe polymorphism**: `p` may live in any `Sort u_3`, so the principle applies equally to propositions (`Prop`) and data (`Type`).

## Not to be confused with

- `Multiset.induction_on`: the ordinary (structural) induction principle for multisets, which splits into a base case for `∅` and a step adding one element — weaker than strong induction because the step only gives `p s`, not `p t` for all `t < a ::ₘ s`.
- `Multiset.case_strongInductionOn`: a variant of strong induction specialised to propositions that uses `≤` rather than `<` in the hypothesis and splits explicitly into the empty and cons cases.
- `WellFounded.induction`: the general well-founded recursion/induction combinator; `VTask.strongInductionOn` is specifically tuned to the `<` order on multisets and presents a more convenient interface.
