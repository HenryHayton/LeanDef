## VTask.IsCobounded

### Object

`VTask.IsCobounded r f` asserts that the filter `f` is *cobounded* (equivalently, *frequently bounded*) with respect to the binary relation `r`. Informally, this means that `f` does not tend to infinity in the direction of `r`: there exists some element `b` of `α` that serves as a persistent witness, in the sense that whenever every large element of `f` satisfies `r x a` for some bound `a`, that same bound `a` is also related to `b` via `r`. In the most common instantiation with `r = (≤)` on an ordered type, this says that the filter `f` is frequently bounded above — it does not escape to `+∞`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsCobounded : {α : Type u_1} -> (r : α → α → Prop) -> (f : Filter α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_1} -> (r : α → α → Prop) -> (f : Filter α) -> Prop`

The implicit argument `α` is the type whose elements the filter and relation both concern. The first explicit argument `r` is the binary relation on `α` that determines the notion of "going to infinity" (typically `(≤)` or `(≥)` on an ordered type). The second explicit argument `f` is the filter whose coboundedness is being asserted.

### Conventions

When `α` is a complete lattice, `VTask.IsCobounded r f` is designed to hold for every filter `f`, including the trivial filter (the one containing the empty set). The definition is deliberately chosen so that this good behavior at the trivial filter is automatic, which differs from the naive negation-based formulation that would fail in that edge case.

### Worked examples

- Claim: For any preorder `α` and a non-bottom filter `f`, if `f` is bounded above (i.e., `f.IsBounded (· ≤ ·)`), then `f.IsCobounded (· ≥ ·)` holds — the filter is frequently bounded below.

- Claim: For a filter `f` on a linear order and an element `l`, if `f` frequently produces values `≥ l` (i.e., `∃ᶠ x in f, l ≤ x`), then `VTask.IsCobounded (· ≤ ·) f` holds.

- Claim: `VTask.IsCobounded r f` is monotone in `f` in the sense that if `f ≤ g` (i.e., `f` is at least as fine as `g`) and `f` is cobounded for `r`, then `g` is also cobounded for `r` — coarser filters inherit coboundedness.

- Claim: For any filter on a complete lattice, `VTask.IsCobounded (· ≤ ·) f` holds, since a witness `b` can always be found when the lattice has all infima.

### Boundaries

- **Trivial filter / filter containing ∅**: The definition is crafted so that coboundedness holds for the trivial filter (the filter containing the empty set) in complete lattices. The naive equivalent `¬ ∀ a, ∀ᶠ n in f, a ≤ n` would fail at this filter, but the chosen existential form does not.
- **`⊥` filter (trivial filter)**: Every element `b` serves as a witness vacuously, so the condition is always satisfied.
- **Principal filter at a single point**: The condition reduces to checking that the single element can serve as the persistent witness `b`, which is immediate.
- **Non-bot filters**: For non-trivial (non-bot) filters, coboundedness with respect to `(≤)` is equivalent to the filter being frequently bounded above; formally this equivalence requires the filter to be `NeBot`.

### Not to be confused with

- `Filter.IsBounded r f`: asserts that `f` *is* bounded with respect to `r` (there is an eventual upper/lower bound in the filter); coboundedness is the "frequent" rather than "eventual" version.
- `Filter.IsCoboundedUnder r f u`: the pulled-back version along a function `u`, asserting coboundedness of the image filter rather than `f` itself.
- `Filter.Tendsto f g r`: asserts that the filter `f` maps into `g` along `r`; coboundedness asserts the filter does *not* escape to infinity and is a much weaker condition.