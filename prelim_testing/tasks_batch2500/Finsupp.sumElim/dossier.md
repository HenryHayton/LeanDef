## Object

Given two finitely-supported functions `f : α →₀ γ` and `g : β →₀ γ`, `VTask.sumElim f g` is the finitely-supported function on the disjoint-union type `α ⊕ β` that sends `Sum.inl x` to `f x` and `Sum.inr y` to `g y`. Its support is precisely the disjoint union of the supports of `f` and `g`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sumElim : {α : Type u_1} -> {β : Type u_2} -> {γ : Type u_3} -> [Zero γ] -> (f : α →₀ γ) -> (g : β →₀ γ) -> α ⊕ β →₀ γ
<!-- PINNED-SIGNATURE:END -->


`VTask.sumElim : {α : Type u_1} -> {β : Type u_2} -> {γ : Type u_3} -> [Zero γ] -> (f : α →₀ γ) -> (g : β →₀ γ) -> α ⊕ β →₀ γ`

The type parameters `α`, `β`, and `γ` are the domain types and the codomain type, respectively; they are inferred implicitly. The `[Zero γ]` instance is required because finitely-supported functions need a zero value to define "finitely many non-zero values". The first explicit argument `f` is the finitely-supported function on `α`, providing values for left summands. The second explicit argument `g` is the finitely-supported function on `β`, providing values for right summands.

## Conventions

No junk-value or edge conventions are declared for this definition: the construction is total and well-behaved for all valid inputs, including the empty finsupp on either or both sides.

## Worked examples

- Claim: If `f` is the finsupp on `Fin 1` sending `0` to `(3 : ℤ)` and `g` is the finsupp on `Fin 1` sending `0` to `(5 : ℤ)`, then `VTask.sumElim f g (Sum.inl 0) = 3`.

- Claim: If `f` is the finsupp on `Fin 1` sending `0` to `(3 : ℤ)` and `g` is the finsupp on `Fin 1` sending `0` to `(5 : ℤ)`, then `VTask.sumElim f g (Sum.inr 0) = 5`.

- Claim: For any `f : α →₀ γ` and `g : β →₀ γ`, the support of `VTask.sumElim f g` equals the disjoint sum (i.e., `Finset.disjSum`) of the supports of `f` and `g`.

- Claim: `VTask.sumElim (0 : α →₀ γ) (0 : β →₀ γ) = 0` — combining two zero finsupps yields the zero finsupp on `α ⊕ β`.

## Boundaries

- If `f = 0` (the zero finsupp on `α`), then `VTask.sumElim f g` acts as zero on all `Sum.inl` inputs and as `g` on all `Sum.inr` inputs.
- If `g = 0`, the situation is symmetric: `VTask.sumElim f g` acts as `f` on `Sum.inl` inputs and as zero on `Sum.inr` inputs.
- If both `f = 0` and `g = 0`, the result is the zero finsupp on `α ⊕ β` with empty support.
- The supports of `f` and `g` are always "disjoint" in the sense that elements of `f.support` are tagged with `inl` and elements of `g.support` are tagged with `inr`, so there is no collision regardless of overlap between the underlying index types.

## Not to be confused with

- `Finsupp.sumFinsuppLEquivProdFinsupp` (or similar): an equivalence between `α ⊕ β →₀ γ` and `(α →₀ γ) × (β →₀ γ)`, of which `VTask.sumElim` is essentially the "backward" (construction) direction.
- `Sum.elim` on ordinary functions: the plain function-level combinator `Sum.elim f g : α ⊕ β → γ`; `VTask.sumElim` is the finsupp-aware version that also tracks support.
- `Finsupp.comapDomain`: maps a finsupp along a function on the index type, but is not tailored to the disjoint-sum structure.