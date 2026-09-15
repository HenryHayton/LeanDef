## Object

A set `s` in a type `α` satisfies `VTask.Subsingleton s` if it has **at most one element**: any two members of `s` must be equal to each other. Equivalently, `s` is either empty or a singleton.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Subsingleton : {α : Type u} -> (s : Set α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Subsingleton : {α : Type u} -> (s : Set α) -> Prop`

The implicit argument `α` is the ambient type whose elements the set contains. The explicit argument `s` is the set being tested for the subsingleton property.

## Conventions

No special junk-value or edge conventions are declared for this predicate: it is a universally quantified proposition that is vacuously true for the empty set (there are no pairs of elements to compare) and trivially true for any singleton, and false for any set containing two or more distinct elements.

## Worked examples

- Claim: The empty set `(∅ : Set ℕ)` satisfies `VTask.Subsingleton ∅`, because the universal quantifier over its members is vacuously true.

- Claim: The singleton set `({42} : Set ℕ)` satisfies `VTask.Subsingleton {42}`, since its only element is 42 and 42 = 42.

- Claim: The two-element set `({0, 1} : Set ℕ)` does **not** satisfy `VTask.Subsingleton {0, 1}`, because 0 and 1 are distinct members.

- Claim: If `s : Set α` satisfies `VTask.Subsingleton s` and `f : α → β` is injective, then `VTask.Subsingleton (f ⁻¹' s)` holds — the preimage of a subsingleton under an injective function is again a subsingleton.

## Boundaries

- **Empty set**: `VTask.Subsingleton ∅` holds vacuously — there are no elements, so the condition `∀ x ∈ ∅, ∀ y ∈ ∅, x = y` is trivially satisfied.
- **Singleton sets**: `VTask.Subsingleton {a}` holds for any element `a`, since the only member is `a` itself and `a = a`.
- **Sets with two or more distinct elements**: `VTask.Subsingleton s` fails as soon as `s` contains two elements `x ≠ y`.
- **Subsets of a subsingleton**: If `s` is a subsingleton and `t ⊆ s`, then `t` is also a subsingleton.
- **Univ in a Subsingleton type**: If `α` itself is a `Subsingleton` (i.e., the type has at most one element), then every set over `α`, including `Set.univ`, satisfies `VTask.Subsingleton`.

## Not to be confused with

- **`_root_.Subsingleton α`** (the typeclass): asserts that the entire type `α` has at most one element, whereas `VTask.Subsingleton s` is a predicate on a particular subset.
- **`Set.Finite s`**: finiteness only bounds cardinality from above by a natural number; `VTask.Subsingleton s` is the sharper statement that the cardinality is at most 1.
- **`Set.Nonempty s`**: asserts that `s` has *at least* one element, which is the complementary condition; combining `Nonempty` and `Subsingleton` gives exactly the singleton sets.