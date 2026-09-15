## Object

Given a finpartition `P` of an element `a` in a modular lattice and, for each part of `P`, a finpartition of that part, `VTask.bind P Q` produces the single finpartition of `a` obtained by replacing each part of `P` with all the pieces of its own sub-partition — in other words, the "flat" or "juxtaposed" refinement that collects every sub-part from every sub-partition into one combined partition of `a`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.bind : {α : Type u_1} -> [Lattice α] -> [OrderBot α] -> [IsModularLattice α] -> [DecidableEq α] -> {a : α} -> (P : Finpartition a) -> (Q : (i : α) → i ∈ P.parts → Finpartition i) -> Finpartition a
<!-- PINNED-SIGNATURE:END -->


`VTask.bind : {α : Type u_1} -> [Lattice α] -> [OrderBot α] -> [IsModularLattice α] -> [DecidableEq α] -> {a : α} -> (P : Finpartition a) -> (Q : (i : α) → i ∈ P.parts → Finpartition i) -> Finpartition a`

The implicit type variable `α` is the carrier type of the lattice. The lattice, order-bot, modularity, and decidable-equality instances supply the algebraic and computational infrastructure needed to combine partitions. The implicit element `a` is the element of `α` being partitioned throughout. `P` is the coarse finpartition of `a` whose parts are to be refined. `Q` is a family of finpartitions, one for each part `i` of `P` (witnessed by the proof that `i ∈ P.parts`), providing the finer partition of that individual part.

## Conventions

There are no declared junk-value or boundary conventions for this construction: every input is constrained to be a genuine finpartition and a genuine family of sub-partitions, so the output is always a well-formed finpartition of `a`; no sentinel or degenerate output value is used.

## Worked examples

- Claim: A part `b` belongs to `(P.bind Q).parts` if and only if there exists some part `A` of `P` and a proof `hA` that `A ∈ P.parts` such that `b` belongs to `(Q A hA).parts`.

- Claim: The number of parts of `P.bind Q` equals the sum, over all parts `A` of `P`, of the number of parts of `Q A _`. Concretely, if `P` has two parts `X` and `Y`, and `Q X _` has 3 parts while `Q Y _` has 4 parts, then `(P.bind Q).parts` has 7 elements.

- Claim: If every part of `P` is given the trivial (singleton) sub-partition consisting of just that part itself, then `P.bind (fun i _ => singletonFinpartition i)` produces a partition with the same parts as `P`.

- Claim: Binding a finpartition `P` with sub-partitions is associative in the sense that binding first a coarse then a medium partition, versus directly binding the coarse partition with the finest partition, yields the same set of parts.

## Boundaries

- If `P` is the discrete partition of `a` into many atoms and each `Q i _` is the trivial one-part partition of `i`, then `VTask.bind P Q` has the same parts as `P`.
- If `P` is the indiscrete one-part partition `{a}` and `Q a _` is some partition `R` of `a`, then `VTask.bind P Q` yields a partition with exactly the parts of `R`.
- The construction is total: it requires no non-emptiness hypothesis beyond what is already encoded in the `Finpartition` type, so there is no junk output case.

## Not to be confused with

- `Finpartition.sup` / `Finpartition.inf` — operations that coarsen or refine two partitions by taking joins or meets of parts, rather than substituting sub-partitions into parts.
- `Finpartition.extend` or `Finpartition.ofErase` — constructors that build partitions by adding or removing a single element, not by recursively replacing each part with a sub-partition.
- The monad `bind` for `Option`/`List`/`Set` — while the name and spirit are analogous ("flatten a nested structure"), this is specific to the `Finpartition` type in a modular lattice and has a distinct signature and algebraic meaning.