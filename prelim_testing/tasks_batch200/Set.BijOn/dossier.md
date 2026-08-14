## Object

`VTask.BijOn f s t` is the proposition that a function `f : α → β` restricts to a bijection from the set `s ⊆ α` to the set `t ⊆ β`. Concretely, this means three things hold simultaneously: every element of `s` maps into `t` (the mapping condition), distinct elements of `s` have distinct images under `f` (injectivity on `s`), and every element of `t` is the image of some element of `s` (surjectivity from `s` onto `t`). Taken together these say that `f` is a set-theoretic bijection between `s` and `t`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.BijOn : {α : Type u} -> {β : Type v} -> (f : α → β) -> (s : Set α) -> (t : Set β) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.BijOn : {α : Type u} -> {β : Type v} -> (f : α → β) -> (s : Set α) -> (t : Set β) -> Prop`

The type parameters `α` and `β` are the source and target types, inferred implicitly. The argument `f` is the function whose restriction is being tested for bijectivity. The argument `s` is the domain subset of `α` on which `f` is being examined. The argument `t` is the codomain subset of `β` that `f` is required to map `s` onto bijectively.

## Conventions

No special junk-value or boundary conventions are declared: the proposition is well-formed for any `f`, `s`, and `t`; in degenerate cases (e.g., empty sets) the three conjuncts are either vacuously true or straightforwardly false, with no special definitional patch applied.

## Worked examples

- Claim: `VTask.BijOn (fun n : ℕ => n + 1) (Set.Icc 0 2) (Set.Icc 1 3)` — the successor function bijects `{0,1,2}` onto `{1,2,3}`.

- Claim: `VTask.BijOn id s s` holds for any set `s` — the identity function always bijects a set with itself.

- Claim: If `VTask.BijOn f s t` then `s` and `t` have the same `Set.ncard` — a bijection between two sets witnesses equal cardinality.

- Claim: `VTask.BijOn (fun x : ℝ => 2 * x) (Set.Icc 0 1) (Set.Icc 0 2)` — multiplication by 2 is a bijection from `[0,1]` to `[0,2]` in ℝ.

## Boundaries

- **Empty domain and codomain**: `VTask.BijOn f ∅ ∅` holds for every `f`, since all three conditions (mapping, injectivity, surjectivity) are vacuously satisfied when the domain set is empty and the target set is also empty.
- **Empty domain, non-empty target**: `VTask.BijOn f ∅ t` fails whenever `t` is non-empty, because the surjectivity condition `f '' ∅ = t` forces `t = ∅`.
- **Non-empty domain, empty target**: `VTask.BijOn f s ∅` fails whenever `s` is non-empty, because the mapping condition forces every element of `s` to land in `∅`, which is impossible.
- **`t` must equal `f '' s` exactly**: A function that maps `s` injectively into a strict superset of `f '' s` does *not* satisfy `BijOn`, because surjectivity requires `f '' s = t`.
- **Injectivity is only on `s`**: `f` may fail to be injective globally; only its behaviour on `s` matters.

## Not to be confused with

- `Set.MapsTo f s t` — only requires that `f` maps `s` into `t`; neither injectivity nor surjectivity is demanded.
- `Function.Bijective f` — asserts global bijectivity of `f` on the entire types `α` and `β`, with no reference to subsets.
- `Set.InjOn f s` — asserts only the injectivity condition of `BijOn`, without requiring that `f` maps `s` onto `t` or even into `t`.