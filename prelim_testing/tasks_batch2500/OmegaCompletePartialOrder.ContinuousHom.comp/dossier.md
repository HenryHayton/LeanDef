## Object

`VTask.comp f g` is the composition of two Scott-continuous functions between omega-complete partial orders (ωCPOs). Given a continuous map `f : β →𝒄 γ` and a continuous map `g : α →𝒄 β`, it produces a continuous map `α →𝒄 γ` whose underlying function is the ordinary function composition `f ∘ g`. The key content is that this composition is again Scott-continuous — it preserves the suprema of ω-chains — so it lives in the category of ωCPOs and continuous morphisms.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {α : Type u_2} -> {β : Type u_3} -> {γ : Type u_4} -> [OmegaCompletePartialOrder α] -> [OmegaCompletePartialOrder β] -> [OmegaCompletePartialOrder γ] -> (f : β →𝒄 γ) -> (g : α →𝒄 β) -> α →𝒄 γ
<!-- PINNED-SIGNATURE:END -->


{VTask.comp : {α : Type u_2} -> {β : Type u_3} -> {γ : Type u_4} -> [OmegaCompletePartialOrder α] -> [OmegaCompletePartialOrder β] -> [OmegaCompletePartialOrder γ] -> (f : β →𝒄 γ) -> (g : α →𝒄 β) -> α →𝒄 γ}

The three implicit type arguments `α`, `β`, `γ` are the carrier types of the three ωCPOs involved. The three typeclass arguments supply the ωCPO structure on each carrier. The explicit argument `f` is the outer continuous map (from `β` to `γ`); the explicit argument `g` is the inner continuous map (from `α` to `β`). The result is the continuous map from `α` to `γ` obtained by composing `g` first, then `f`.

## Conventions

No junk-value or edge conventions are declared for this definition: it is a total constructor whose inputs are always well-formed continuous homomorphisms, and it always produces a valid continuous homomorphism with no special-cased outputs.

## Worked examples

- Claim: Composing any continuous map `f : β →𝒄 γ` with the continuous identity on `β` on the right yields a map that agrees with `f` pointwise — that is, `VTask.comp f id = f`.

- Claim: Composing the continuous identity on `β` on the left of any continuous map `f : α →𝒄 β` yields a map that agrees with `f` pointwise — that is, `VTask.comp id f = f`.

- Claim: Composition is associative: for continuous maps `h : α →𝒄 β`, `g : β →𝒄 γ`, `f : γ →𝒄 δ`, we have `VTask.comp f (VTask.comp g h) = VTask.comp (VTask.comp f g) h`.

- Claim: For concrete continuous maps, applying `VTask.comp f g` to an element `a : α` gives the same result as first applying `g` to `a` and then applying `f` to the result.

## Boundaries

- The definition is total: it is defined for any two composable continuous maps and always returns a valid continuous homomorphism.
- There are no degenerate or boundary types to worry about: even for trivial ωCPOs (e.g., a single-element type), composition works and is equal to the identity or constant map as expected.
- The order of arguments follows the categorical convention for morphism composition: `VTask.comp f g` applies `g` first and `f` second, mirroring `f ∘ g` in standard mathematical notation.

## Not to be confused with

- `Function.comp` — ordinary function composition without any continuity structure; `VTask.comp` wraps this but also carries the proof of Scott-continuity.
- The `id` continuous homomorphism — the identity morphism in the ωCPO category; `VTask.comp` is the binary composition operation, not the identity.
- `OrderHom.comp` — composition of order-preserving maps (monotone maps) between ordered types, which does not require or guarantee preservation of ω-chain suprema.