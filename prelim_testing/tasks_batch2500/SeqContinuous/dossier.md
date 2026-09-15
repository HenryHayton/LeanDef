## Object

A function `f : X → Y` between topological spaces is *sequentially continuous* if, whenever a sequence of points in `X` converges to some limit `p`, the image sequence under `f` converges to `f(p)`. That is, `f` commutes with sequential limits: convergent sequences are mapped to convergent sequences with the expected limit.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.SeqContinuous : {X : Type u_1} -> {Y : Type u_2} -> [TopologicalSpace X] -> [TopologicalSpace Y] -> (f : X → Y) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.SeqContinuous : {X : Type u_1} -> {Y : Type u_2} -> [TopologicalSpace X] -> [TopologicalSpace Y] -> (f : X → Y) -> Prop`

The universe-polymorphic type parameters `X` and `Y` are the domain and codomain types, inferred implicitly. The two instance arguments supply the topological-space structures on `X` and `Y`, also inferred automatically. The explicit argument `f` is the function whose sequential continuity is being asserted.

## Conventions

No special junk-value or boundary conventions are declared for this predicate: it is a universally quantified `Prop` that is well-formed for every function between topological spaces, including constant functions, identity functions, and discontinuous functions.

## Worked examples

- Claim: The identity function on any topological space satisfies `VTask.SeqContinuous id`, because the limit of any convergent sequence is preserved trivially.

- Claim: Any continuous function `f : X → Y` satisfies `VTask.SeqContinuous f`, because continuity (in the filter sense) implies that the image of a net — and in particular a sequence — tending to `p` tends to `f p`.

- Claim: A constant function `fun _ => c` satisfies `VTask.SeqContinuous (fun _ => c)` for any point `c : Y`, since the image sequence is eventually the constant sequence at `c`, which converges to `c = f p` regardless of the input sequence.

- Claim: If `f : X → Y` and `g : Y → Z` both satisfy `VTask.SeqContinuous`, then so does `g ∘ f`, because applying `g`'s sequential-continuity property to the convergent image sequence produced by `f`'s sequential-continuity property yields convergence of `(g ∘ f) ∘ x` to `g (f p)`.

## Boundaries

- On a first-countable topological space (e.g., any metric space), sequential continuity is equivalent to ordinary topological continuity; on non-first-countable spaces the predicate is strictly weaker than continuity.
- The predicate is vacuously true for the empty domain type (there are no sequences to check), so every function out of an empty type satisfies it.
- The predicate places no restriction on the function at individual points; it is a global condition quantified over all convergent sequences.

## Not to be confused with

- **Topological continuity** (`Continuous f`): requires pre-images of open sets to be open (equivalently, preservation of all filter limits), which is stronger than sequential continuity on non-first-countable spaces.
- **Continuity at a point** (`ContinuousAt f p`): the filter-limit condition at a single point, not restricted to sequences or global.
- **Uniform continuity** (`UniformContinuous f`): requires a single modulus of continuity uniform over the whole space, a strictly stronger metric/uniform notion unrelated to sequential limits per se.