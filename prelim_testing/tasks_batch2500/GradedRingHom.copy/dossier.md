## Object

`VTask.copy` produces a new graded ring homomorphism that is definitionally equal to a given one, but whose underlying function is replaced by a specified function that is propositionally (but perhaps not definitionally) equal to the original. This is a standard "copy" idiom: the new map agrees with the old one in every mathematical sense, but carries a different term for its underlying function, which can help Lean's kernel reduce expressions that would otherwise be stuck.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {ι : Type u_1} -> {A : Type u_2} -> {B : Type u_3} -> {σ : Type u_6} -> {τ : Type u_7} -> [Semiring A] -> [Semiring B] -> [SetLike σ A] -> [SetLike τ B] -> {𝒜 : ι → σ} -> {ℬ : ι → τ} -> (f : 𝒜 →+*ᵍ ℬ) -> (f' : A → B) -> (h : f' = ⇑f) -> 𝒜 →+*ᵍ ℬ
<!-- PINNED-SIGNATURE:END -->


`VTask.copy : {ι : Type u_1} -> {A : Type u_2} -> {B : Type u_3} -> {σ : Type u_6} -> {τ : Type u_7} -> [Semiring A] -> [Semiring B] -> [SetLike σ A] -> [SetLike τ B] -> {𝒜 : ι → σ} -> {ℬ : ι → τ} -> (f : 𝒜 →+*ᵍ ℬ) -> (f' : A → B) -> (h : f' = ⇑f) -> 𝒜 →+*ᵍ ℬ`

The implicit type arguments `ι`, `A`, `B`, `σ`, `τ` are the index type, source ring, target ring, and their respective `SetLike` container types. The two `Semiring` instances equip `A` and `B` with ring structure, while the two `SetLike` instances allow `𝒜` and `ℬ` to be families of subsets (e.g., subgroups or submodules) of `A` and `B` respectively. The grading data `𝒜 : ι → σ` and `ℬ : ι → τ` specify how each grade index maps to a piece of the ring. The argument `f` is the original graded ring homomorphism being copied. The argument `f'` is the new function to use as the underlying map. The argument `h` is the proof that `f'` is propositionally equal to the coercion of `f` to a function.

## Conventions

The copy construction is total: any function `f'` together with a proof `h` that it equals the coercion of `f` is accepted, even when `f'` and `⇑f` are already definitionally equal. The resulting graded ring homomorphism is propositionally equal to the original `f` as a graded ring homomorphism (not merely as a function).

## Worked examples

- Claim: For any graded ring homomorphism `f : 𝒜 →+*ᵍ ℬ`, passing `f' = ⇑f` and `h = rfl` gives a copy that is propositionally equal to `f`; that is, `VTask.copy f (⇑f) rfl = f`.

- Claim: The coercion of `VTask.copy f f' h` to a function equals `f'`; that is, `⇑(VTask.copy f f' h) = f'`.

- Claim: For any graded ring homomorphism `f` and any element `a` in grade `i` (i.e., `a ∈ 𝒜 i`), the copy satisfies `VTask.copy f f' h a ∈ ℬ i`, since the graded-membership condition is inherited from `f` via the proof `h`.

## Boundaries

The definition is total: there are no restrictions on the choice of `f'` beyond `h : f' = ⇑f`. When `f' = ⇑f` definitionally (not just propositionally), the copy is redundant but still valid. The copied map is always propositionally equal to the original (`copy_eq`), so no information is lost. The underlying function of the copy is exactly `f'` (not the coercion of `f`), which is the whole point of the construction.

## Not to be confused with

- `RingHom.copy`: the analogous construction for plain (non-graded) ring homomorphisms; `VTask.copy` additionally preserves the graded-membership condition.
- The identity graded ring homomorphism: unlike `copy`, the identity is a specific canonical map, not a renaming of an existing one.
- Definitional equality vs. propositional equality: `VTask.copy` does not change the mathematical map at all; it only introduces a new term for the same function, useful for resolving definitional equality issues in the type checker.