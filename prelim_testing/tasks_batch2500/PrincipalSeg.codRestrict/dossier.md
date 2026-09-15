## Object

Given a principal segment embedding `f : r ≺i s` (an order-embedding from a type `α` with relation `r` into a type `β` with relation `s`, together with a distinguished "top" element such that the image of `f` is exactly the set of elements strictly below the top), `VTask.codRestrict` produces a new principal segment from `r` into the sub-relation of `s` restricted to a chosen subset `p` of `β`. In other words, it confines the codomain of `f` to the subset `p`, provided every element in the image of `f` belongs to `p` and the top element also belongs to `p`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.codRestrict : {α : Type u_1} -> {β : Type u_2} -> {r : α → α → Prop} -> {s : β → β → Prop} -> (p : Set β) -> (f : PrincipalSeg r s) -> (H : ∀ (a : α), f.toRelEmbedding a ∈ p) -> (H₂ : f.top ∈ p) -> PrincipalSeg r (Subrel s fun x => x ∈ p)
<!-- PINNED-SIGNATURE:END -->


`VTask.codRestrict : {α : Type u_1} -> {β : Type u_2} -> {r : α → α → Prop} -> {s : β → β → Prop} -> (p : Set β) -> (f : PrincipalSeg r s) -> (H : ∀ (a : α), f.toRelEmbedding a ∈ p) -> (H₂ : f.top ∈ p) -> PrincipalSeg r (Subrel s fun x => x ∈ p)`

- `p` is the subset of `β` to which the codomain is restricted; the resulting principal segment lands inside the sub-relation of `s` on `p`.
- `f` is the original principal segment embedding from `(α, r)` into `(β, s)`.
- `H` is the proof obligation that every element in the image of `f` (i.e., `f a` for every `a : α`) belongs to `p`.
- `H₂` is the proof obligation that the top element `f.top` of the principal segment also belongs to `p`.

## Conventions

No special junk-value or boundary conventions are declared: the definition is total and well-defined precisely when both membership hypotheses `H` and `H₂` are supplied, so no edge-case conventions arise.

## Worked examples

- Claim: When `VTask.codRestrict p f H H₂` is applied to an element `a : α`, the result is the pair `⟨f a, H a⟩` inside the subtype `{x : β // x ∈ p}`.

- Claim: The top element of the restricted principal segment `VTask.codRestrict p f H H₂` is `⟨f.top, H₂⟩`, i.e., the original top element packaged with its membership proof.

- Claim: If `f : r ≺i s` is a principal segment and `p = Set.univ` (the whole set), then `H` and `H₂` are trivially satisfied, and the resulting principal segment is essentially the same embedding but with codomain `Subrel s (· ∈ Set.univ)`, which is order-isomorphic to `s` itself.

## Boundaries

- If `p` is a proper subset of `β`, the construction is still valid as long as both `H` and `H₂` are supplied; the top element is explicitly required to lie in `p` via `H₂`, since it need not be in the image of `f`.
- The case `p = Set.univ` is valid (all membership proofs are trivial) and yields a principal segment into the full sub-relation on `β`, which is isomorphic to the original `s`.
- The case where `f` is an embedding whose image is a singleton (i.e., `α` has exactly one element) is handled uniformly: both `H` and `H₂` must still be provided separately.

## Not to be confused with

- `RelEmbedding.codRestrict`: restricts the codomain of a plain order-embedding (without a top element), yielding a `RelEmbedding` rather than a `PrincipalSeg`.
- `InitialSeg.codRestrict` (if it exists): a similar restriction for initial segments, which do not carry a top element and have a different universal property.
- `PrincipalSeg.restrict` or domain restriction variants: these restrict the *domain* rather than the codomain, producing a different kind of sub-embedding.