## Object

Given a commutative ring $R$, an ideal $I \subseteq R$, two $R$-modules $M$ and $N$, and an $R$-linear map $f : M \to N$, `VTask.map I f` is the induced $R$-linear map on $I$-adic Cauchy sequences: it sends each Cauchy sequence $(a_n)_{n \geq 0}$ in $M$ (in the sense that $a_m \equiv a_n \pmod{I^m \cdot M}$ whenever $m \leq n$) to the componentwise image sequence $(f(a_n))_{n \geq 0}$ in $N$, which is again an $I$-adic Cauchy sequence.

In other words, `VTask.map` is the functorial action of the $I$-adic Cauchy sequence construction on linear maps between modules.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.map : {R : Type u_1} -> [CommRing R] -> (I : Ideal R) -> {M : Type u_2} -> [AddCommGroup M] -> [Module R M] -> {N : Type u_3} -> [AddCommGroup N] -> [Module R N] -> (f : M →ₗ[R] N) -> AdicCompletion.AdicCauchySequence I M →ₗ[R] AdicCompletion.AdicCauchySequence I N
<!-- PINNED-SIGNATURE:END -->


VTask.map : {R : Type u_1} -> [CommRing R] -> (I : Ideal R) -> {M : Type u_2} -> [AddCommGroup M] -> [Module R M] -> {N : Type u_3} -> [AddCommGroup N] -> [Module R N] -> (f : M →ₗ[R] N) -> AdicCompletion.AdicCauchySequence I M →ₗ[R] AdicCompletion.AdicCauchySequence I N

The ambient commutative ring $R$ and the two $R$-modules $M$ and $N$ are implicit type arguments, inferred from context. The first explicit argument `I` is the ideal of $R$ with respect to which the adic topology and the Cauchy condition are defined. The second explicit argument `f` is the $R$-linear map from $M$ to $N$ being promoted to the level of Cauchy sequences.

## Conventions

There are no declared junk-value or boundary conventions for this definition: the construction is well-defined and total for every ideal $I$ and every $R$-linear map $f$.

## Worked examples

- Claim: For the zero linear map $0 : M \to N$, `VTask.map I 0` sends every adic Cauchy sequence $(a_n)$ to the zero Cauchy sequence $(0)_n$.

- Claim: For the identity linear map $\mathrm{id} : M \to M$, `VTask.map I (LinearMap.id)` acts as the identity on adic Cauchy sequences: if $a$ is a Cauchy sequence, then `(VTask.map I LinearMap.id) a = a`.

- Claim: `VTask.map` respects composition: for $R$-linear maps $f : M \to N$ and $g : N \to P$, the map induced by $g \circ f$ equals the composition of the induced maps, i.e., `VTask.map I (g ∘ₗ f) = (VTask.map I g) ∘ₗ (VTask.map I f)`.

- Claim: For any adic Cauchy sequences $a, b$ and scalar $r : R$, the induced map satisfies `VTask.map I f (a + b) = VTask.map I f a + VTask.map I f b` and `VTask.map I f (r • a) = r • VTask.map I f a`, reflecting that the output is an $R$-linear map.

## Boundaries

- When $I = \top$ (the unit ideal), all powers $I^m = \top$, so the Cauchy condition becomes vacuous and every sequence is Cauchy; `VTask.map I f` still acts componentwise and is well-typed.
- When $I = 0$ (the zero ideal), $I^m = 0$ for $m \geq 1$, making the Cauchy condition require that differences lie in $0 \cdot M = 0$, i.e., sequences must be eventually constant; `VTask.map I f` applies $f$ termwise and preserves this constancy.
- When $f = 0$ (the zero linear map), `VTask.map I f` is the zero linear map on Cauchy sequences.
- The definition is total: no restriction on $I$ or $f$ is needed.

## Not to be confused with

- `AdicCompletion.map`: the induced map on the $I$-adic completion (the quotient/limit), not on the underlying Cauchy sequences.
- `AdicCompletion.AdicCauchySequence` itself: the subtype/submodule of sequences satisfying the Cauchy condition, which is the domain and codomain of `VTask.map`, not the map itself.
- Pointwise application of $f$ to a sequence without checking the Cauchy property: `VTask.map I f` bundles the proof that the image is again Cauchy, making it a map of the structured subtype.