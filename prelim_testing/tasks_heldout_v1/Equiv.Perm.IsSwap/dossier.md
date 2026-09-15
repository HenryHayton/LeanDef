## Object

`VTask.IsSwap f` is the proposition that the permutation `f` is a *transposition* (also called a 2-cycle or swap): there exist two distinct elements `x` and `y` of the underlying type such that `f` exchanges `x` and `y` and fixes every other element. In classical group-theoretic language, `f` is a transposition of a two-element subset.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsSwap : {α : Type u_1} -> [DecidableEq α] -> (f : Equiv.Perm α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsSwap : {α : Type u_1} -> [DecidableEq α] -> (f : Equiv.Perm α) -> Prop`

The implicit type argument `α` is the set being permuted. The `DecidableEq α` instance provides decidable equality on `α`, which is needed to form individual transpositions. The explicit argument `f` is the permutation being tested.

## Conventions

The predicate requires the two exchanged elements to be *strictly distinct*: a swap of `x` with itself is the identity and is not considered a transposition. There are no junk-value conventions because the predicate is `Prop`-valued and is simply `False` on inputs that do not satisfy the existential.

## Worked examples

- Claim: For distinct `a b : α`, `(Equiv.swap a b).IsSwap` holds if and only if `a ≠ b`.

- Claim: Every swap has order 2, i.e., if `h : VTask.IsSwap f` then `orderOf f = 2`.

- Claim: Every swap is an odd permutation: if `h : VTask.IsSwap f` then `Equiv.Perm.sign f = -1`.

- Claim: Every swap is a cycle: if `h : VTask.IsSwap f` then `f.IsCycle`.

- Claim: A permutation is a swap if and only if its support has exactly 2 elements, i.e., `VTask.IsSwap f ↔ f.support.card = 2`.

- Claim: The set of all swaps generates the full symmetric group: `Subgroup.closure { σ | VTask.IsSwap σ } = ⊤`.

## Boundaries

- The identity permutation is **not** a swap, because any representation `swap x y` with `f = id` forces `x = y`, violating the distinctness requirement.
- The predicate is meaningful for any type `α` with `DecidableEq`, including infinite types; it does not require `α` to be finite.
- On a type with fewer than 2 elements (e.g., `Unit` or `Empty`), no two distinct elements exist, so `VTask.IsSwap` is vacuously false for every permutation.
- The two elements `x, y` witnessing the swap are not required to be unique (they can be listed in either order), but the permutation itself is uniquely determined by the unordered pair `{x, y}`.

## Not to be confused with

- `Equiv.Perm.IsCycle`: a strictly weaker notion — every swap is a cycle, but a cycle need not be a swap (it may move more than 2 elements).
- `Equiv.swap x y`: the *construction* of a specific transposition, whereas `VTask.IsSwap f` is the *property* that an already-given permutation equals some such construction.
- `Equiv.Perm.IsThreeCycle`: the analogous predicate for 3-cycles, which asserts the support has exactly 3 elements rather than 2.