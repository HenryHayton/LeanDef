## VTask.PartiallyWellOrderedOn

### Object

A set `s` in a type `α` is *partially well-ordered* with respect to a binary relation `r` when `r`, restricted to elements of `s`, constitutes a well-quasi-order on `s`. Concretely, this means that every infinite sequence of elements drawn from `s` must contain two indices `m < n` such that the `m`-th term is related to the `n`-th term by `r`. Equivalently (when `r` is symmetric in the appropriate sense), every antichain contained in `s` — a subset in which no two distinct elements are related by `r` in either direction — is finite. The concept generalises well-foundedness by additionally forbidding infinite antichains.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.PartiallyWellOrderedOn : {α : Type u_2} -> (s : Set α) -> (r : α → α → Prop) -> Prop
<!-- PINNED-SIGNATURE:END -->


The first argument `s` is the subset of `α` under consideration — the "arena" to which the relation is restricted. The second argument `r` is the binary relation on `α` whose well-quasi-order behaviour on `s` is being asserted.

### Conventions

No special junk-value or edge-case conventions are declared for this definition beyond what falls out of the logical content: the empty set and any finite set automatically satisfy the property regardless of `r`; a subsingleton set (at most one element) trivially satisfies it; a singleton set always satisfies it.

### Worked examples

- Claim: The empty set `∅ : Set ℕ` is partially well-ordered by any relation `r`.

- Claim: Any finite set `s : Set ℕ` satisfies `VTask.PartiallyWellOrderedOn s r` for any relation `r`, since no infinite sequence can be drawn from a finite set.

- Claim: The set `Set.univ : Set ℕ` is partially well-ordered by `(· ≤ ·)` on `ℕ`, because any infinite sequence of natural numbers contains an infinite non-decreasing subsequence, and in particular two indices `m < n` with `f m ≤ f n`.

- Claim: If `s` and `t` are both partially well-ordered by `r`, then so is their union `s ∪ t`.

- Claim: For a product of two sets, if `s` is partially well-ordered by `r` and `t` is partially well-ordered by `r'`, then `s ×ˢ t` is partially well-ordered by the component-wise relation `fun x y => r x.1 y.1 ∧ r' x.2 y.2`.

### Boundaries

- **Empty set**: `∅.PartiallyWellOrderedOn r` holds trivially for any `r`, since no infinite sequence can be formed from elements of the empty set.
- **Singleton**: A singleton `{a}` is always partially well-ordered by any `r`; the only sequence values are copies of `a`, and reflexivity (or the trivial repeated element) yields the required pair — formally the result `partiallyWellOrderedOn_singleton` asserts this.
- **Finite sets**: Every finite set is partially well-ordered by any relation `r`; finiteness alone forces the property.
- **Subsingleton**: Any set with at most one element is partially well-ordered by any `r`.
- **Antichains**: An antichain `s` (where no two distinct elements are `r`-related in either direction) is partially well-ordered by `r` if and only if `s` is finite. This is the tightest boundary case.
- **Monotone images**: Partial well-orderedness is preserved under maps that are monotone with respect to the relevant relations; images of PWO sets are PWO.
- **Subsets**: If `t` is partially well-ordered by `r` and `s ⊆ t`, then `s` is also partially well-ordered by `r` (downward closure under inclusion).

### Not to be confused with

- `Set.WellFoundedOn r`: Only requires that there is no infinite strictly descending chain; does not forbid infinite antichains, so it is strictly weaker than partial well-orderedness.
- `WellQuasiOrdered`: The global (not set-restricted) version of the same concept, applying to the entire type rather than a specified subset.
- `Set.IsPWO` (if present): A variant spelling or alias sometimes used; the underlying content is the same well-quasi-order condition but accessed through a different Mathlib API path.