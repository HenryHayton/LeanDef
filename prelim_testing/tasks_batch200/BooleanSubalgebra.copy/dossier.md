## Object

`VTask.copy` produces a new Boolean subalgebra whose carrier set is explicitly given as `s`, where `s` is required to be definitionally equal to the carrier of an existing Boolean subalgebra `L`. The result is mathematically identical to `L` — same elements, same operations, same algebraic structure — but recorded with `s` as its carrier. This is a bookkeeping device used to force definitional equalities that Lean's kernel needs for type-checking purposes.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {α : Type u_2} -> [BooleanAlgebra α] -> (L : BooleanSubalgebra α) -> (s : Set α) -> (hs : s = ↑L) -> BooleanSubalgebra α
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_2} -> [BooleanAlgebra α] -> (L : BooleanSubalgebra α) -> (s : Set α) -> (hs : s = ↑L) -> BooleanSubalgebra α`

The ambient type `α` is a Boolean algebra, providing the full algebraic structure. `L` is the original Boolean subalgebra being copied. `s` is the new carrier set to attach to the copy. `hs` is a proof that `s` equals the coercion of `L` to a set (i.e., `s` is literally the same set as the carrier of `L`).

## Conventions

The output of `VTask.copy L s hs` is considered equal to `L` as a Boolean subalgebra (they share the same carrier and all structural data), so `copy_eq` holds: the copied subalgebra is propositionally equal to the original. The carrier coercion of the result is exactly `s`, as recorded by `coe_copy`.

## Worked examples

- Claim: For any Boolean subalgebra `L` of a Boolean algebra `α`, applying `VTask.copy L ↑L rfl` yields a Boolean subalgebra whose carrier is `↑L`.

- Claim: For any Boolean subalgebra `L` of a Boolean algebra `α`, `(VTask.copy L ↑L rfl : BooleanSubalgebra α) = L` (the copy is propositionally equal to the original).

- Claim: For any Boolean subalgebra `L` and proof `hs : s = ↑L`, an element `x` belongs to `VTask.copy L s hs` if and only if `x ∈ L`.

## Boundaries

Since `hs` must be a proof that `s = ↑L`, the only admissible input is a set `s` literally equal to the carrier of `L`; there is no notion of a "different" carrier being supplied. The construction is total under these constraints: once `hs` is provided, the copy always succeeds. When `s = ↑L` and `hs = rfl`, the copy is the canonical identity copy.

## Not to be confused with

- `BooleanSubalgebra.mk` — constructs a Boolean subalgebra from scratch by supplying all closure conditions, rather than copying an existing one.
- Sublattice or Subgroup `copy` operations — analogous copying constructions for weaker algebraic structures; they do not carry the Boolean (complement and bottom) data.
- Set-level equality of carriers — two subalgebras with equal carriers are propositionally equal as subalgebras (by extensionality), but `VTask.copy` is specifically for adjusting *definitional* equality of the carrier without reproving all closure conditions.