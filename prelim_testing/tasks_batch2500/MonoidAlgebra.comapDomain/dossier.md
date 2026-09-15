## VTask.comapDomain

### Object

Given a semiring `R`, monoids `M` and `N`, and an injective function `f : M → N`, `VTask.comapDomain f hf x` produces an element of the monoid algebra `R[M]` from an element `x` of the monoid algebra `R[N]` by pulling back coefficients along `f`. Concretely, the coefficient of `m : M` in the result is the coefficient of `f m` in `x`; any basis element of `R[N]` whose index is not in the image of `f` is simply discarded.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comapDomain : {R : Type u_3} -> {M : Type u_6} -> {N : Type u_7} -> [Semiring R] -> (f : M → N) -> (hf : Function.Injective f) -> (x : MonoidAlgebra R N) -> MonoidAlgebra R M
<!-- PINNED-SIGNATURE:END -->


The type parameters `R`, `M`, and `N` are the coefficient semiring and the source and target monoids, respectively; `[Semiring R]` is the required algebraic structure on coefficients. The argument `f` is the injective function from `M` to `N` along which the pullback is performed. The argument `hf` is a proof that `f` is injective, used to ensure coefficients are well defined (no two distinct `m` values map to the same `f m`, so no coefficient collisions can occur). The argument `x` is the element of `R[N]` whose coefficients are being pulled back.

### Conventions

For any index `m : M`, the coefficient of `m` in `VTask.comapDomain f hf x` equals the coefficient of `f m` in `x`. For any index `n : N` that does not lie in the image of `f`, the contribution of that basis element to `x` is completely lost in the pullback; there is no way to recover it from the result.

### Worked examples

- Claim: For the inclusion `f : Fin 2 → Fin 3` sending `0 ↦ 0` and `1 ↦ 1`, pulling back a monoid algebra element that has coefficient `5` at index `0`, coefficient `3` at index `1`, and coefficient `7` at index `2` yields an element with coefficient `5` at `0` and coefficient `3` at `1`; the coefficient at `2` is dropped because `2` is not in the image of `f`.

- Claim: If `x : MonoidAlgebra R N` is zero, then `VTask.comapDomain f hf x` is zero for any injective `f`.

- Claim: Pulling back along the identity function `id : M → M` with injectivity proof returns the original element unchanged.

- Claim: If `x : MonoidAlgebra ℤ ℕ` is the single-term element with coefficient `4` at index `3`, and `f : ℕ → ℕ` is the map `n ↦ n + 1` (which is injective), then the coefficient of `2` in `VTask.comapDomain f hf x` is `4` (since `f 2 = 3`), and the coefficient of `0` is `0`.

### Boundaries

- If `x` is a zero element of `R[N]`, the result is the zero element of `R[M]`, regardless of `f`.
- If the image of `f` is disjoint from the support of `x`, the result is zero.
- If `f` is a bijection (in particular a bijective map between finite types), no coefficients are dropped and the result is a faithful re-indexing.
- The injectivity hypothesis `hf` is essential: without it, two distinct elements `m₁, m₂ : M` with `f m₁ = f m₂` would both claim the same coefficient from `x`, which would be ambiguous.
- All coefficients at indices outside the image of `f` are dropped silently; the operation is not surjective onto `R[M]` in general unless `f` is also surjective.

### Not to be confused with

- `MonoidAlgebra.mapDomain`: the forward (covariant) direction, which pushes coefficients along a map `M → N` (summing when the map is not injective), rather than pulling them back.
- `Finsupp.comapDomain`: the analogous operation on bare finitely-supported functions; `VTask.comapDomain` wraps this for the `MonoidAlgebra` type.
- `MonoidAlgebra.domCongr` (or similar reindexing by a bijection): a bijection-based reindexing that is an algebra isomorphism, whereas `VTask.comapDomain` works for any injective map and may lose information.
