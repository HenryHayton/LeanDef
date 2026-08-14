## Object

`VTask.nextFixed f x hx` is the **least fixed point of `f` that lies above `x`**. More precisely, given a monotone self-map `f` on a complete lattice and a point `x` satisfying `x ≤ f x`, it returns the smallest element `z` of the lattice such that `f z = z` and `x ≤ z`. The result is packaged as a term of the subtype of fixed points of `f`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.nextFixed : {α : Type u} -> [CompleteLattice α] -> (f : α →o α) -> (x : α) -> (hx : x ≤ f x) -> ↑(Function.fixedPoints ⇑f)
<!-- PINNED-SIGNATURE:END -->


`VTask.nextFixed : {α : Type u} -> [CompleteLattice α] -> (f : α →o α) -> (x : α) -> (hx : x ≤ f x) -> ↑(Function.fixedPoints ⇑f)`

- `α` is the carrier type of the complete lattice on which `f` operates.
- The `CompleteLattice α` instance supplies all necessary lattice operations, including arbitrary joins and meets.
- `f` is the monotone self-map (an order homomorphism `α →o α`) whose fixed points are under consideration.
- `x` is the starting point — the lower bound from which we seek the next fixed point.
- `hx` is the proof that `x` is below or equal to its image under `f`, i.e., `x ≤ f x`, which ensures that a fixed point above `x` exists and the construction is well-defined.

The return type is an element of the subtype `Function.fixedPoints f`, i.e., an `α` together with a proof that it is a fixed point of `f`.

## Conventions

The hypothesis `hx : x ≤ f x` is required as a precondition; junk-value behavior for inputs that do not satisfy this condition is not defined, as the function is not total over all `x : α` — callers must supply the proof.

## Worked examples

- Claim: For any monotone map `f` on a complete lattice and `x` with `x ≤ f x`, the result `VTask.nextFixed f x hx` satisfies `x ≤ VTask.nextFixed f x hx` (the output lies above `x`).

- Claim: For any monotone map `f` on a complete lattice, `x` with `x ≤ f x`, and any fixed point `y` of `f` with `x ≤ y`, we have `VTask.nextFixed f x hx ≤ y` (minimality: the next fixed point is indeed the *least* one above `x`).

- Claim: The iff characterization holds: `VTask.nextFixed f x hx ≤ y ↔ x ≤ y` for any fixed point `y`, capturing both the above-`x` property and minimality in a single equivalence.

## Boundaries

- If `x` is itself a fixed point (i.e., `f x = x`, so in particular `x ≤ f x`), then `VTask.nextFixed f x hx = x` — the next fixed point at a fixed point is the fixed point itself.
- The condition `x ≤ f x` is essential: without it, no fixed point above `x` need exist in general, and the function is not defined.
- In a complete lattice, the set of fixed points above any such `x` is non-empty (by a Knaster–Tarski-style argument), so the least one always exists when `hx` is satisfied.
- If `f` is the identity map, then every point is a fixed point, and `VTask.nextFixed f x hx = x` for all `x`.

## Not to be confused with

- `OrderHom.lfp` / the least fixed point of `f` overall: `VTask.nextFixed` gives the least fixed point *above a given `x`*, whereas `lfp` gives the absolute least fixed point of `f` (which corresponds to taking `x = ⊥`).
- `OrderHom.prevFixed`: the dual construction giving the *greatest* fixed point *below* a given `x` satisfying `f x ≤ x`; direction of the inequality and the extremum are both reversed.
- Fixed points of `f` in general (`Function.fixedPoints f`): `VTask.nextFixed` selects a specific distinguished element of this set relative to `x`, not the whole set.