## Object

`VTask.next c i` picks the "next" index after `i` in the complex shape `c`. Concretely, a `ComplexShape ι` carries a binary relation `Rel` on indices that encodes which pairs `(i, j)` are consecutive in a homological or cohomological complex. Given an index `i`, `VTask.next c i` returns *some* index `j` satisfying `c.Rel i j` when such a `j` exists, and returns `i` itself (a self-loop sentinel) when no such `j` exists. Because the choice among multiple eligible successors is arbitrary (but fixed), the function is well-defined and total.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.next : {ι : Type u_1} -> (c : ComplexShape ι) -> (i : ι) -> ι
<!-- PINNED-SIGNATURE:END -->


`VTask.next : {ι : Type u_1} -> (c : ComplexShape ι) -> (i : ι) -> ι`

The implicit type argument `ι` is the index type. The first explicit argument `c` is the complex shape, whose relation `Rel` determines which pairs of indices are "adjacent." The second explicit argument `i` is the index whose successor is sought.

## Conventions

When there exists at least one index `j` such that `c.Rel i j` holds, `VTask.next c i` is defined to be *some* such `j`; the particular choice is not specified beyond that it satisfies `c.Rel i j`. When no such `j` exists — i.e., `i` has no successors in the shape — `VTask.next c i` returns `i` itself as a junk value.

## Worked examples

- Claim: For the standard cohomological shape on `ℤ` (where `Rel i j ↔ j = i + 1`), `VTask.next c i = i + 1` for every `i`.

- Claim: If `c.Rel i j` holds for some `j`, then `VTask.next c i = j`.

- Claim: If no index `j` satisfies `c.Rel i j`, then `VTask.next c i = i`.

- Claim: For a complex shape on a one-element type `Unit` with the empty relation (`Rel` holds nowhere), `VTask.next c ()  = ()`.

## Boundaries

- **No successor exists**: `VTask.next c i = i`. This is the designated junk value; it does not mean `i` is related to itself.
- **Successor exists but is not unique**: `VTask.next c i` equals *one* of the valid successors, but which one is unspecified. For well-behaved (functional) complex shapes, `Rel` is a partial function, so there is at most one successor, making the result unambiguous.
- **Successor equals `i` itself (a genuine self-loop)**: If `c.Rel i i`, then `VTask.next c i` may equal `i`, but this reflects the real relation, not the junk-value fallback.
- **Addition compatibility**: When `c.Rel p (VTask.next c p)` does hold (i.e., the result is a genuine successor), `VTask.next c (p + q) = VTask.next c p + q` and `VTask.next c (p + q) = p + VTask.next c q` in additive index settings where the shape is compatible with addition.

## Not to be confused with

- `ComplexShape.prev` / `VTask.prev`: the analogous function selecting a *predecessor* `j` with `c.Rel j i`, going in the reverse direction.
- `ComplexShape.Rel i j` itself: the underlying relation that specifies which pairs are adjacent; `VTask.next` is a derived function that picks a concrete index, not just a predicate.
- The identity function on `ι`: `VTask.next c i` coincides with the identity only at indices with no successor (junk-value convention), not in general.