## VTask.subtype

### Object

Given a prime power index `p`, a group `G`, a Sylow `p`-subgroup `P` of `G`, and a subgroup `N` of `G` that contains `P`, this construction produces a Sylow `p`-subgroup of `N`. In other words, if `P` is a maximal `p`-power-order subgroup of `G` and `P` happens to sit inside the subgroup `N`, then `P` is also a maximal `p`-power-order subgroup of `N`, and this definition packages that fact as an element of `Sylow p N`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.subtype : {p : ℕ} -> {G : Type u_1} -> [Group G] -> (P : Sylow p G) -> {N : Subgroup G} -> (h : ↑P ≤ N) -> Sylow p ↥N
<!-- PINNED-SIGNATURE:END -->


`{p : ℕ}` is the prime (or prime power base) determining the Sylow theory. `{G : Type u_1}` is the ambient group. `[Group G]` is the group structure on `G`. `(P : Sylow p G)` is the chosen Sylow `p`-subgroup of the full group `G`. `{N : Subgroup G}` is the subgroup of `G` into which `P` is to be restricted. `(h : ↑P ≤ N)` is the containment hypothesis asserting that the underlying subgroup of `P` is a subset of `N`; this is what makes the restriction meaningful.

### Conventions

There are no junk-value or boundary conventions to declare: the construction is a mathematically meaningful total function on its domain, with the containment hypothesis `h` ensuring the result is always a well-formed Sylow subgroup of `N`.

### Worked examples

- Claim: For any group `G`, any prime `p`, any Sylow `p`-subgroup `P` of `G`, and `N = G` (the whole group viewed as a subgroup), `VTask.subtype P (le_refl _)` recovers a Sylow `p`-subgroup of `G` (under the identification of `G` with `↥G`).

- Claim: If `P` is a Sylow `p`-subgroup of `G` and `N` is a subgroup of `G` with `P ≤ N`, then the underlying subgroup of `VTask.subtype P h` (as a subgroup of `N`) has, when mapped back into `G` via the inclusion `N → G`, the same carrier set as `P`.

- Claim: If `G` is a finite group, `p` is a prime, `P` is a Sylow `p`-subgroup of `G`, and `N` is a subgroup of `G` containing `P`, then the order of `VTask.subtype P h` (as a subgroup of `N`) equals the order of `P` (as a subgroup of `G`).

### Boundaries

- The construction requires the explicit containment proof `h : ↑P ≤ N`; without it, restricting a Sylow subgroup to a subgroup is not well-defined (a Sylow subgroup of `G` need not be a Sylow subgroup of an arbitrary subgroup of `G`).
- When `N = G` (i.e., `N` is the top subgroup), the result is essentially `P` itself re-expressed as a Sylow subgroup of `↥G`.
- The construction does not assert anything about Sylow subgroups of `G` relative to subgroups `N` that do *not* contain `P`; the hypothesis `h` rules out that degenerate case entirely.
- The result lives in `Sylow p ↥N`, whose elements are Sylow `p`-subgroups of the subtype `↥N`, not of `G` directly; one must apply the subgroup inclusion to relate them back to `G`.

### Not to be confused with

- `Sylow.map`: transports a Sylow subgroup along a group homomorphism, whereas `VTask.subtype` restricts to a *sub*group using a containment rather than an arbitrary homomorphism.
- `Sylow.comapOfInjective`: the more general operation of pulling back a Sylow subgroup along an injective homomorphism; `VTask.subtype` is the special case where the homomorphism is the subgroup inclusion `N → G`.
- `Subgroup.sylow_mem_fixedPoints_mul_normal`: a statement about which Sylow subgroups are fixed points of conjugation, not about restricting Sylow subgroups to subgroups.