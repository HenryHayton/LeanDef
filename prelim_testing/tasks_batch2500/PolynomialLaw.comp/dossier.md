## Object

`VTask.comp` constructs the composition of two polynomial maps between modules. A *polynomial map* from an $R$-module $M$ to an $R$-module $N$ is a natural transformation of set-valued functors that, for every commutative $R$-algebra $S$, sends the scalar extension $M \otimes_R S$ into $N \otimes_R S$ in a way that is compatible with algebra homomorphisms. Given such a map $f : M \to N$ and another $g : N \to P$, their composition $g \circ f$ is the polynomial map $M \to P$ obtained by applying $f$ first and then $g$ at each scalar extension.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {R : Type u} -> [CommSemiring R] -> {M : Type u_1} -> [AddCommMonoid M] -> [Module R M] -> {N : Type u_2} -> [AddCommMonoid N] -> [Module R N] -> {P : Type u_3} -> [AddCommMonoid P] -> [Module R P] -> (g : N →ₚₗ[R] P) -> (f : M →ₚₗ[R] N) -> M →ₚₗ[R] P
<!-- PINNED-SIGNATURE:END -->


`VTask.comp : {R : Type u} -> [CommSemiring R] -> {M : Type u_1} -> [AddCommMonoid M] -> [Module R M] -> {N : Type u_2} -> [AddCommMonoid N] -> [Module R N] -> {P : Type u_3} -> [AddCommMonoid P] -> [Module R P] -> (g : N →ₚₗ[R] P) -> (f : M →ₚₗ[R] N) -> M →ₚₗ[R] P`

`R` is the commutative semiring of scalars shared by all three modules. `M`, `N`, and `P` are the source, intermediate, and target $R$-modules, respectively, each equipped with their additive-monoid and module structures as implicit arguments. `g` is the outer polynomial map from $N$ to $P$; `f` is the inner polynomial map from $M$ to $N$. The result is the composite polynomial map from $M$ to $P$.

## Conventions

No special junk-value or edge-case conventions have been declared for this definition: it is a total construction on all valid inputs, and the compatibility condition is enforced structurally.

## Worked examples

- Claim: Composing the identity polynomial map on $M$ with any polynomial map $f : M \to N$ yields a polynomial map from $M$ to $N$ (here the identity is treated as `VTask.comp f id`).

- Claim: For polynomial maps $f : M \to N$, $g : N \to P$, and $h : P \to Q$, the composition `VTask.comp (VTask.comp h g) f` equals `VTask.comp h (VTask.comp g f)` — composition is associative.

- Claim: If $f : M \to N$ and $g : N \to P$ are polynomial maps, then for every commutative $R$-algebra $S$ and every element $m \in M \otimes_R S$, the composite `VTask.comp g f` evaluated at $m$ equals $g$ evaluated at $f(m)$.

## Boundaries

- When $M = N = P$ and both $f$ and $g$ are the zero polynomial map, the composition is again the zero polynomial map.
- When either $f$ or $g$ is a constant polynomial map, the composition reduces to a constant map (taking the value that $g$ assigns to the constant value of $f$).
- The definition is total: it requires no extra hypotheses beyond the module structures already present in the signature, and it produces a well-formed polynomial map for any pair of composable polynomial maps.
- The roles of $g$ and $f$ are **not** symmetric: `VTask.comp g f` applies $f$ first, then $g$; swapping them yields a type error unless $M = P$.

## Not to be confused with

- **Linear map composition (`LinearMap.comp`)**: composes ordinary $R$-linear maps, which are a special case of polynomial maps but carry linearity as a definitional constraint rather than just polynomial naturality.
- **Ring homomorphism composition**: composes morphisms of rings/semirings, not of modules over a fixed base ring.
- **Function composition (`Function.comp`)**: raw set-level composition with no algebraic compatibility requirements; polynomial maps require naturality with respect to base-change.
