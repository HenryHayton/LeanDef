## 1. Object

A set `s` is **nontrivial** if it contains at least two *distinct* elements. Equivalently, `s` is not a subsingleton (not empty and not a singleton): there exist `x` and `y` in `s` with `x ≠ y`.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Nontrivial : {α : Type u} -> (s : Set α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Nontrivial : {α : Type u} -> (s : Set α) -> Prop`

The implicit type argument `α` is the type whose elements populate the set. The explicit argument `s` is the set being tested for nontriviality.

## 3. Conventions

There are no junk-value or boundary conventions to declare: `VTask.Nontrivial` is a Prop-valued predicate that is simply false for sets that do not contain two distinct elements (the empty set, any singleton, and any subsingleton set). No special sentinel values or out-of-domain defaults are involved.

## 4. Worked Examples

- Claim: The set `{0, 1}` of natural numbers is nontrivial (since `0 ≠ 1` and both belong to the set).

- Claim: A singleton set `{x}` is **not** nontrivial, because every two elements of it are equal.

- Claim: The empty set `∅` is **not** nontrivial, because it contains no elements at all.

- Claim: If `s` is nontrivial and `s ⊆ t`, then `t` is also nontrivial (monotonicity: a superset of a nontrivial set is nontrivial).

- Claim: If `s` is nontrivial and `f` is injective, then the image `f '' s` is nontrivial (injectivity preserves distinctness).

## 5. Boundaries

- **Empty set**: `VTask.Nontrivial ∅` is false — there are no elements to witness the existential.
- **Singleton `{x}`**: `VTask.Nontrivial {x}` is false — any two elements of the singleton are equal.
- **Two-element set `{x, y}` with `x ≠ y`**: nontrivial, this is the minimal nontrivial case.
- **Infinite sets**: every infinite set is nontrivial.
- **The condition is symmetric in the two witnesses**: the existential requires only the *existence* of some pair `x, y ∈ s` with `x ≠ y`; it does not require every pair to be distinct.

## 6. Not to be confused with

- **`Set.Nonempty s`**: asserts only that `s` has *at least one* element; nontriviality is strictly stronger.
- **`Nontrivial α` (the typeclass)**: asserts that the *entire type* `α` has at least two distinct elements; `VTask.Nontrivial` is the set-level analogue, applied to a specific subset.
- **`¬ Set.Subsingleton s`**: logically equivalent to `VTask.Nontrivial s` for nonempty sets, but `Set.Subsingleton` allows the empty set (empty sets are subsingletons), so the negation differs on `∅`.
