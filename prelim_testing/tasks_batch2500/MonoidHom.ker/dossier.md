## VTask.ker

### Object

Given a group homomorphism `f : G →* M` from a group `G` to a monoid `M`, the **kernel** of `f` is the subgroup of `G` consisting of all elements that `f` maps to the identity element `1` of `M`. It is the complete preimage of `{1}` under `f`, and it is indeed a subgroup of `G` (closed under the group operations, including inversion).

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ker : {G : Type u_1} -> [Group G] -> {M : Type u_7} -> [MulOneClass M] -> (f : G →* M) -> Subgroup G
<!-- PINNED-SIGNATURE:END -->


`VTask.ker : {G : Type u_1} -> [Group G] -> {M : Type u_7} -> [MulOneClass M] -> (f : G →* M) -> Subgroup G`

The implicit type `G` is the source group; the instance `[Group G]` supplies the full group structure on `G`. The implicit type `M` is the target monoid; the instance `[MulOneClass M]` supplies just enough structure on `M` to have a distinguished identity element. The explicit argument `f` is the monoid homomorphism whose kernel is being taken. The result is a subgroup of `G`.

### Conventions

The target `M` need only be a `MulOneClass` (it does not need to be a group), so the kernel is defined in the broadest multiplicative setting where an identity element exists. No special junk-value conventions are needed because the definition is total over all homomorphisms.

### Worked examples

- Claim: The kernel of the identity homomorphism `MonoidHom.id G` is the trivial subgroup `⊥`.

- Claim: An element `g : G` belongs to `VTask.ker f` if and only if `f g = 1`.

- Claim: For the unique homomorphism `f : G →* PUnit` (sending every element to the single element of the trivial monoid), every element of `G` lies in `VTask.ker f`, so `VTask.ker f = ⊤`.

- Claim: `VTask.ker f = ⊥` (the trivial subgroup) if and only if `f` is injective.

### Boundaries

- If `f` is the trivial (constant-one) homomorphism, then `VTask.ker f = ⊤` — the entire group is the kernel.
- If `f` is injective, then `VTask.ker f = ⊥` — only the identity element maps to `1`.
- The definition requires `G` to be a full group (inversion must be available), so that the kernel is closed under inverses. The target `M`, however, need only carry a `MulOneClass` structure.
- The kernel is always a normal subgroup of `G` when `M` is itself a group, but the definition itself makes sense for any monoid target.

### Not to be confused with

- `MonoidHom.mker f` — the kernel viewed merely as a submonoid of `G`, without the subgroup structure (no inversion closure guaranteed at that level of abstraction).
- `AddMonoidHom.ker f` — the additive analogue, defined for `AddGroup` source and `AddZeroClass` target, where membership means `f x = 0` instead of `f x = 1`.
- `Subgroup.comap f H` — the full preimage of an arbitrary subgroup `H ≤ M` under `f`; the kernel is the special case `H = ⊥`.