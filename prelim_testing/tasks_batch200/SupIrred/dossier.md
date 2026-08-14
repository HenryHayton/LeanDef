## VTask.SupIrred

### Object

An element `a` of a semilattice (a partially ordered set equipped with binary suprema / joins) is called **sup-irreducible** if it satisfies two conditions simultaneously:

1. It is not a minimum element of the whole order (intuitively, it is not "bottom").
2. Whenever `a` is expressed as the supremum (join) of two elements `b` and `c`, at least one of those elements must already equal `a` itself — that is, `a` cannot be "split" into two strictly smaller pieces whose join is `a`.

In classical lattice theory, these are exactly the join-irreducible elements (the condition that `b ⊔ c = a` forces `b = a` or `c = a`), and the non-minimality condition rules out the bottom element.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.SupIrred : {α : Type u_2} -> [SemilatticeSup α] -> (a : α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.SupIrred : {α : Type u_2} -> [SemilatticeSup α] -> (a : α) -> Prop`

The implicit type argument `α` is the carrier type of the order. The instance argument supplies the semilattice structure (the binary supremum operation and the compatible partial order). The explicit argument `a` is the element whose sup-irreducibility is being tested.

### Conventions

In a semilattice that happens to have a bottom element `⊥`, a minimum element is never sup-irreducible; the theorem `not_supIrred_bot` records that `⊥` itself is not sup-irreducible. In a semilattice with no bottom, the non-minimality condition still rules out any globally minimal element.

### Worked examples

- Claim: In the lattice of natural numbers ordered by divisibility, the prime number 2 is sup-irreducible (its only way of being "joined" from below is trivially from itself).

- Claim: In any semilattice, if `a` is sup-irreducible then `a` cannot be a minimum element of the order.

- Claim: In the Boolean algebra on a two-element set `{0,1}`, the top element `1` is sup-irreducible because the only way to write `1 = b ⊔ c` with `b, c ≤ 1` that gives `1` requires at least one of `b` or `c` to equal `1` (since the only other element is `0`, and `0 ⊔ 0 = 0 ≠ 1`).

- Claim: In a linear order (total order) with more than one element, every non-minimum element `a` is sup-irreducible, because if `b ⊔ c = a` then `b ⊔ c = max(b, c) = a`, which forces `b = a` or `c = a`.

- Claim: Every sup-prime element is sup-irreducible (i.e., `VTask.SupIrred a` follows from `SupPrime a`).

### Boundaries

- A minimum element (including `⊥` when it exists) is **never** sup-irreducible; the predicate is definitionally `False` for such elements.
- In a one-element semilattice the single element is minimal, hence not sup-irreducible; the predicate has no witnesses.
- In a distributive lattice, `VTask.SupIrred a` is equivalent to `SupPrime a`; the two notions coincide in that setting.
- Every sup-irreducible element has a finite sup-decomposition theorem: if a finite supremum equals `a`, then one of the summands already equals `a`.
- The notion is self-dual in the following sense: `a` is sup-irreducible in `α` if and only if the corresponding element is inf-irreducible in the dual order `αᵒᵈ`.

### Not to be confused with

- **`SupPrime`**: a strictly stronger property requiring that `a ≤ b ⊔ c` implies `a ≤ b` or `a ≤ c`; sup-irreducible is weaker (only the equality case `b ⊔ c = a` is controlled).
- **`InfIrred`**: the order-dual notion — an element that is not maximum and cannot be written as a meet of two strictly larger elements; related by the duality `infIrred_toDual`.
- **`IsAtom`**: in a bounded lattice, an atom is an element covering `⊥`; atoms are sup-irreducible but the converse fails in general.
