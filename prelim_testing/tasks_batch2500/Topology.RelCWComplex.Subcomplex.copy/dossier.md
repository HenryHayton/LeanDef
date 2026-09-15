## Object

`VTask.copy` produces a new `Subcomplex` of a relative CW-complex that is definitionally equal to the original but carries a (possibly syntactically different) set and index family that have been supplied explicitly. Its purpose is purely bookkeeping: when the Lean elaborator needs a subcomplex whose carrier or index family is *definitionally* a particular expression rather than a propositionally equal one, `copy` lets you swap in that expression while keeping the mathematical content identical.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {X : Type u_1} -> [t : TopologicalSpace X] -> {C D : Set X} -> [Topology.RelCWComplex C D] -> (E : Topology.RelCWComplex.Subcomplex C) -> (F : Set X) -> (hF : F = ↑E) -> (J : (n : ℕ) → Set (Topology.RelCWComplex.cell C n)) -> (hJ : J = E.I) -> Topology.RelCWComplex.Subcomplex C
<!-- PINNED-SIGNATURE:END -->


The ambient type `X` is the topological space in which everything lives, equipped with a topology instance. `C` and `D` are subsets of `X`, and the instance `RelCWComplex C D` endows the pair with a relative CW-complex structure. `E` is the source subcomplex being copied. `F` is the set that should become the carrier of the new subcomplex, and `hF` is a proof that `F` equals the carrier of `E` (coerced to a set). `J` is the index family — for each dimension `n`, a set of cells — intended for the new subcomplex, and `hJ` is a proof that `J` equals the index family `E.I` of the original subcomplex.

## Conventions

There are no junk-value or boundary conventions to declare: every argument is a genuine mathematical requirement (a subcomplex, two equal replacements, and their equality proofs), and the function is total over all such inputs.

## Worked examples

- Claim: For any subcomplex `E`, calling `VTask.copy` with `F := ↑E` and `J := E.I` (with the trivial equality proofs `rfl`) yields a subcomplex that equals `E`.

- Claim: For any subcomplex `E` and any `F`, `hF`, `J`, `hJ`, the carrier of `VTask.copy E F hF J hJ` (coerced to a set) equals `F`.

## Boundaries

- If `hF : F = ↑E` is `rfl` and `hJ : J = E.I` is `rfl`, then `VTask.copy E F hF J hJ` is definitionally identical to `E`; the result is not merely propositionally but also definitionally equal to the original.
- The function never alters the mathematical content of the subcomplex: it is provably equal to `E` regardless of what syntactic forms `F` and `J` take, as long as the supplied proofs are valid.
- Because both equalities are required as explicit proof arguments, there is no silent coercion: calling `copy` with `F` not literally equal to the carrier would require a non-trivial proof of `hF`, still yielding a subcomplex with carrier `F`.

## Not to be confused with

- `Topology.RelCWComplex.Subcomplex` — this is the type that `VTask.copy` produces a new value of; `copy` is not a constructor of the CW-complex itself but of a *subcomplex*.
- `Topology.RelCWComplex.Subcomplex.mk` — the raw structure constructor, which does not require pre-existing subcomplex data and does not carry an explicit equality proof tying it back to another subcomplex.
- Subcomplex union or intersection operations — those combine two subcomplexes into a new one; `copy` only re-packages an existing one with syntactically prescribed fields.