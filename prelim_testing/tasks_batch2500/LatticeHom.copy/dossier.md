## Object

`VTask.copy` constructs a new lattice homomorphism from an existing one by substituting a (definitionally different but propositionally equal) underlying function. The resulting lattice homomorphism is propositionally equal to the original but carries `f'` as its `toFun`, which can be useful when Lean's definitional equality checker needs to see a specific syntactic form for the underlying function.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {α : Type u_2} -> {β : Type u_3} -> [Lattice α] -> [Lattice β] -> (f : LatticeHom α β) -> (f' : α → β) -> (h : f' = ⇑f) -> LatticeHom α β
<!-- PINNED-SIGNATURE:END -->


The first two implicit arguments are the source and target types `α` and `β`, both required to carry `Lattice` instances (supplied by the next two implicit arguments). The argument `f` is the original lattice homomorphism being copied. The argument `f'` is the new underlying function that will be installed as `toFun` in the result. The argument `h` is a proof that `f'` equals the coercion of `f` to a plain function, establishing that the two functions agree pointwise (in fact everywhere).

## Conventions

There are no special junk-value or edge-case conventions for this definition: it is a total constructor whose inputs are fully constrained by the proof `h`.

## Worked examples

- Claim: For any lattice homomorphism `f : LatticeHom α β`, calling `VTask.copy f (⇑f) rfl` gives back something whose coercion is `⇑f`.

- Claim: For any lattice homomorphism `f : LatticeHom α β`, `VTask.copy f (⇑f) rfl = f` (the copy with the same function is propositionally equal to the original).

- Claim: If `f' = ⇑f` then `⇑(VTask.copy f f' h) = f'` (the coercion of the copy is exactly `f'`, not `⇑f`).

## Boundaries

- The proof `h` must be a proof of `f' = ⇑f` (i.e., the new function equals the coercion of the original); without this the construction is ill-typed.
- The resulting homomorphism is always propositionally equal to `f`, regardless of which syntactically distinct `f'` is chosen, so `VTask.copy` never produces a "different" lattice homomorphism — only a definitionally more convenient packaging.
- Because `h` forces `f'` and `⇑f` to be propositionally equal, both the sup-preservation and inf-preservation properties of the copy follow directly from those of `f`.

## Not to be confused with

- `SupHom.copy` / `InfHom.copy`: analogous copy constructors for the individual sup-only or inf-only reduct homomorphisms; `VTask.copy` packages both together into a full lattice homomorphism.
- `LatticeHom.mk`: the primary constructor for a `LatticeHom`, which requires explicit proofs of sup- and inf-preservation rather than deriving them by equality from an existing hom.
- Function extensionality / `funext`: a way to prove two functions equal; conceptually dual to `copy`, which instead wraps a proof of equality into a new hom rather than producing a proof.