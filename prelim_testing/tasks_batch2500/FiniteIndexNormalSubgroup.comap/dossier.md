## Object

`VTask.comap f K` is the preimage of a finite-index normal subgroup `K` of a group `H` under a group homomorphism `f : G →* H`, regarded as a finite-index normal subgroup of `G`. That is, it is the subgroup of `G` consisting of all elements `g` such that `f(g)` belongs to `K`, equipped with the data that this subgroup is normal in `G` and has finite index in `G`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comap : {G : Type u_1} -> [Group G] -> {H : Type u_2} -> [Group H] -> (f : G →* H) -> (K : FiniteIndexNormalSubgroup H) -> FiniteIndexNormalSubgroup G
<!-- PINNED-SIGNATURE:END -->


`VTask.comap : {G : Type u_1} -> [Group G] -> {H : Type u_2} -> [Group H] -> (f : G →* H) -> (K : FiniteIndexNormalSubgroup H) -> FiniteIndexNormalSubgroup G`

The implicit arguments `G` and `H` are the domain and codomain groups, respectively. The group structures on `G` and `H` are supplied as instance arguments. The first explicit argument `f` is the group homomorphism from `G` to `H` whose preimage operation is being applied. The second explicit argument `K` is the finite-index normal subgroup of `H` whose preimage is taken.

## Conventions

There are no special junk-value or edge conventions declared for this definition. The operation is total: any group homomorphism and any finite-index normal subgroup of the codomain yield a well-defined finite-index normal subgroup of the domain.

## Worked examples

- Claim: For the trivial homomorphism `f : G →* H` and any finite-index normal subgroup `K` of `H`, the underlying subgroup of `VTask.comap f K` is all of `G` (since every element maps to the identity, which lies in `K`).

- Claim: For the identity homomorphism `id : G →* G` and a finite-index normal subgroup `K` of `G`, `VTask.comap id K` has the same underlying subgroup as `K` itself.

- Claim: If `f : G →* H` is surjective and `K` is a finite-index normal subgroup of `H`, then the index of `VTask.comap f K` in `G` divides the index of `K` in `H`.

- Claim: If `K` is the trivial normal subgroup `{1}` of `H` with finite index (i.e., `H` itself is finite), then `VTask.comap f K` is the kernel of `f`, viewed as a finite-index normal subgroup of `G`.

## Boundaries

- When `f` is the trivial (constant) homomorphism, the preimage of any subgroup containing the identity is all of `G`, so `VTask.comap f K` is the whole group `G` as a subgroup, which is a finite-index (index 1) normal subgroup.
- When `f` itself is surjective, the index of `VTask.comap f K` in `G` equals the index of `K` in `H`. When `f` is not surjective, the index may be smaller.
- If `K` happens to be all of `H`, then `VTask.comap f K` is all of `G`.
- The construction is well-typed even when `G` or `H` is infinite, as long as `K` has finite index in `H` (the finite-index property of the preimage is deduced automatically).

## Not to be confused with

- `Subgroup.comap f K`: The plain comap of a `Subgroup` under a homomorphism, which does not carry finiteness-of-index or normality data as part of its type.
- `VTask.map` (a hypothetical forward-image construction): The image of a subgroup under a homomorphism goes in the opposite direction and does not generally preserve finite-index or normality without surjectivity assumptions.
- `MonoidHom.ker f`: The kernel of `f`, which is the preimage of the trivial subgroup; `VTask.comap f K` generalises this to an arbitrary finite-index normal subgroup `K`.