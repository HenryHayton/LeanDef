## 1. Object

Two permutations `f` and `g` of a type `α` are *disjoint* when their supports are disjoint: every element of `α` is either a fixed point of `f` or a fixed point of `g` (or both). In other words, no element is moved by both permutations simultaneously.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Disjoint : {α : Type u_1} -> (f g : Equiv.Perm α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Disjoint : {α : Type u_1} -> (f g : Equiv.Perm α) -> Prop`

The implicit argument `α` is the type on which the permutations act. The first explicit argument `f` and the second explicit argument `g` are the two permutations whose disjointness is being asserted.

## 3. Conventions

The relation is symmetric: `VTask.Disjoint f g` and `VTask.Disjoint g f` are logically equivalent, and neither argument is treated as primary. There are no junk-value conventions because the predicate is total: it is a well-formed proposition for every pair of permutations, including the identity.

## 4. Worked Examples

- Claim: The identity permutation is disjoint from every permutation `g`, because the identity fixes every element.

- Claim: If `f` is the transposition swapping two distinct elements `a` and `b`, and `g` is a permutation that fixes both `a` and `b`, then `VTask.Disjoint f g` holds, since every element outside `{a, b}` is fixed by `f`, and `a`, `b` are fixed by `g`.

- Claim: If `f` and `g` are both non-trivial transpositions swapping the same pair of elements, then `VTask.Disjoint f g` fails, because those elements are moved by both permutations.

- Claim: For any permutation `f`, `VTask.Disjoint f 1` holds (where `1` denotes the identity), because the identity fixes every point.

## 5. Boundaries

- When `α` is empty there are no elements to quantify over, so `VTask.Disjoint f g` holds vacuously for all `f` and `g`.
- When both `f` and `g` are the identity, the condition holds trivially since every element is fixed by both.
- The condition does not require the supports to be *nonempty*; two permutations both equal to the identity are considered disjoint.
- Disjointness of permutations implies commutativity (`f * g = g * f`), but commutativity alone does not imply disjointness.
- Disjointness is closed under inversion on either side and under multiplication: if `f` is disjoint from `h` and `g` is disjoint from `h`, then `f * g` is disjoint from `h`.

## 6. Not to be confused with

- `_root_.Disjoint` (the lattice-theoretic disjointness predicate): that is a general order-theoretic notion (greatest lower bound is bottom); `VTask.Disjoint` is specific to permutations and defined pointwise.
- `Equiv.Perm.support`: the support of a single permutation (the set of non-fixed points); `VTask.Disjoint` concerns the *intersection* of two supports being empty, not the support itself.
- Commutativity of permutations (`Commute f g`): disjoint permutations always commute, but commuting permutations need not be disjoint.