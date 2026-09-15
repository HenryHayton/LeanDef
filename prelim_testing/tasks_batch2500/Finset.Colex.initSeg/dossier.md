## Object

`VTask.initSeg s` is the **colexicographic initial segment** ending at `s`: the collection of all finite sets that have the same cardinality as `s` and that precede or equal `s` in the colexicographic order on finite sets. Concretely, if we linearly order all finite subsets of the ground type by the colex ordering, `VTask.initSeg s` is the downward-closed (initial) segment of that order restricted to sets of size `#s`, from the colex-minimum set of that size up through and including `s` itself.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.initSeg : {α : Type u_1} -> [LinearOrder α] -> [Fintype α] -> (s : Finset α) -> Finset (Finset α)
<!-- PINNED-SIGNATURE:END -->


The implicit type argument `α` is the ground type whose subsets are being ordered. The `LinearOrder α` instance provides the total order on elements of `α` that underlies the colexicographic comparison of sets. The `Fintype α` instance ensures `α` is finite, so that the collection of all subsets of a given size is itself finite (and the result is a genuine `Finset`). The explicit argument `s` is the **top element** of the initial segment: every set in the output has the same size as `s` and is colex-at-most `s`.

## Conventions

The output always includes `s` itself, because the colex order is reflexive (`s ≤ s`) and `#s = #s`. There are no junk-value conventions declared beyond this: the definition is total and well-behaved for any `s`.

## Worked examples

- Claim: `s ∈ VTask.initSeg s` for any `s : Finset α` — every set belongs to its own initial segment.

- Claim: For `α = Fin 4` with the natural order, `VTask.initSeg {2, 3}` contains exactly the two-element subsets of `{0,1,2,3}` that are colex-at-most `{2,3}`, namely `{0,1}`, `{0,2}`, `{1,2}`, `{0,3}`, `{1,3}`, and `{2,3}` (all two-element subsets up to and including `{2,3}` in colex order).

- Claim: `t ∈ VTask.initSeg s ↔ #s = #t ∧ toColex t ≤ toColex s` — membership is characterized by matching cardinality and being colex-at-most `s`.

- Claim: `VTask.initSeg s` is an initial segment of the colex order at level `#s` (i.e., `IsInitSeg (VTask.initSeg s) #s` holds).

## Boundaries

- If `s = ∅`, then `VTask.initSeg ∅` contains exactly `{∅}`, because `∅` is the unique set of size 0 and it is trivially colex-least.
- If `s` is the colex-maximum set of its cardinality (i.e., the set consisting of the top `#s` elements of `α`), then `VTask.initSeg s` contains *all* sets of that cardinality in `α`.
- If `s` is the colex-minimum set of its cardinality, then `VTask.initSeg s = {s}`, a singleton.
- The operation is total: it is defined for every `s` regardless of cardinality or position in the colex order.

## Not to be confused with

- `IsInitSeg 𝒜 r`: a predicate asserting that a family `𝒜` is *some* initial segment of the colex order at level `r`; `VTask.initSeg s` constructs the specific such segment ending at `s`.
- The colexicographic order `toColex` itself: that is the ordering on `Finset α` wrapped in a newtype, whereas `VTask.initSeg s` is a *set of sets* cut out by that ordering.
- The shadow `∂ (VTask.initSeg s)`: a related but distinct construction that applies the combinatorial shadow operator to an initial segment, yielding the initial segment at the next smaller level.