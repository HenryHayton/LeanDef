## Object

Given a Lie algebra $L$ over a commutative ring $R$ that is graded by an additive monoid $\iota$ (with grading $\mathcal{L}: \iota \to \mathrm{Submodule}_R\,L$), and given an additive group homomorphism $\varphi: \iota \to R$, `VTask.ofGrading` produces the **Lie derivation** $D: L \to L$ that acts on each homogeneous component by scalar multiplication: if $a \in \mathcal{L}_i$ then $D(a) = \varphi(i) \cdot a$. The action on all of $L$ is the unique $R$-linear extension of this prescription. One checks that this map is indeed a derivation (it is $R$-linear and satisfies the Leibniz rule with respect to the Lie bracket) precisely because $\varphi$ is additive and the grading is multiplicative with respect to the bracket.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofGrading : {ι : Type u_1} -> {R : Type u_3} -> {L : Type u_4} -> [DecidableEq ι] -> [AddCommMonoid ι] -> [CommRing R] -> [LieRing L] -> [LieAlgebra R L] -> (ℒ : ι → Submodule R L) -> [GradedLieAlgebra ℒ] -> (φ : ι →+ R) -> LieDerivation R L L
<!-- PINNED-SIGNATURE:END -->


The type string is inserted automatically above.

- `ι` is the grading index type, required to carry the structure of an `AddCommMonoid` with decidable equality; it parameterises the degrees of the homogeneous components.
- `R` is the coefficient commutative ring.
- `L` is the Lie ring and, simultaneously, the $R$-Lie algebra on which the derivation acts and into which it maps.
- `ℒ` is the grading: a family of $R$-submodules of $L$, one per degree in $\iota$, carrying a `GradedLieAlgebra` instance that asserts $[\mathcal{L}_i, \mathcal{L}_j] \subseteq \mathcal{L}_{i+j}$.
- `φ` is the additive group homomorphism $\varphi: \iota \to R$ that assigns to each degree $i \in \iota$ the scalar $\varphi(i)$ by which homogeneous elements of degree $i$ are multiplied.

## Conventions

No junk-value or edge-case conventions are declared: the definition is total and well-defined for any admissible inputs; there are no degenerate inputs that require a special-case scalar or sentinel output.

## Worked examples

- Claim: For a homogeneous element $a \in \mathcal{L}_i$, `VTask.ofGrading ℒ φ a = φ i • a`. This is the defining property, established by the theorem `ofGrading_apply_apply`: given `ha : a ∈ ℒ i`, we have `VTask.ofGrading ℒ φ a = φ i • a`.

- Claim: If $\varphi = 0$ (the zero additive homomorphism), then `VTask.ofGrading ℒ 0` is the zero Lie derivation. For every homogeneous $a \in \mathcal{L}_i$, the action gives $0 \cdot a = 0$; by linearity the whole derivation is zero.

- Claim: If $L$ is concentrated in degree $0$ (i.e., $\mathcal{L}_0 = L$ and $\mathcal{L}_i = 0$ for $i \neq 0$), then `VTask.ofGrading ℒ φ` acts on every element as multiplication by $\varphi(0)$. Since $\varphi(0) = 0$ for any additive homomorphism, the derivation is again zero in this case.

## Boundaries

- The derivation is defined on all of $L$, not merely on homogeneous elements; it extends linearly from the homogeneous pieces using the direct-sum decomposition given by the grading.
- When $\varphi$ is the zero map, `VTask.ofGrading ℒ φ` is the zero derivation regardless of the grading.
- The `GradedLieAlgebra` hypothesis is essential: it ensures $[\mathcal{L}_i, \mathcal{L}_j] \subseteq \mathcal{L}_{i+j}$, and the additivity $\varphi(i+j) = \varphi(i) + \varphi(j)$ is then exactly what forces the Leibniz rule to hold.
- There is no restriction on $\iota$ beyond `AddCommMonoid` with `DecidableEq`; in particular $\iota$ need not be $\mathbb{Z}$ or $\mathbb{N}$.

## Not to be confused with

- `LieDerivation.inner`: the inner derivation $\mathrm{ad}(x)$, which acts by the Lie bracket with a fixed element rather than by scalar multiplication on homogeneous components.
- A graded algebra **automorphism** that exponentiates a graded derivation: `ofGrading` produces a derivation (an infinitesimal object), not an automorphism.
- The `GradedLieAlgebra` typeclass itself: that is the hypothesis encoding the grading's compatibility with the bracket, whereas `VTask.ofGrading` is the derived construction of a specific derivation from such a structure.