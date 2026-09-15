## VTask.maxTrivSubmodule

### Object

Given a Lie algebra $L$ acting on a module $M$ (a Lie module), the **maximal trivial submodule** is the largest submodule of $M$ on which $L$ acts trivially — that is, the set of all elements $m \in M$ such that $[x, m] = 0$ for every $x \in L$. It is a Lie submodule of $M$ in its own right, and every submodule of $M$ on which $L$ acts trivially is contained in it.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.maxTrivSubmodule : (R : Type u) -> (L : Type v) -> (M : Type w) -> [CommRing R] -> [LieRing L] -> [LieAlgebra R L] -> [AddCommGroup M] -> [Module R M] -> [LieRingModule L M] -> [LieModule R L M] -> LieSubmodule R L M
<!-- PINNED-SIGNATURE:END -->


The first three arguments are the types: $R$ is the commutative ring of scalars, $L$ is the Lie algebra, and $M$ is the module being acted upon. The remaining arguments are the typeclass instances equipping $R$ with a commutative ring structure, $L$ with a Lie ring and $R$-Lie algebra structure, and $M$ with an abelian group, $R$-module, Lie ring module over $L$, and full Lie module structure. No explicit data beyond these instances is required; the submodule is determined entirely by the Lie action.

### Conventions

No junk-value or defaulting conventions are declared: the definition is total and well-typed whenever the required typeclasses are satisfied, and its value is uniquely determined by those structures.

### Worked examples

- Claim: An element $m \in M$ belongs to `VTask.maxTrivSubmodule R L M` if and only if $[x, m] = 0$ for all $x \in L$.

- Claim: If $L$ acts trivially on all of $M$ (i.e., $[x, m] = 0$ for every $x \in L$ and $m \in M$), then `VTask.maxTrivSubmodule R L M` equals the top submodule of $M$.

- Claim: The zero element of $M$ always belongs to `VTask.maxTrivSubmodule R L M`, since $[x, 0] = 0$ for every $x \in L$.

- Claim: If $N$ is any Lie submodule of $M$ on which $L$ acts trivially, then $N \leq$ `VTask.maxTrivSubmodule R L M`.

### Boundaries

- If $L$ acts trivially on all of $M$, then `VTask.maxTrivSubmodule R L M` is the entire module (top submodule).
- If the Lie action is free (no nonzero element is killed by all of $L$), then `VTask.maxTrivSubmodule R L M` is the zero submodule.
- The zero submodule is always contained in `VTask.maxTrivSubmodule R L M`, so it is never empty.
- The submodule is closed under addition, scalar multiplication by $R$, and the Lie bracket action of $L$ (in the sense required by a Lie submodule), so it is itself a legitimate Lie submodule.

### Not to be confused with

- The **trivial Lie module** or **trivial representation**: a construction that forces a trivial action on a given abelian group, rather than extracting the trivially-acted-upon part of a given module.
- **LieModule.IsTrivial**: a typeclass asserting that the entire Lie action on $M$ is trivial, rather than carving out the largest submodule with that property.
- **LieSubmodule.center** or the center of $L$ itself: the center concerns elements of the Lie algebra commuting with all others, not elements of a module annihilated by the action.
