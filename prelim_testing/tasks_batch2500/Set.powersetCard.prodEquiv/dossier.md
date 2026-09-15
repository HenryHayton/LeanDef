## Object

`VTask.prodEquiv` is a canonical bijection (an equivalence of types) between the dependent-pair type whose first component is a natural number `n` and whose second component is a finite subset of `α` of cardinality exactly `n`, on the one hand, and the type `Finset α` of all finite subsets of `α`, on the other hand. Concretely, every finite set knows its own cardinality, so the cardinality datum is redundant; this equivalence makes that redundancy explicit by showing the two types are in natural one-to-one correspondence.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prodEquiv : {α : Type u_1} -> (n : ℕ) × ↑(Set.powersetCard α n) ≃ Finset α
<!-- PINNED-SIGNATURE:END -->


`VTask.prodEquiv : {α : Type u_1} -> (n : ℕ) × ↑(Set.powersetCard α n) ≃ Finset α`

The implicit type argument `α` is the ambient type whose finite subsets are being considered. The equivalence itself takes no further explicit arguments; it is a global canonical equivalence depending only on `α`.

## Conventions

There are no junk-value conventions for this definition: the equivalence is total and every value in either type is mapped to a genuine counterpart — no degenerate or edge input produces a meaningless default.

## Worked examples

- Claim: Applying `VTask.prodEquiv` to the pair `⟨2, ⟨{0, 1}, rfl⟩⟩` (a pair of cardinality `2` together with the two-element finset `{0, 1}`) yields the finset `{0, 1}` itself.

- Claim: The inverse `VTask.prodEquiv.symm` applied to the finset `{3, 7}` (of cardinality 2) yields the pair `⟨2, ⟨{3, 7}, rfl⟩⟩`, i.e., cardinality 2 paired with the set `{3, 7}` viewed as an element of `Set.powersetCard α 2`.

- Claim: The forward map forgets the cardinality witness: for any pair `x : (n : ℕ) × ↑(Set.powersetCard α n)`, `VTask.prodEquiv x` equals `x.2` (the underlying finset).

- Claim: The inverse map recovers the cardinality: for any `s : Finset α`, `(VTask.prodEquiv.symm s).1 = s.card`.

## Boundaries

- The empty finset `∅` is handled correctly: `VTask.prodEquiv.symm ∅ = ⟨0, ⟨∅, rfl⟩⟩`, pairing cardinality `0` with the unique member of `Set.powersetCard α 0`.
- For a singleton `{a}`, the inverse yields cardinality `1` and the set `{a}` as an element of `Set.powersetCard α 1`.
- The definition places no restriction on `α`; it works for any type, including infinite types, since `Finset α` only ever contains finitely many elements per set.
- Both the forward map and the inverse are computable; the equivalence is not merely a propositional existence result.

## Not to be confused with

- `Finset.card` — this is just the function extracting the cardinality of a single finset, not an equivalence between type families.
- `Set.powersetCard α n` — this is the *set* of all finsets of cardinality `n` for a *fixed* `n`, not the sigma type ranging over all `n` simultaneously.
- `Fintype.equivFin` — a different equivalence relating a `Fintype` to a standard finite type `Fin n`, not about the cardinality stratification of `Finset α`.