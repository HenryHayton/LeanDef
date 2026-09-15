## VTask.orthogonal

### Object

Given a Lie module $M$ over a commutative ring $R$ with a Lie ring $L$ acting on it, and a bilinear form $\Phi : M \times M \to R$ that is *Lie-invariant* (meaning $\Phi(\![x, m]\!, n) + \Phi(m, \![x, n]\!) = 0$ for all $x \in L$ and $m, n \in M$), the **orthogonal complement** of a Lie submodule $N \subseteq M$ is the set of all elements $y \in M$ satisfying $\Phi(x, y) = 0$ for every $x \in N$. The key content of the construction is that this set is not merely a submodule but again a **Lie submodule**: it is closed under the Lie bracket action of $L$, which uses the Lie-invariance of $\Phi$ in an essential way.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.orthogonal : {R : Type u_1} -> {L : Type u_2} -> {M : Type u_3} -> [CommRing R] -> [LieRing L] -> [AddCommGroup M] -> [Module R M] -> [LieRingModule L M] -> (Φ : LinearMap.BilinForm R M) -> (hΦ_inv : LinearMap.BilinForm.lieInvariant L Φ) -> (N : LieSubmodule R L M) -> LieSubmodule R L M
<!-- PINNED-SIGNATURE:END -->


```
VTask.orthogonal : {R : Type u_1} -> {L : Type u_2} -> {M : Type u_3} -> [CommRing R] -> [LieRing L] -> [AddCommGroup M] -> [Module R M] -> [LieRingModule L M] -> (Φ : LinearMap.BilinForm R M) -> (hΦ_inv : LinearMap.BilinForm.lieInvariant L Φ) -> (N : LieSubmodule R L M) -> LieSubmodule R L M
```

`R` is the base commutative ring; `L` is the Lie ring acting on the module; `M` is the module being acted upon. The instance arguments supply the algebraic structures: `CommRing R`, `LieRing L`, `AddCommGroup M`, `Module R M`, and `LieRingModule L M`. `Φ` is the bilinear form on `M` with respect to which orthogonality is measured. `hΦ_inv` is the proof that `Φ` is Lie-invariant with respect to the $L$-action; this invariance is what guarantees the orthogonal complement is closed under Lie bracket. `N` is the Lie submodule whose orthogonal complement is to be formed.

### Conventions

There are no special junk-value or boundary conventions: the construction is total and well-defined for any Lie-invariant bilinear form and any Lie submodule.

### Worked examples

- Claim: For any Lie-invariant bilinear form $\Phi$ on $M$ and any Lie submodule $N$, an element $y \in M$ belongs to `VTask.orthogonal Φ hΦ_inv N` if and only if $\Phi(x, y) = 0$ for all $x \in N$.

- Claim: The underlying submodule of `VTask.orthogonal Φ hΦ_inv N` coincides with the ordinary bilinear-form orthogonal complement of the underlying submodule of $N$; that is, `(VTask.orthogonal Φ hΦ_inv N).toSubmodule = Φ.orthogonal N.toSubmodule`.

- Claim: When $L$ is a Lie algebra over a field $K$ and $I$ is an atomic Lie ideal, `VTask.orthogonal Φ hΦ_inv I` and $I$ are complementary as submodules (and as Lie submodules), provided $\Phi$ is nondegenerate and every atom of the ideal lattice is non-abelian.

- Claim: The zero element $0 \in M$ always belongs to `VTask.orthogonal Φ hΦ_inv N`, since $\Phi(x, 0) = 0$ for all $x$ by linearity of $\Phi$.

### Boundaries

- If $N$ is the zero submodule, the orthogonal complement is all of $M$ (every element is trivially orthogonal to the zero submodule).
- If $N = M$, the orthogonal complement is the *radical* of $\Phi$: the set of $y$ with $\Phi(x, y) = 0$ for all $x \in M$. If $\Phi$ is nondegenerate, this is the zero submodule.
- The intersection $N \cap \operatorname{VTask.orthogonal}(\Phi, h, N)$ need not be trivial in general; it equals zero exactly when $\Phi$ restricts to a nondegenerate form on $N$.
- When $\Phi$ is the zero bilinear form, the orthogonal complement of any $N$ is all of $M$.

### Not to be confused with

- `LinearMap.BilinForm.orthogonal`: The purely linear-algebraic orthogonal complement, which is a submodule but not necessarily a Lie submodule; `VTask.orthogonal` lifts this to the Lie-submodule level using Lie-invariance.
- The *orthogonal complement in an inner product space*: that notion requires positive-definiteness and a symmetric form; this construction works for any Lie-invariant bilinear form.
- The *centralizer* or *normalizer* of a Lie submodule: those are defined by the Lie bracket alone, not by a bilinear form.
