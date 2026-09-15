## VTask.toRegular

### Object

`VTask.toRegular` is the **regularization map** on a Heyting algebra: given an element `a`, it produces the smallest regular element of the algebra that is greater than or equal to `a`. Regular elements of a Heyting algebra are those satisfying `aᶜᶜ = a` (i.e., elements equal to their own double complement). The regularization of `a` is exactly `aᶜᶜ`, packaged as a member of the type `Heyting.Regular α` of regular elements. The map is presented as an order morphism (monotone map) from `α` to `Heyting.Regular α`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toRegular : {α : Type u_1} -> [HeytingAlgebra α] -> α →o Heyting.Regular α
<!-- PINNED-SIGNATURE:END -->


`VTask.toRegular : {α : Type u_1} -> [HeytingAlgebra α] -> α →o Heyting.Regular α`

The implicit type argument `α` is the carrier type of the Heyting algebra. The instance argument supplies the Heyting algebra structure on `α`. The map itself takes an element of `α` and returns the smallest regular element above it, as an element of `Heyting.Regular α`; by packaging it as `α →o Heyting.Regular α`, the map is asserted to be monotone (order-preserving).

### Conventions

The coercion of `VTask.toRegular a` back to `α` equals the double complement `aᶜᶜ`. There are no junk-value conventions: the map is total on any Heyting algebra, and every element has a well-defined regularization.

### Worked examples

- Claim: For any element `a` in a Heyting algebra `α`, the underlying element of `VTask.toRegular a` in `α` is `aᶜᶜ`.

- Claim: Applying `VTask.toRegular` to a regular element `r : Heyting.Regular α` (viewed as an element of `α`) returns `r` itself — regularization is idempotent on regular elements.

- Claim: The map `VTask.toRegular` is monotone: if `a ≤ b` in a Heyting algebra, then `VTask.toRegular a ≤ VTask.toRegular b` in `Heyting.Regular α`.

- Claim: `VTask.toRegular a` is always a regular element, i.e., its double complement equals itself — equivalently, `(aᶜᶜ)ᶜᶜ = aᶜᶜ` in any Heyting algebra.

### Boundaries

- The map is defined for **all** elements of any Heyting algebra; there are no excluded inputs.
- When `a` is itself regular (i.e., `aᶜᶜ = a`), `VTask.toRegular a` equals `a` as an element of `Heyting.Regular α`.
- For the bottom element `⊥`, the regularization `⊥ᶜᶜ` equals `⊥` in any Heyting algebra, so `VTask.toRegular ⊥ = ⊥`.
- For the top element `⊤`, `⊤ᶜᶜ = ⊤`, so `VTask.toRegular ⊤ = ⊤`.
- Regularization is not in general a Heyting algebra morphism — it preserves order but need not preserve `⊓`, `⊔`, or `⇒`.

### Not to be confused with

- `Heyting.Regular α` — the **subtype** of regular elements, not the regularization map itself.
- The double-complement map `compl ∘ compl : α → α` — `VTask.toRegular` computes the same value but targets the subtype `Heyting.Regular α` rather than `α`.
- A closure operator on the full lattice `α` — while regularization is a closure operator when viewed as a map `α → α`, `VTask.toRegular` lands in the subtype and is presented as a monotone map, not a lattice endomorphism.