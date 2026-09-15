## Object

The *null subgroup* of a seminormed commutative group `M` is the subgroup consisting of all elements whose norm equals zero. Because the norm is only required to be a *semi*norm (so `‖x‖ = 0` need not imply `x = 1`), this set can be non-trivial; it captures exactly the "zero-norm" elements and forms a genuine (normal) subgroup of `M`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.nullSubgroup : (M : Type u_1) -> [SeminormedCommGroup M] -> Subgroup M
<!-- PINNED-SIGNATURE:END -->


`VTask.nullSubgroup : (M : Type u_1) -> [SeminormedCommGroup M] -> Subgroup M`

The explicit argument `M` is the underlying commutative group whose seminorm is under consideration. The instance argument supplies both the group structure and the seminorm on `M`.

## Conventions

No special junk-value or out-of-domain conventions are declared: the definition is total and well-defined for every seminormed commutative group `M`, including cases where the seminorm is actually a norm (making the null subgroup trivial) and degenerate cases where every element has norm zero (making the null subgroup the whole group).

## Worked examples

- Claim: An element `x : M` belongs to `VTask.nullSubgroup M` if and only if `‖x‖ = 0`.

- Claim: In any normed commutative group (where `‖x‖ = 0 → x = 1`), the null subgroup contains only the identity element.

- Claim: `VTask.nullSubgroup M` is a closed subset of `M` (with respect to the topology induced by the seminorm).

- Claim: If every element of `M` has norm `0` (e.g. the trivial seminorm on any group), then `VTask.nullSubgroup M` equals the whole group `M`.

## Boundaries

- When the seminorm is actually a genuine norm (`‖x‖ = 0 ↔ x = 1`), the null subgroup is the trivial subgroup `{1}`.
- When the seminorm is identically zero on all of `M`, the null subgroup is all of `M`.
- The null subgroup is always closed in the topology induced by the seminorm.
- Because `M` is commutative, every subgroup is automatically normal, so the null subgroup is always a normal subgroup; this makes it suitable as the kernel of the quotient map to the associated normed group.

## Not to be confused with

- `Subgroup.trivial M`: the trivial subgroup `{1}`, which coincides with `VTask.nullSubgroup M` only when the seminorm is a genuine norm.
- The null submodule of a seminormed module: the analogous construction for modules over a ring, not subgroups of a group.
- `Subgroup.ker f` for some homomorphism `f`: the null subgroup is a kernel (of the quotient map), but is defined purely in terms of the norm, not as the kernel of a separately-given map.