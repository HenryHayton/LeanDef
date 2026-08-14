## Object

`VTask.copy` produces an order homomorphism (a monotone map between preordered types) that is definitionally equal to a given bare function `f'`, while being provably equal to an existing order homomorphism `f`. Its purpose is to replace the underlying function of an order homomorphism with a definitionally equal variant, which can resolve issues where two expressions are propositionally but not definitionally equal in Lean's type theory.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {α : Type u_2} -> {β : Type u_3} -> [Preorder α] -> [Preorder β] -> (f : α →o β) -> (f' : α → β) -> (h : f' = ⇑f) -> α →o β
<!-- PINNED-SIGNATURE:END -->


`VTask.copy : {α : Type u_2} -> {β : Type u_3} -> [Preorder α] -> [Preorder β] -> (f : α →o β) -> (f' : α → β) -> (h : f' = ⇑f) -> α →o β`

The implicit type arguments `α` and `β` are the domain and codomain types, each equipped with a `Preorder` instance supplied by the corresponding implicit typeclass arguments. The argument `f` is the existing order homomorphism whose monotonicity proof is to be reused. The argument `f'` is the new bare function that will serve as the underlying function of the result; it must be definitionally a function `α → β` (not an order homomorphism). The argument `h` is a proof that `f'` is propositionally equal to the coercion of `f` to a plain function; this equality is used to transfer the monotonicity of `f` to `f'`.

## Conventions

There are no junk-value or out-of-domain edge conventions for this definition: it is total and well-typed whenever the arguments are provided, and it carries no implicit defaulting behavior.

## Worked examples

- Claim: The coercion of `VTask.copy f f' h` to a plain function equals `f'`. That is, `⇑(VTask.copy f f' h) = f'`.

- Claim: The result of `VTask.copy f f' h` is equal (as an order homomorphism) to the original `f`. That is, `VTask.copy f f' h = f`.

- Claim: For the identity order homomorphism `id_hom : ℕ →o ℕ` with underlying function `id`, copying it with `f' = id` and `h : id = ⇑id_hom` yields an order homomorphism whose coercion is `id`.

## Boundaries

- The proof `h` must go in the direction `f' = ⇑f` (not `⇑f = f'`); the symmetry is handled internally.
- If `f'` is already definitionally equal to `⇑f` (not just propositionally), `VTask.copy` is still applicable and simply produces a copy of `f` with `f'` as its recorded underlying function.
- There is no restriction on the preorders on `α` or `β`; they need not be partial orders or linear orders.
- The result order homomorphism is propositionally equal to `f` (by `copy_eq`) and has `f'` as its coercion (by `coe_copy`), but `f'` and `⇑f` may differ definitionally.

## Not to be confused with

- `OrderHom.mk` / `⟨f', hf'⟩`: the direct constructor for order homomorphisms, which requires supplying a fresh monotonicity proof for `f'` rather than inheriting it from an existing homomorphism via an equality.
- `Function.Injective` or coercion lemmas about order homomorphisms: these describe properties of `⇑f`, not a mechanism for replacing the underlying function.
- `OrderIso.copy`: an analogous utility for order isomorphisms, which additionally requires replacing the inverse function.