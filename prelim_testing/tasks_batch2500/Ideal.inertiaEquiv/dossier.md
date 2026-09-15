## VTask.inertiaEquiv

### Object

Given two groups `M` and `N` that both act on a ring `R` via semiring-compatible actions, and given a group isomorphism `e : M ≃* N` whose action on `R` agrees with that of `M` (in the sense that applying `e` to a group element and then acting on `R` yields the same result as the original action), `VTask.inertiaEquiv` produces a group isomorphism between the inertia subgroup of an ideal `I` in `M` and the inertia subgroup of the same ideal `I` in `N`. Informally, it says that the inertia subgroup is an invariant of the action on `I`, not of the particular group realizing that action: if two groups act the same way, their inertia subgroups are isomorphic.

Recall that the inertia subgroup `Ideal.inertia M I` consists of all elements `m ∈ M` that act trivially on `I` modulo `I`, i.e., every element of `I` is sent to an element that is congruent to itself modulo `I`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.inertiaEquiv : {M : Type u_1} -> [Group M] -> {N : Type u_4} -> [Group N] -> {R : Type u_5} -> [Ring R] -> [MulSemiringAction M R] -> [MulSemiringAction N R] -> (I : Ideal R) -> (e : M ≃* N) -> (he : ∀ (m : M) (x : R), e m • x = m • x) -> ↥(Ideal.inertia M I) ≃* ↥(Ideal.inertia N I)
<!-- PINNED-SIGNATURE:END -->


`VTask.inertiaEquiv : {M : Type u_1} -> [Group M] -> {N : Type u_4} -> [Group N] -> {R : Type u_5} -> [Ring R] -> [MulSemiringAction M R] -> [MulSemiringAction N R] -> (I : Ideal R) -> (e : M ≃* N) -> (he : ∀ (m : M) (x : R), e m • x = m • x) -> ↥(Ideal.inertia M I) ≃* ↥(Ideal.inertia N I)`

- `M` and `N` are the two groups whose inertia subgroups are being compared; they appear as implicit type arguments, each equipped with a `Group` instance.
- `R` is the ring on which both groups act, equipped with a `Ring` instance and separate `MulSemiringAction` instances for `M` and `N`.
- `I` is the ideal of `R` whose stabilizer (inertia subgroup) is under consideration.
- `e` is the group isomorphism from `M` to `N` that transports one inertia subgroup to the other.
- `he` is the compatibility hypothesis: for every element `m` of `M` and every ring element `x`, applying `e m` to `x` (via `N`'s action) yields the same result as applying `m` to `x` (via `M`'s action). This is what allows the isomorphism of groups to induce an isomorphism of inertia subgroups.

### Conventions

No junk-value or edge-case conventions are declared for this definition: it is a construction that is meaningful and well-typed whenever its explicit arguments and typeclass hypotheses are satisfied, with no degenerate outputs. The action compatibility hypothesis `he` is required explicitly by the caller and is not assumed silently.

### Worked examples

- Claim: When `e` is the identity isomorphism on `M` (so `N = M`) and `he` is trivially satisfied, `VTask.inertiaEquiv I (MulEquiv.refl M) (fun m x => rfl)` is a `MulEquiv` from `Ideal.inertia M I` to itself.

- Claim: For any element `m` in `Ideal.inertia M I` and any `x : R`, the image element under `VTask.inertiaEquiv I e he` acts on `x` in the same way as `m` does, i.e., `(VTask.inertiaEquiv I e he m) • x = m • x`. This is exactly the content of `Ideal.inertiaEquiv_apply_smul`.

- Claim: For any element `n` in `Ideal.inertia N I` and any `x : R`, the preimage element under `(VTask.inertiaEquiv I e he).symm` acts on `x` in the same way as `n` does, i.e., `(VTask.inertiaEquiv I e he).symm n • x = n • x`. This is exactly the content of `Ideal.inertiaEquiv_symm_apply_smul`.

- Claim: If `m₁ m₂ : Ideal.inertia M I`, then `VTask.inertiaEquiv I e he (m₁ * m₂) = VTask.inertiaEquiv I e he m₁ * VTask.inertiaEquiv I e he m₂`, since `VTask.inertiaEquiv` is a `MulEquiv` and therefore preserves multiplication.

### Boundaries

- If `e` is the identity isomorphism `MulEquiv.refl M` (with `M = N`) and `he` holds trivially, the resulting `MulEquiv` is the identity on `Ideal.inertia M I`.
- The compatibility condition `he` is essential: without it, there is no reason for the inertia subgroup of `M` and that of `N` to be related, even if `M ≃* N` as abstract groups.
- The construction works for any ideal `I`, including the zero ideal and the unit ideal; for the unit ideal, both inertia subgroups equal the whole group, and the isomorphism induced is simply `e` restricted to those subgroups.
- The resulting `MulEquiv` is a subtype equivalence: it sends `m ∈ Ideal.inertia M I` to `e m ∈ Ideal.inertia N I`, and the symm sends `n ∈ Ideal.inertia N I` to `e⁻¹ n`.

### Not to be confused with

- `Ideal.inertia M I` itself: this is the inertia subgroup as a subgroup of `M`, not an isomorphism between two inertia subgroups.
- `MulEquiv.subgroupMap`: a general tool for transporting a subgroup along a group isomorphism, without the ring/action structure and inertia-specific membership condition.
- The decomposition group or ramification group: related filtration subgroups in algebraic number theory that are sometimes confused with the inertia subgroup.