## Object

`VTask.comp f g` is the composite of two continuous order homomorphisms. Given a continuous order-preserving map `f : β → γ` and a continuous order-preserving map `g : α → β`, it produces the composite map `α → γ` that first applies `g` and then `f`, and certifies that this composite is again both continuous and order-preserving.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {α : Type u_2} -> {β : Type u_3} -> {γ : Type u_4} -> [TopologicalSpace α] -> [Preorder α] -> [TopologicalSpace β] -> [Preorder β] -> [TopologicalSpace γ] -> [Preorder γ] -> (f : β →Co γ) -> (g : α →Co β) -> α →Co γ
<!-- PINNED-SIGNATURE:END -->


`VTask.comp : {α : Type u_2} -> {β : Type u_3} -> {γ : Type u_4} -> [TopologicalSpace α] -> [Preorder α] -> [TopologicalSpace β] -> [Preorder β] -> [TopologicalSpace γ] -> [Preorder γ] -> (f : β →Co γ) -> (g : α →Co β) -> α →Co γ`

The type parameters `α`, `β`, and `γ` are the domain, intermediate, and codomain types respectively, each carrying a topology (given by the `TopologicalSpace` instances) and a preorder (given by the `Preorder` instances). The argument `f` is a continuous order homomorphism from `β` to `γ`; it is applied second. The argument `g` is a continuous order homomorphism from `α` to `β`; it is applied first. The result is a continuous order homomorphism from `α` directly to `γ`.

## Conventions

There are no junk-value or edge conventions to declare: the operation is defined for all valid pairs of composable continuous order homomorphisms without any domain restriction or special-case output.

## Worked examples

- Claim: Composing two identity-like continuous order homomorphisms on a type yields a map that agrees with the identity on every element.

- Claim: For any `f : β →Co γ` and `g : α →Co β`, the underlying function of `VTask.comp f g` sends each `a : α` to `f (g a)`.

- Claim: `VTask.comp f g` is order-preserving: if `a₁ ≤ a₂` in `α`, then `(VTask.comp f g) a₁ ≤ (VTask.comp f g) a₂` in `γ`, because both `g` and `f` are order-preserving.

- Claim: `VTask.comp f g` is continuous: preimages of open sets in `γ` under `VTask.comp f g` are open in `α`, because both `g` and `f` are continuous.

## Boundaries

- The operation is total: it is defined for every pair of composable continuous order homomorphisms, with no restrictions beyond the type-checking requirement that the codomain of `g` equals the domain of `f`.
- When one of the components is an identity morphism, the composite is the other component (up to definitional or propositional equality of the underlying functions).
- Composition is associative: `VTask.comp (VTask.comp h f) g` and `VTask.comp h (VTask.comp f g)` agree as elements of the appropriate hom-type.

## Not to be confused with

- `OrderHom.comp`: composition of order-preserving maps that carries no continuity structure — `VTask.comp` additionally enforces and preserves continuity.
- `ContinuousMap.comp`: composition of continuous maps that carries no order structure — `VTask.comp` additionally enforces and preserves the order-homomorphism property.
- Function composition `Function.comp`: a bare set-theoretic composition with no topological or order properties tracked in the type.