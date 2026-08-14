## Object

`VTask.AntivaryOn f g s` is the proposition that the functions `f` and `g`, both indexed by the same type `ι`, *antivary* with each other on the subset `s` of indices. Concretely, this means: whenever two indices `i` and `j` both lie in `s` and `g` is strictly smaller at `i` than at `j` (i.e., `g i < g j`), then `f` is at least as large at `j` as at `i` (i.e., `f j ≤ f i`). In other words, `f` and `g` move in *opposite* directions on `s`: if `g` increases, `f` must not increase.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.AntivaryOn : {ι : Type u_1} -> {α : Type u_3} -> {β : Type u_4} -> [Preorder α] -> [Preorder β] -> (f : ι → α) -> (g : ι → β) -> (s : Set ι) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.AntivaryOn : {ι : Type u_1} -> {α : Type u_3} -> {β : Type u_4} -> [Preorder α] -> [Preorder β] -> (f : ι → α) -> (g : ι → β) -> (s : Set ι) -> Prop`

The implicit type arguments `ι`, `α`, and `β` are the index type and the two value types, respectively. The two preorder instances supply the orderings used to compare values of `f` (in `α`) and values of `g` (in `β`). The argument `f` is the first function, whose values live in the preordered type `α`. The argument `g` is the second function, whose values live in the preordered type `β`; strict comparisons of `g` drive the condition. The argument `s` is the set of indices over which the antivary condition is required to hold; only pairs of indices both belonging to `s` are considered.

## Conventions

No special junk-value or out-of-domain conventions are declared for this definition. The proposition is universally quantified, so vacuous truth applies naturally at edge cases (e.g., empty sets or trivial index types) without any special convention being needed.

## Worked examples

- Claim: `VTask.AntivaryOn (fun n : Fin 3 => (2 : ℕ) - n.val) (fun n : Fin 3 => n.val) Set.univ` holds, because `f n = 2 - n` is antitone in `n` while `g n = n` is strictly monotone, so whenever `g i < g j` we have `i < j` and thus `f j = 2 - j ≤ 2 - i = f i`.

- Claim: `VTask.AntivaryOn f g ∅` holds for any `f` and `g`, since there are no indices in the empty set and the universal quantification is vacuously true.

- Claim: If `f : ℝ → ℝ` is the negation function `f x = -x` and `g : ℝ → ℝ` is the identity `g x = x`, then `VTask.AntivaryOn f g Set.univ` holds, because `g i < g j` means `i < j`, which gives `-j ≤ -i`, i.e., `f j ≤ f i`.

- Claim: `VTask.AntivaryOn (fun _ : ℕ => (0 : ℕ)) (fun _ : ℕ => (0 : ℕ)) Set.univ` holds, since `g i < g j` is never satisfied (both are constantly 0), making the implication vacuously true.

## Boundaries

- **Empty set**: `VTask.AntivaryOn f g ∅` is always true for any `f` and `g`, by vacuous quantification.
- **Singleton set**: `VTask.AntivaryOn f g {i}` is always true, since having both indices equal to `i` forces `g i < g i`, which is false, making the premise unsatisfiable.
- **Constant functions**: If `g` is constant on `s`, the condition `g i < g j` is never met, so `VTask.AntivaryOn f g s` holds vacuously regardless of `f`.
- **Subset monotonicity**: If `VTask.AntivaryOn f g t` holds and `s ⊆ t`, then `VTask.AntivaryOn f g s` holds as well, since fewer pairs need to satisfy the condition.
- **Symmetry**: `VTask.AntivaryOn f g s` implies `VTask.AntivaryOn g f s`; the antivary relation is symmetric in its two function arguments.

## Not to be confused with

- **`Antivary f g`** (the global version): requires the antivary condition to hold for *all* indices in `ι`, not just those in a specified subset `s`.
- **`MonovaryOn f g s`**: the *co-varying* counterpart — `g i < g j` implies `f i ≤ f j`; here `f` and `g` move in the *same* direction, opposite to antivary.
- **`AntitoneOn f s`**: requires `f` itself to be antitone on `s` with respect to a single ordering on the index type, not a condition mediated by a second function `g`.