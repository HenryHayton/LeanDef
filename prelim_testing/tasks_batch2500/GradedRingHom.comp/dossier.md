## Object

`VTask.comp` constructs the composition of two graded ring homomorphisms. Given a graded ring homomorphism `f` from a graded ring `𝒜` to a graded ring `ℬ`, and a graded ring homomorphism `g` from `ℬ` to a graded ring `𝒞`, their composite is a graded ring homomorphism from `𝒜` to `𝒞`. It is simultaneously a composition of the underlying ring homomorphisms and preserves the grading: if an element lies in the `i`-th graded piece of `𝒜`, its image under the composite lies in the `i`-th graded piece of `𝒞`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {ι : Type u_1} -> {A : Type u_2} -> {B : Type u_3} -> {C : Type u_4} -> {σ : Type u_6} -> {τ : Type u_7} -> {ψ : Type u_8} -> [Semiring A] -> [Semiring B] -> [Semiring C] -> [SetLike σ A] -> [SetLike τ B] -> [SetLike ψ C] -> {𝒜 : ι → σ} -> {ℬ : ι → τ} -> {𝒞 : ι → ψ} -> (g : ℬ →+*ᵍ 𝒞) -> (f : 𝒜 →+*ᵍ ℬ) -> 𝒜 →+*ᵍ 𝒞
<!-- PINNED-SIGNATURE:END -->


VTask.comp : {ι : Type u_1} -> {A : Type u_2} -> {B : Type u_3} -> {C : Type u_4} -> {σ : Type u_6} -> {τ : Type u_7} -> {ψ : Type u_8} -> [Semiring A] -> [Semiring B] -> [Semiring C] -> [SetLike σ A] -> [SetLike τ B] -> [SetLike ψ C] -> {𝒜 : ι → σ} -> {ℬ : ι → τ} -> {𝒞 : ι → ψ} -> (g : ℬ →+*ᵍ 𝒞) -> (f : 𝒜 →+*ᵍ ℬ) -> 𝒜 →+*ᵍ 𝒞

The index type `ι` is the common grading monoid/index used by all three graded structures. The types `A`, `B`, `C` are the ambient semirings carrying the gradings. The types `σ`, `τ`, `ψ` are the types of the graded pieces (collections of subobjects), with the `SetLike` instances giving the membership relation between elements and pieces. The families `𝒜 : ι → σ`, `ℬ : ι → τ`, `𝒞 : ι → ψ` assign a graded piece to each index, for the source, intermediate, and target graded rings respectively. The argument `g` is the graded ring homomorphism from `ℬ` to `𝒞` (applied second, on the left). The argument `f` is the graded ring homomorphism from `𝒜` to `ℬ` (applied first, on the right). The result is the graded ring homomorphism from `𝒜` to `𝒞` obtained by first applying `f` then `g`.

## Conventions

Argument order follows the standard mathematical convention for composition: `VTask.comp g f` means "first apply `f`, then apply `g`", matching the notation `g ∘ f`. This mirrors the convention for `RingHom.comp`.

## Worked examples

- Claim: For any graded ring homomorphism `f : 𝒜 →+*ᵍ ℬ` and `g : ℬ →+*ᵍ 𝒞`, the composite `VTask.comp g f` sends an element `a` in the `i`-th piece of `𝒜` to an element in the `i`-th piece of `𝒞`.

- Claim: For any graded ring homomorphisms `f : 𝒜 →+*ᵍ ℬ` and `g : ℬ →+*ᵍ 𝒞`, the underlying ring homomorphism of `VTask.comp g f` equals the composition of the underlying ring homomorphisms of `g` and `f`.

- Claim: Composition of graded ring homomorphisms is associative: for `f : 𝒜 →+*ᵍ ℬ`, `g : ℬ →+*ᵍ 𝒞`, `h : 𝒞 →+*ᵍ 𝒟`, we have `VTask.comp h (VTask.comp g f) = VTask.comp (VTask.comp h g) f` (as graded ring homomorphisms).

## Boundaries

- The function is defined for any two composable graded ring homomorphisms sharing the same index type `ι` and intermediate graded ring `ℬ`; there are no degenerate or partial cases.
- If either `f` or `g` is the identity graded ring homomorphism, the composite equals the other morphism.
- The grading index type `ι` is shared across all three graded structures; compositions mixing different index types are not possible with this construction.
- The membership-preservation property of the composite is obtained directly from those of `f` and `g` without any additional hypotheses.

## Not to be confused with

- `RingHom.comp`: the composition of plain (non-graded) ring homomorphisms, which does not carry or enforce any grading data.
- `GradedRing` identity morphism: the identity graded ring homomorphism, which is the unit for `VTask.comp`, not the composition itself.
- Function composition `Function.comp`: purely set-theoretic composition of the underlying functions, which does not package the ring homomorphism or grading-preservation structure.