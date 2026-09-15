## VTask.equivOfEq

### Object

Given two subalgebras `S` and `T` of an `R`-algebra `A` that are equal as subalgebras, `VTask.equivOfEq S T h` is the canonical algebra isomorphism (an `R`-algebra equivalence) from `S` to `T`. It is the unique "trivial" equivalence produced by the equality proof alone, acting as the identity on the underlying elements — it simply reinterprets a member of `S` as a member of `T` by transporting the membership proof along `h`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.equivOfEq : {R : Type u} -> {A : Type v} -> [CommSemiring R] -> [Semiring A] -> [Algebra R A] -> (S T : Subalgebra R A) -> (h : S = T) -> ↥S ≃ₐ[R] ↥T
<!-- PINNED-SIGNATURE:END -->


`VTask.equivOfEq : {R : Type u} -> {A : Type v} -> [CommSemiring R] -> [Semiring A] -> [Algebra R A] -> (S T : Subalgebra R A) -> (h : S = T) -> ↥S ≃ₐ[R] ↥T`

The implicit type `R` is the commutative semiring of scalars; `A` is the ambient semiring that is also an `R`-algebra. The instance arguments supply the algebraic structures. `S` and `T` are the two subalgebras of `A` over `R` between which the equivalence is built. `h` is the proof that `S` and `T` are equal as subalgebras.

### Conventions

There are no junk-value or out-of-domain conventions to declare: the function is total and its behaviour is fully determined by the equality proof `h`. When `h` is `rfl` (i.e., `S = T` trivially because `S` and `T` are definitionally the same), the resulting equivalence is definitionally the identity.

### Worked examples

- Claim: For any subalgebra `S`, `VTask.equivOfEq S S rfl` maps an element `x : ↥S` to the element with the same underlying value in `↥S`.

- Claim: For any subalgebra `S` and proof `h : S = S`, the forward map of `VTask.equivOfEq S S h` applied to an element `x : ↥S` satisfies `(VTask.equivOfEq S S h x : A) = (x : A)` — the coercion to `A` is unchanged.

- Claim: For subalgebras `S T : Subalgebra R A` with `h : S = T`, the composition of `VTask.equivOfEq S T h` followed by `(VTask.equivOfEq S T h).symm` is the identity on `↥S` (the equivalence is self-inverse via its symmetric counterpart).

- Claim: For subalgebras `S T U : Subalgebra R A` with `h₁ : S = T` and `h₂ : T = U`, composing `VTask.equivOfEq S T h₁` with `VTask.equivOfEq T U h₂` yields an algebra equivalence that acts the same as `VTask.equivOfEq S U (h₁.trans h₂)` on underlying elements.

### Boundaries

- When `h : S = T` is `rfl`, the equivalence is definitionally the identity map on the subtype `↥S`.
- The construction works for any equality proof `h`, regardless of how it was obtained (propositional equality suffices; definitional equality is not required).
- The resulting equivalence is an `R`-algebra equivalence, so it respects addition, multiplication, scalar multiplication by `R`, and the algebra map from `R`.
- Since subalgebras contain the unit and are closed under the algebra operations, the algebra equivalence structure (including `commutes'`) holds automatically.
- The equivalence goes from `↥S` to `↥T` as subtypes; the coercions to `A` of corresponding elements are equal.

### Not to be confused with

- `LinearEquiv.ofEq`: the analogous construction for submodules, which produces only a linear equivalence, not a full algebra equivalence.
- `Equiv.setCongr`: the analogous construction for sets/subtypes, which produces only a bare type equivalence with no algebraic structure.
- `AlgEquiv.refl`: the reflexivity algebra equivalence on an algebra `A` itself (not a subalgebra), which is the identity equivalence `A ≃ₐ[R] A`.