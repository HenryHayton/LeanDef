## Object

`VTask.Equiv` is the relation of **extensional equivalence** on pre-sets (`PSet`). Two pre-sets are extensionally equivalent when they represent the same set in the cumulative hierarchy: every element (in the sense of the indexing family) of the first is equivalent to some element of the second, and vice-versa. It is the coarsest congruence that identifies pre-sets with the same membership structure, and it is precisely the kernel of the quotient map from `PSet` to `ZFSet` (von-Neumann–Bernays–Gödel sets).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Equiv : PSet.{u_1} → PSet.{u_2} → Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Equiv : PSet.{u_1} → PSet.{u_2} → Prop`

The first argument is the left-hand pre-set; the second argument is the right-hand pre-set. Both are pre-sets possibly living at different universe levels, and the relation checks that their membership structures mutually simulate each other.

## Conventions

There are no junk-value conventions to declare: the relation is defined for every pair of pre-sets without restriction, and no special output is designated for any degenerate input.

## Worked examples

- Claim: Every pre-set is extensionally equivalent to itself (reflexivity). For any `x : PSet`, `VTask.Equiv x x` holds.

- Claim: The empty pre-set `∅ : PSet` is extensionally equivalent to itself: `VTask.Equiv ∅ ∅`.

- Claim: Extensional equivalence is symmetric: if `VTask.Equiv x y` then `VTask.Equiv y x`.

- Claim: `VTask.Equiv x y` holds if and only if `PSet.toSet x = PSet.toSet y` (i.e., the two pre-sets represent the exact same set of equivalence classes).

- Claim: If `mk x = mk y` in `ZFSet` (the quotient), then `VTask.Equiv x y`; conversely if `VTask.Equiv x y` then `mk x = mk y`.

## Boundaries

- The relation is **reflexive**, **symmetric**, and **transitive**, forming an equivalence relation on `PSet`.
- It is **not anti-symmetric** on `PSet` itself: two syntactically different pre-sets (with different index types) can be equivalent without being definitionally equal.
- The relation interacts with subset: `VTask.Equiv x y` iff `x ⊆ y` and `y ⊆ x` (mutual subset).
- Universe polymorphism: the two arguments may live at different universe levels `u_1` and `u_2`, so pre-sets from different universes can be compared.
- The empty pre-set has no elements, so both quantifiers in the definition are vacuously satisfied; hence the empty pre-set is equivalent only to pre-sets that also have no elements.

## Not to be confused with

- `PSet.Subset` (`x ⊆ y`): one-directional containment; `VTask.Equiv` requires both directions simultaneously.
- `ZFSet.eq` / propositional equality in `ZFSet`: that is equality *after* quotienting by `VTask.Equiv`, whereas `VTask.Equiv` lives on the unquotiented pre-sets.
- Definitional equality of `PSet` terms in Lean (`=` on `PSet`): two pre-sets can be `VTask.Equiv` without being propositionally equal, since index types may differ.