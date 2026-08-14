## Object

`VTask.TFAE l` is the proposition asserting that every proposition in the list `l` is logically equivalent to every other proposition in `l`. Informally, it says "all of the propositions on this list are equivalent to one another" — the standard mathematical idiom abbreviated TFAE, standing for *The Following Are Equivalent*.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.TFAE : (l : List Prop) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.TFAE : (l : List Prop) -> Prop`

The single argument is a list of propositions. `VTask.TFAE` then states that for any two members of that list, each implies and is implied by the other.

## Conventions

When the list `l` is empty, `VTask.TFAE l` is vacuously true, since there are no propositions to compare. Similarly, when `l` contains exactly one proposition, `VTask.TFAE l` is also vacuously true, since the only pair to consider is that proposition with itself, and every proposition is equivalent to itself.

## Worked examples

- Claim: `VTask.TFAE [P, Q, R]` is equivalent to asserting that `P ↔ Q`, `Q ↔ R`, and `P ↔ R` all hold simultaneously.

- Claim: `VTask.TFAE []` holds (the empty list case is vacuously true).

- Claim: For any proposition `P`, `VTask.TFAE [P]` holds (a single proposition is trivially equivalent to itself).

- Claim: `VTask.TFAE [True, True]` holds.

- Claim: `VTask.TFAE [False, False]` holds.

## Boundaries

- **Empty list**: `VTask.TFAE []` is vacuously true because the universal quantifier over an empty list has no instances to check.
- **Singleton list**: `VTask.TFAE [P]` is vacuously true for any proposition `P` because the only eligible pair `(x, y)` is `(P, P)` and `P ↔ P` always holds.
- **Duplicate entries**: `VTask.TFAE [P, P]` holds if and only if `P ↔ P`, which is always true, so duplicating a proposition does not change satisfiability.
- **Mixed truth values**: `VTask.TFAE [True, False]` does not hold, since `True` and `False` are not equivalent.
- **Symmetry**: The relation is symmetric in the list entries — if `VTask.TFAE l` holds, reordering `l` preserves the property.

## Not to be confused with

- **`Iff` (biconditional `↔`)**: `P ↔ Q` states equivalence between exactly two propositions; `VTask.TFAE` generalises this to an arbitrary-length list.
- **`List.Pairwise (· ↔ ·) l`**: This asserts that *consecutive or ordered* pairs in `l` satisfy `↔`, which is logically equivalent to `VTask.TFAE l` but is a different syntactic predicate.
- **`∀ P ∈ l, P`**: This asserts that every proposition in the list is *true*, not that they are all equivalent to each other.