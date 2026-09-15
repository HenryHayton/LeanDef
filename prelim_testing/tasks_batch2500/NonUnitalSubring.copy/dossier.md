## Object

Given a non-unital subring `S` of a ring `R` and a set `s` that is propositionally equal to the underlying carrier of `S`, `VTask.copy S s hs` produces a new `NonUnitalSubring R` whose carrier is definitionally `s` (rather than `↑S`) but which is otherwise identical to `S` in every structural respect. The sole purpose is to adjust definitional equalities — when downstream constructions or proofs need the carrier to be *syntactically* `s` rather than `↑S`, this operation provides a copy that satisfies that requirement without changing any mathematical content.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {R : Type u} -> [NonUnitalNonAssocRing R] -> (S : NonUnitalSubring R) -> (s : Set R) -> (hs : s = ↑S) -> NonUnitalSubring R
<!-- PINNED-SIGNATURE:END -->


`VTask.copy : {R : Type u} -> [NonUnitalNonAssocRing R] -> (S : NonUnitalSubring R) -> (s : Set R) -> (hs : s = ↑S) -> NonUnitalSubring R`

The implicit type argument `R` is the ambient ring. The instance argument supplies the non-unital, non-associative ring structure on `R`. The first explicit argument `S` is the non-unital subring being copied. The second explicit argument `s` is the new set that will serve as the carrier of the result. The third explicit argument `hs` is the proof that `s` equals the carrier of `S` as a set, ensuring the copy is mathematically identical to the original.

## Conventions

There are no junk-value or degenerate-input conventions to declare: the function is total and every valid input yields a meaningful non-unital subring. The only noteworthy convention is that the copy equals the original as a `NonUnitalSubring` whenever `s` equals `↑S`, which is exactly what `hs` guarantees.

## Worked examples

- Claim: For any non-unital subring `S` of a ring `R`, the element `x` belongs to `VTask.copy S (↑S) rfl` if and only if it belongs to `S`.

- Claim: For any non-unital subring `S` of a ring `R`, the carrier of `VTask.copy S (↑S) rfl` equals `↑S` as a set.

- Claim: If `s` and `t` are both equal to `↑S` as sets, then `VTask.copy S s hs` and `VTask.copy S t ht` have the same carrier, namely `↑S`.

## Boundaries

- The proof `hs : s = ↑S` must go in the direction `s = ↑S` (not `↑S = s`); passing the symmetric proof would require first applying `Eq.symm`.
- When `s` is chosen to be exactly `↑S` and `hs` is `rfl`, the copy is literally the same subring up to definitional equality of the carrier.
- The copy carries over all closure properties (`add_mem`, `mul_mem`, `neg_mem`, `zero_mem`) from `S`; none are re-verified independently.
- There is no restriction on which set `s` is supplied, as long as the caller provides a proof of equality; the definition is total under that contract.

## Not to be confused with

- `NonUnitalSubring.mk` — directly constructs a non-unital subring from raw data (carrier and closure proofs), whereas `VTask.copy` derives everything from an existing subring.
- Coercion `↑S : Set R` — this is just the underlying set of `S`, not a new `NonUnitalSubring`; `VTask.copy` uses it as the target of the equality proof but produces a `NonUnitalSubring`, not a `Set`.
- `NonUnitalSubring.map` — transports a non-unital subring along a ring homomorphism to a different ambient ring, whereas `VTask.copy` stays in the same ring and merely renames the carrier set.