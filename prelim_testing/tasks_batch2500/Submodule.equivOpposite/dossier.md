## VTask.equivOpposite

### Object

A canonical ring isomorphism between two naturally related semiring structures built from a (possibly non-commutative) `R`-algebra `A` and its opposite algebra `Aᵐᵒᵖ`:

- **Domain**: the semiring `Submodule R Aᵐᵒᵖ` of `R`-submodules of the *opposite* algebra.
- **Codomain**: the opposite semiring `(Submodule R A)ᵐᵒᵖ` — that is, the semiring of `R`-submodules of `A`, but with its own multiplication reversed.

Because the multiplication of `R`-submodules of `Aᵐᵒᵖ` is exactly the "reversed" multiplication of submodules of `A`, these two semirings are isomorphic, and `VTask.equivOpposite` makes that isomorphism explicit as a bundled `≃+*`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.equivOpposite : {R : Type u} -> [CommSemiring R] -> {A : Type v} -> [Semiring A] -> [Algebra R A] -> Submodule R Aᵐᵒᵖ ≃+* (Submodule R A)ᵐᵒᵖ
<!-- PINNED-SIGNATURE:END -->


```
VTask.equivOpposite : {R : Type u} -> [CommSemiring R] -> {A : Type v} -> [Semiring A] -> [Algebra R A] -> Submodule R Aᵐᵒᵖ ≃+* (Submodule R A)ᵐᵒᵖ
```

`R` is the commutative base semiring over which the algebra structure is defined. `A` is the `R`-algebra whose submodule lattice is being studied. The `CommSemiring R`, `Semiring A`, and `Algebra R A` instances supply the algebraic structure needed so that both sides carry their semiring of submodules. There are no explicit term-level arguments: the isomorphism is entirely determined by the types `R` and `A` and their instances.

### Conventions

Because `R` and `A` are implicit type arguments inferred from context, there are no junk-value or out-of-domain conventions to declare: the definition is structurally total and all inputs are constrained by typeclass assumptions.

### Worked examples

- Claim: `VTask.equivOpposite` is a ring isomorphism, so its inverse composed with itself is the identity on `Submodule R Aᵐᵒᵖ`; concretely, for any `p : Submodule R Aᵐᵒᵖ`, `VTask.equivOpposite.symm (VTask.equivOpposite p) = p`.

- Claim: The forward direction sends an `R`-submodule `p` of `Aᵐᵒᵖ` to the `R`-submodule of `A` consisting of those elements `a : A` whose opposite `op a` lies in `p`, wrapped in `MulOpposite.op` to live in `(Submodule R A)ᵐᵒᵖ`.

- Claim: `VTask.equivOpposite` preserves addition of submodules: for `p q : Submodule R Aᵐᵒᵖ`, `VTask.equivOpposite (p + q) = VTask.equivOpposite p + VTask.equivOpposite q` (in `(Submodule R A)ᵐᵒᵖ`, where addition of submodules is the same as the sum/span of the two).

- Claim: `VTask.equivOpposite` preserves multiplication: for `p q : Submodule R Aᵐᵒᵖ`, `VTask.equivOpposite (p * q) = VTask.equivOpposite p * VTask.equivOpposite q`; because multiplication is reversed in the opposite ring, this is compatible with the reversal of submodule products under passing to the opposite algebra.

### Boundaries

- When `A` is a commutative algebra, `Aᵐᵒᵖ` is canonically isomorphic to `A` itself, so `VTask.equivOpposite` reduces to the trivial identity-like isomorphism on submodules; however, `VTask.equivOpposite` does not specialise away or simplify — it still witnesses the same structural fact.
- The definition applies to semirings (not just rings): no additive inverses are required.
- The submodule `⊥` (zero submodule) is sent to `op ⊥`, and `⊤` (whole module) is sent to `op ⊤`, as both are preserved by the underlying comap construction.
- Because `VTask.equivOpposite` is a `≃+*` (ring equivalence), both `VTask.equivOpposite` and its inverse `VTask.equivOpposite.symm` are ring homomorphisms and are inverses of each other.

### Not to be confused with

- `MulOpposite.opLinearEquiv R : A ≃ₗ[R] Aᵐᵒᵖ` — a linear equivalence between `A` and `Aᵐᵒᵖ` as modules, acting on *elements*, not on submodules.
- `Submodule.orderIsoMapComap` — an order isomorphism between submodules along a linear map, which does not account for the semiring (multiplication) structure on submodules.
- The canonical map `MulOpposite.op : Submodule R A → (Submodule R A)ᵐᵒᵖ` — this merely wraps a submodule in `MulOpposite` without changing the underlying set, and is not a map from `Submodule R Aᵐᵒᵖ`.
