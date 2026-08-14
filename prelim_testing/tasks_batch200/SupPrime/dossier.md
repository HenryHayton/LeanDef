## Object

A **sup-prime** element of a semilattice is an element `a` that satisfies two conditions simultaneously:
1. `a` is not a minimal element of the lattice (informally, something strictly smaller than `a` exists, or at least `a` is not a bottom element).
2. Whenever `a` is bounded above by a binary supremum `b ⊔ c`, then `a` is already bounded above by one of the two operands individually — i.e., `a ≤ b ⊔ c` implies `a ≤ b` or `a ≤ c`.

This is the order-theoretic analogue of a prime element in a ring: a sup-prime element cannot be "covered" by a join unless it is already below one of the joinands.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.SupPrime : {α : Type u_2} -> [SemilatticeSup α] -> (a : α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.SupPrime : {α : Type u_2} -> [SemilatticeSup α] -> (a : α) -> Prop`

The implicit type parameter `α` is the carrier type of the semilattice. The instance `[SemilatticeSup α]` supplies the binary supremum operation `⊔` and the associated order structure. The explicit argument `a` is the element of `α` whose sup-primeness is being tested.

## Conventions

In a semilattice that happens to have a bottom element `⊥`, sup-primeness automatically excludes `⊥` (since `⊥` is always minimal). There is no special junk-value convention — `VTask.SupPrime` is a `Prop` and is simply `False` for any element that fails either condition.

## Worked examples

- Claim: In a linear order with more than one element, every non-minimum element is sup-prime (since in a linear order every join reduces to one of the two elements, so the primeness condition is automatic).

- Claim: The bottom element `⊥` of a bounded semilattice is never sup-prime, because `⊥` is always a minimal element.

- Claim: In the powerset lattice of a two-element set `{x, y}`, the singleton sets `{x}` and `{y}` are sup-prime: each is non-minimal (it lies above the empty set `∅`), and if `{x} ⊆ S ∪ T` then `{x} ⊆ S` or `{x} ⊆ T`.

- Claim: In the powerset lattice of `{x, y}`, the full set `{x, y}` is **not** sup-prime: `{x, y} ⊆ {x} ∪ {y}`, yet `{x, y} ⊄ {x}` and `{x, y} ⊄ {y}`.

## Boundaries

- A minimal element (including `⊥` in a bounded lattice) is never sup-prime, by the first conjunct of the definition.
- In a two-element lattice `{⊥, ⊤}`, the top element `⊤` is sup-prime: it is not minimal, and the only way `⊤ ≤ b ⊔ c` can hold (since everything is `≤ ⊤`) is if `b` or `c` already equals `⊤`.
- Every sup-prime element is also sup-irreducible (`SupIrred`); the converse holds in linear orders (and more generally whenever `supPrime_iff_supIrred` applies) but may fail in more general semilattices.
- The notion is self-dual in the following sense: `a` is sup-prime in `α` if and only if `a` (viewed in the dual order `αᵒᵈ`) is inf-prime.

## Not to be confused with

- **`SupIrred`** (sup-irreducible): a weaker condition — an element is sup-irreducible if it is non-minimal and is not the join of two strictly smaller elements, but it need not satisfy the full primeness condition `a ≤ b ⊔ c → a ≤ b ∨ a ≤ c`. Every sup-prime element is sup-irreducible, but not conversely in general.
- **`InfPrime`** (inf-prime): the order-dual concept, concerning the meet operation `⊓` instead of the join `⊔`.
- **`IsMin`** (minimal element): a property that directly contradicts sup-primeness; a minimal element is never sup-prime.