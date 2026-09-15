## Object

`VTask.fixedPoints M α` is the subset of `α` consisting of every element that is left unchanged by every element of the monoid `M` acting on `α`. Concretely, a point `a : α` belongs to this set if and only if `m • a = a` for every `m : M`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.fixedPoints : (M : Type u_1) -> (α : Type u_3) -> [Monoid M] -> [MulAction M α] -> Set α
<!-- PINNED-SIGNATURE:END -->


`VTask.fixedPoints : (M : Type u_1) -> (α : Type u_3) -> [Monoid M] -> [MulAction M α] -> Set α`

The first explicit argument `M` is the monoid of symmetries (or transformations) doing the acting. The second explicit argument `α` is the type being acted upon, i.e., the ambient set from which the fixed points are drawn. The `Monoid M` instance supplies the monoid structure on `M`, and the `MulAction M α` instance specifies how elements of `M` act on elements of `α`.

## Conventions

No special junk-value or boundary conventions are declared for this definition: it is a totally defined set comprehension that is well-formed for any monoid `M` and any `MulAction M α`, including trivial or degenerate cases.

## Worked examples

- Claim: For the trivial (one-element) monoid acting on any type, every element is a fixed point, so `VTask.fixedPoints Unit α = Set.univ`.

- Claim: If `M = ℤ` acts on `ℤ` by addition (`m • a = m + a`), then the only fixed point is `0`, since `m + a = a` for all `m` forces `m = 0` for all `m`, which is impossible unless `a` plays no role — in fact the fixed-point set is empty in this case.

- Claim: For a group `G` acting on itself by conjugation, the fixed-point set `VTask.fixedPoints G G` is exactly the center of `G`, because `g • a = g * a * g⁻¹ = a` for all `g` is the definition of `a` lying in the center.

- Claim: The identity element `1 : M` always satisfies `1 • a = a` by the axioms of a `MulAction`, but membership in `VTask.fixedPoints M α` requires `m • a = a` for *all* `m`, not just `m = 1`.

## Boundaries

- When `M` is the trivial monoid `Unit`, every element of `α` is trivially fixed (the single element acts as the identity), so `VTask.fixedPoints Unit α = Set.univ`.
- When `α` is empty (`α = Empty`), the fixed-point set is vacuously empty.
- When `M` acts freely on `α` (no non-identity element fixes any point), `VTask.fixedPoints M α = ∅` provided `M` is nontrivial.
- The fixed-point set is always closed under the action in the sense that every element of `M` maps it to itself; in other words, it is a union of singleton orbits.
- Because the condition is a universal quantification over all of `M`, adding more elements to `M` (or making the action less trivial) can only shrink or preserve the fixed-point set, never enlarge it.

## Not to be confused with

- **Stabilizer of a single point** (`MulAction.stabilizer M a`): this is the *submonoid/subgroup of `M`* fixing a given `a`, whereas `VTask.fixedPoints M α` is the *subset of `α`* fixed by all of `M`.
- **Fixed points of a single endomorphism** (e.g., `Function.fixedPoints f` for `f : α → α`): those are points fixed by one specific self-map, not by an entire monoid action.
- **Orbit** (`MulAction.orbit M a`): the orbit of `a` is the set of all points reachable from `a` by the action, the opposite notion — a point is in `VTask.fixedPoints M α` precisely when its orbit is the singleton `{a}`.