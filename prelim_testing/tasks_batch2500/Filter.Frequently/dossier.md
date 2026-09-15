## VTask.Frequently

### Object

`VTask.Frequently p f` (written `∃ᶠ x in f, p x`) asserts that the predicate `p` holds **frequently** along the filter `f`: the set of elements where `p` fails is **not** a member of `f`. Intuitively, `p` cannot be eventually false along `f` — no matter how "far out" in `f` you look, you can always find elements where `p` is true. This is the logical dual of "eventually": while `∀ᶠ x in f, p x` says `p` holds for all sufficiently representative elements, `∃ᶠ x in f, p x` says `p` recurs without cease.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Frequently : {α : Type u_1} -> (p : α → Prop) -> (f : Filter α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Frequently : {α : Type u_1} -> (p : α → Prop) -> (f : Filter α) -> Prop`

The implicit argument `α` is the type on which everything lives. The first explicit argument `p` is the predicate whose frequent truth along the filter is being asserted. The second explicit argument `f` is the filter encoding the notion of "largeness" or "proximity" — it determines what it means to look far out or close in.

### Conventions

There are no junk-value conventions declared for this definition: `VTask.Frequently` is a `Prop`-valued predicate defined for all predicates `p` and all filters `f` on any type, with no edge cases requiring special treatment.

### Worked examples

- Claim: For the `atTop` filter on `ℕ`, the predicate `fun n => Even n` holds frequently, since no cofinite set excludes all even numbers.

- Claim: If `p` holds everywhere (`∀ x, p x`) and `f` is a `NeBot` filter, then `∃ᶠ x in f, p x`.

- Claim: `VTask.Frequently (fun _ => True) Filter.atTop` holds on `ℕ`, since `{x | ¬True} = ∅` is never in any filter whose base sets are nonempty.

- Claim: If `∃ᶠ x in f, p x` and `f ≤ g`, then `∃ᶠ x in g, p x` — frequency is preserved when passing to a coarser filter.

- Claim: `¬ ∃ᶠ x in (⊥ : Filter ℕ), fun _ => True` does **not** hold — in fact `∃ᶠ x in ⊥, p x` is false for every `p`, since `⊥` contains every set including the empty set, so `{x | ¬p x} ∈ ⊥` always.

### Boundaries

- **Bottom filter (`⊥`)**: The bottom filter contains every set (including `∅` and its complement). Hence `{x | ¬p x} ∈ ⊥` for every predicate `p`, so `VTask.Frequently p ⊥` is **always false**.
- **Top filter (`⊤`, the cofinite or principal `univ` filter)**: The top filter `⊤` on a type consists only of `univ`. The complement `{x | ¬p x}` belongs to `⊤` only if it equals `univ`, i.e., `p` is nowhere true. So `VTask.Frequently p ⊤` is true precisely when `p` holds somewhere.
- **Principal filter `𝓟 s`**: `∃ᶠ x in 𝓟 s, p x` holds iff `p` is true for at least one element of `s`, i.e., `s ∩ {x | p x}` is nonempty.
- **`atTop` on a preorder**: `∃ᶠ x in atTop, p x` means that for every bound `a`, there exists some `b ≥ a` with `p b` — exactly "arbitrarily large witnesses exist".
- **Neighbourhood filter**: `∃ᶠ x in 𝓝 x₀, p x` means `x₀` is a limit point of `{x | p x}`; if additionally `{x | p x}` is closed, then `x₀ ∈ {x | p x}`.
- **Monotonicity**: `VTask.Frequently` is antitone in the filter argument: if `∃ᶠ x in f, p x` and `f ≤ g` (i.e., `g` is coarser), then `∃ᶠ x in g, p x`. It is also monotone in the predicate: if `p` implies `q` pointwise, frequency of `p` implies frequency of `q`.

### Not to be confused with

- **`Filter.Eventually` (`∀ᶠ x in f, p x`)**: The dual notion — `p` holds for *all* filter-large sets — rather than just recurrently. `Frequently p f` is equivalent to `¬ Eventually (¬p) f`.
- **`∃ x, p x`** (bare existence): `VTask.Frequently p f` implies `∃ x, p x` but is strictly stronger — it asserts recurrence within the filter, not merely a single witness anywhere.
- **`Filter.Tendsto`**: A statement about the *convergence* of a function along filters, not about the recurrence of a predicate.