## VTask.HasUnifEigenvector

### Object

Let `M` be a module over a commutative ring `R`, and let `f` be an `R`-linear endomorphism of `M`. Given a scalar `μ : R` and an extended natural number `k : ℕ∞`, the predicate `HasUnifEigenvector f μ k x` asserts that `x` is a **nonzero generalized eigenvector** of `f` at eigenvalue `μ` of uniform order `k`. Concretely, `x` must belong to the `k`-th generalized eigenspace of `f` at `μ` (the subspace of vectors annihilated by `(f − μ·id)^k` in the appropriate extended sense) and must be nonzero.

When `k = 1`, this reduces to the classical notion: `x` is an ordinary eigenvector of `f` with eigenvalue `μ`, meaning `f x = μ • x` and `x ≠ 0`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.HasUnifEigenvector : {R : Type v} -> {M : Type w} -> [CommRing R] -> [AddCommGroup M] -> [Module R M] -> (f : Module.End R M) -> (μ : R) -> (k : ℕ∞) -> (x : M) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.HasUnifEigenvector : {R : Type v} -> {M : Type w} -> [CommRing R] -> [AddCommGroup M] -> [Module R M] -> (f : Module.End R M) -> (μ : R) -> (k : ℕ∞) -> (x : M) -> Prop
```

The implicit type arguments `R` and `M` are the coefficient ring and the module, respectively, with the relevant algebraic structure provided by the typeclass arguments. The argument `f` is the endomorphism under study. The argument `μ` is the candidate eigenvalue (a scalar in `R`). The argument `k` is the uniform order parameter, an element of the extended naturals `ℕ∞` (so it may be a finite natural number or ∞). The final argument `x` is the vector in `M` being tested.

### Conventions

There are no special junk-value or out-of-domain conventions: the predicate is defined for all valid inputs without restriction, and its two constituent conditions (membership in the generalized eigenspace and nonzero) handle every case cleanly.

### Worked examples

- Claim: If `f.HasUnifEigenvector μ 1 x` holds, then `f x = μ • x` (the vector satisfies the classical eigenvector equation).

- Claim: If `f.HasUnifEigenvector μ 1 v` holds, then for every natural number `n`, `(f ^ n) v = μ ^ n • v` (iterating the map scales by the `n`-th power of the eigenvalue).

- Claim: If `f.HasUnifEigenvector μ k x` holds for any `k`, then `f.HasUnifEigenvalue μ k` holds — that is, witnessing a uniform eigenvector for `(f, μ, k)` implies `μ` is a uniform eigenvalue of order `k` for `f`.

- Claim: Conversely, `f.HasUnifEigenvalue μ k` implies the existence of some `v` with `f.HasUnifEigenvector μ k v` — the generalized eigenspace is nonempty (modulo the zero vector) exactly when the eigenvalue condition holds.

### Boundaries

- When `k = 0`, the generalized eigenspace at order `0` is the trivial subspace `{0}`, so no nonzero vector can belong to it; thus `HasUnifEigenvector f μ 0 x` is always `False` for any `f`, `μ`, `x`.
- When `k = ∞`, membership in the generalized eigenspace requires `x` to be annihilated by some finite power of `(f − μ·id)`, with no fixed bound on the power; combined with `x ≠ 0`, this is the most permissive uniform eigenvector condition.
- The zero vector `0 : M` never satisfies `HasUnifEigenvector f μ k 0`, regardless of `f`, `μ`, or `k`, because the nonzero condition `x ≠ 0` is always violated.

### Not to be confused with

- `HasUnifEigenvalue f μ k`: a strictly weaker statement asserting only that the generalized eigenspace is nontrivial, without naming a specific witness vector.
- `HasEigenvector f μ x` (the classical version, `k = 1` specialization): while `HasUnifEigenvector f μ 1 x` is equivalent to classical eigenvector membership, the uniform version generalizes to arbitrary order `k`.
- Membership in `f.genEigenspace μ k` alone: that submodule contains `0`, so it does not require the nonzero condition that `HasUnifEigenvector` enforces.