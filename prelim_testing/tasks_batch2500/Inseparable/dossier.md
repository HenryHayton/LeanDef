## VTask.Inseparable

### Object

Two points `x` and `y` in a topological space are **inseparable** (also called *topologically indistinguishable*) when every open set contains either both of them or neither of them. Equivalently, no open set separates them: there is no open neighbourhood of `x` that misses `y`, and no open neighbourhood of `y` that misses `x`. In terms of closures, `x` and `y` are inseparable precisely when `closure {x} = closure {y}`, i.e., the two singleton closures coincide, or equivalently each point lies in the closure of the other's singleton.

In a T₀ space the relation collapses to equality; in a non-T₀ space there can be genuinely distinct but inseparable points.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Inseparable : {X : Type u_1} -> [TopologicalSpace X] -> (x y : X) -> Prop
<!-- PINNED-SIGNATURE:END -->


The implicit argument is the ambient type `X`, which must carry a topological space structure (supplied by the type-class instance). The two explicit arguments `x` and `y` are the points whose topological indistinguishability is being asserted.

### Conventions

No special junk-value or edge conventions are declared for this definition: it is a straightforward Prop-valued predicate that is meaningful for every pair of points in every topological space, including the trivial one-point space and the empty space.

### Worked examples

- Claim: In any topological space, every point is inseparable from itself (`VTask.Inseparable x x` holds for all `x`).

- Claim: In a T₁ space, `VTask.Inseparable x y` implies `x = y`; in particular, in `ℝ` with its standard topology, two distinct real numbers are never inseparable.

- Claim: `VTask.Inseparable` is a symmetric relation: if `VTask.Inseparable x y` then `VTask.Inseparable y x`.

- Claim: `VTask.Inseparable` is a transitive relation: if `VTask.Inseparable x y` and `VTask.Inseparable y z` then `VTask.Inseparable x z`.

- Claim: On a set with the indiscrete topology, every pair of points satisfies `VTask.Inseparable x y`.

### Boundaries

- **Reflexivity**: Every point is inseparable from itself, since equality of neighbourhood filters is trivially reflexive.
- **T₀ spaces**: The relation `VTask.Inseparable` on a T₀ space is the same as equality; two points that are inseparable must be equal.
- **Discrete spaces**: In a discrete space every singleton is open, so distinct points have different neighbourhood filters and are never inseparable.
- **Indiscrete spaces**: In the indiscrete topology the only open sets are ∅ and the whole space, so every pair of points is inseparable.
- **Empty type**: The predicate is vacuously satisfied (there are no pairs to consider).

### Not to be confused with

- **`Specializes` (`x ⤳ y`)**: A one-directional version where the neighbourhood filter of `x` is finer than that of `y`; inseparability is the symmetric closure of specialisation.
- **`SeparatedNhds`**: A condition on *sets* (or pairs of points) asserting the existence of disjoint open neighbourhoods; this is stronger than mere distinguishability and is unrelated in direction to `VTask.Inseparable`.
- **`IsOpen` membership coincidence**: While inseparability is *equivalent* to membership coincidence for every open set, the individual open-set condition alone does not define the relation — the quantified equivalence is a characterisation theorem, not the definition.