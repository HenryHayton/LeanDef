## 1. Object

A set `s` in a topological space is **sequentially closed** if it is closed under sequential limits: whenever a sequence of points, all lying in `s`, converges to some point `p` in the ambient space, that limit point `p` also belongs to `s`. This is the sequential analogue of topological closedness, replacing the general net/filter closure condition with the more concrete notion of convergent sequences.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsSeqClosed : {X : Type u_1} -> [TopologicalSpace X] -> (s : Set X) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsSeqClosed : {X : Type u_1} -> [TopologicalSpace X] -> (s : Set X) -> Prop`

The implicit type argument `X` is the ambient topological space. The instance argument provides the topology on `X`. The explicit argument `s` is the set being tested for sequential closure.

## 3. Conventions

No junk-value conventions are declared for this predicate: it is a universally quantified `Prop` over all sequences in `s` and all convergent limits, so there are no out-of-domain inputs or degenerate edge treatments to specify beyond standard vacuous truth.

## 4. Worked examples

- Claim: Every closed set in a topological space is sequentially closed. That is, if `s` is closed (in the topological sense), then `VTask.IsSeqClosed s` holds.

- Claim: In a sequential space, `VTask.IsSeqClosed s` if and only if `s` is topologically closed (`IsClosed s`).

- Claim: The preimage of a sequentially closed set under a sequentially continuous map is sequentially closed. That is, if `VTask.IsSeqClosed s` and `f` is sequentially continuous, then `VTask.IsSeqClosed (f ⁻¹' s)`.

- Claim: `VTask.IsSeqClosed s` holds if and only if the sequential closure of `s` equals `s` itself (`seqClosure s = s`).

## 5. Boundaries

- The **empty set** is sequentially closed vacuously: there are no sequences with all terms in `∅`, so the universal quantifier is trivially satisfied.
- The **whole space** `Set.univ` is sequentially closed: any limit of a sequence of elements of the full space remains in the full space.
- Sequential closure of a set is **not** in general sequentially closed itself (the sequential closure operation may need to be iterated transfinitely to reach a sequentially closed set), though once it stabilises to a fixed point the condition is met.
- In general topological spaces, **sequential closedness does not imply topological closedness** and vice versa; the two notions coincide precisely in sequential spaces.

## 6. Not to be confused with

- **`IsClosed`**: topological closedness (defined via complements and open sets, or equivalently via closure of all limit points in the sense of nets/filters); strictly stronger than sequential closedness in non-sequential spaces.
- **`seqClosure`**: the *sequential closure operator* that adds to a set all sequential limit points; `VTask.IsSeqClosed s` is the fixed-point condition for this operator, not the operator itself.
- **`IsSeqCompact`**: a different sequential property asserting that every sequence in the set has a convergent subsequence whose limit lies in the set; concerns compactness, not closedness.