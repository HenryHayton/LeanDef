## Object

Given a proof that two subgroups `H` and `K` of a group `G` are equal, `VTask.subgroupCongr` produces the canonical multiplicative isomorphism (a `MulEquiv`) from `H` to `K` that acts as the identity on elements: every element of `H` is sent to itself, viewed as an element of `K`. This is the "transport" or "substitution" isomorphism arising from the equality of subgroups.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.subgroupCongr : {G : Type u_1} -> [Group G] -> {H K : Subgroup G} -> (h : H = K) -> ↥H ≃* ↥K
<!-- PINNED-SIGNATURE:END -->


`VTask.subgroupCongr : {G : Type u_1} -> [Group G] -> {H K : Subgroup G} -> (h : H = K) -> ↥H ≃* ↥K`

The ambient group `G` is inferred from context. The `Group G` instance provides the multiplicative group structure. `H` and `K` are subgroups of `G`, both inferred from context. The argument `h` is a proof of equality `H = K` of subgroups; it is the sole explicit input, and the resulting multiplicative isomorphism is entirely determined by it.

## Conventions

No junk-value or edge conventions are declared: the function is total and well-defined for any proof `h : H = K`; the isomorphism it produces is always the identity on underlying elements regardless of which proof of `H = K` is supplied.

## Worked examples

- Claim: For any group `G` and subgroup `H`, `VTask.subgroupCongr (rfl : H = H)` is a `MulEquiv` whose underlying function sends every element to itself (i.e., the coercion to `G` of the image equals the coercion of the original element).

- Claim: For any group `G`, subgroups `H K : Subgroup G` with `h : H = K`, and any element `x : ↥H`, the coercion of `VTask.subgroupCongr h x` to `G` equals the coercion of `x` to `G`.

- Claim: For any group `G`, subgroups `H K : Subgroup G` with `h : H = K`, and any element `x : ↥K`, the coercion of `(VTask.subgroupCongr h).symm x` to `G` equals the coercion of `x` to `G`.

- Claim: For any group `G` and subgroup `H`, `(VTask.subgroupCongr rfl).symm` composed with `VTask.subgroupCongr rfl` is the identity `MulEquiv` on `H`.

## Boundaries

- When `H = K = ⊥` (the trivial subgroup), the isomorphism is still defined and acts as the identity on the unique element.
- When `H = K = ⊤` (the whole group as a subgroup), the isomorphism is the identity on all elements.
- The function accepts any proof `h : H = K`, including those constructed by `rfl`, `Subgroup.ext`, or `subst`; the resulting `MulEquiv` is always the same identity map regardless of which proof term is used (proof-irrelevance applies).
- The isomorphism is its own inverse: `(VTask.subgroupCongr h).symm = VTask.subgroupCongr h.symm`.

## Not to be confused with

- `MulEquiv.refl H`: the reflexive multiplicative isomorphism from `H` to itself; this is the special case of `VTask.subgroupCongr rfl`, but `refl` does not take a proof of subgroup equality as an argument.
- `Subgroup.equivMapOfInjective` or subgroup map isomorphisms: those produce isomorphisms via group homomorphisms, not from a bare equality proof.
- `Equiv.setCongr`: a plain set-level equivalence between the underlying sets; `VTask.subgroupCongr` promotes this to a `MulEquiv` by additionally verifying compatibility with multiplication.