## 1. Object

`VTask.MapsTo f s t` is the proposition that the function `f` carries every element of the set `s` into the set `t`; in other words, the image of `s` under `f` is a subset of `t`. It is the standard set-theoretic notion of a function *mapping a set into another set*.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.MapsTo : {α : Type u} -> {β : Type v} -> (f : α → β) -> (s : Set α) -> (t : Set β) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.MapsTo : {α : Type u} -> {β : Type v} -> (f : α → β) -> (s : Set α) -> (t : Set β) -> Prop`

The universe levels `u` and `v` are implicit and inferred automatically. The argument `f` is the function whose behaviour on `s` is being described. The argument `s` is the source set (a subset of the domain type `α`) whose image is under scrutiny. The argument `t` is the target set (a subset of the codomain type `β`) that is required to contain the image.

## 3. Conventions

The proposition is stated universally and is vacuously true when `s` is the empty set: there are no elements to map, so `VTask.MapsTo f ∅ t` holds for any `f` and any `t`, including the empty set.

## 4. Worked examples

- Claim: `VTask.MapsTo (fun n : ℕ => n + 1) {0, 1, 2} {1, 2, 3}` — the successor function maps `{0,1,2}` into `{1,2,3}`.

- Claim: `VTask.MapsTo (fun x : ℝ => x ^ 2) (Set.Icc 0 1) (Set.Icc 0 1)` — squaring maps the unit interval `[0,1]` into itself.

- Claim: `VTask.MapsTo (id : ℕ → ℕ) ∅ ∅` — the identity function vacuously maps the empty set into the empty set.

- Claim: `VTask.MapsTo (fun _ : ℕ => (0 : ℕ)) Set.univ {0}` — the constant-zero function maps every natural number into the singleton `{0}`.

## 5. Boundaries

- **Empty source set**: `VTask.MapsTo f ∅ t` is vacuously true for every `f` and every `t` (including `t = ∅`), because there is no element in `∅` to violate the condition.
- **Empty target set**: `VTask.MapsTo f s ∅` forces `s` to be empty; it is true if and only if `s = ∅`, since any element of `s` would have to map to an element of `∅`.
- **Universal source**: `VTask.MapsTo f Set.univ t` asserts that every value of `f` lies in `t`, i.e., the range of `f` is contained in `t`.
- **Universal target**: `VTask.MapsTo f s Set.univ` is always true regardless of `f` and `s`, since every element of any type belongs to the universal set.
- **Containment direction**: the condition requires `f(s) ⊆ t`, not equality; the image may be a proper subset of `t`.

## 6. Not to be confused with

- **`Set.SurjOn f s t`**: requires that `t` is *contained in* the image of `s` under `f` — the opposite containment from `VTask.MapsTo`.
- **`Set.InjOn f s`**: a separate injectivity condition on `f` restricted to `s`; says nothing about where elements are mapped, only that distinct inputs give distinct outputs.
- **`Set.image f s ⊆ t`**: an equivalent formulation phrased as a subset relation between sets rather than a universal membership statement; these are definitionally equivalent but syntactically different.