## Object

`VTask.comapDomain f l hf` is the finitely supported function `α →₀ M` obtained by pre-composing the finitely supported function `l : β →₀ M` with the map `f : α → β`. Concretely, it sends each `a : α` to the value `l(f(a))`. The hypothesis `hf` ensures that the support of the result is a genuine finite set (by guaranteeing `f` is injective when restricted to the preimage of `l`'s support), so the construction is well-typed as a `Finsupp`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comapDomain : {α : Type u_1} -> {β : Type u_2} -> {M : Type u_5} -> [Zero M] -> (f : α → β) -> (l : β →₀ M) -> (hf : Set.InjOn f (f ⁻¹' ↑l.support)) -> α →₀ M
<!-- PINNED-SIGNATURE:END -->


`VTask.comapDomain : {α : Type u_1} -> {β : Type u_2} -> {M : Type u_5} -> [Zero M] -> (f : α → β) -> (l : β →₀ M) -> (hf : Set.InjOn f (f ⁻¹' ↑l.support)) -> α →₀ M`

The implicit types `α` and `β` are the domain and codomain types of the pulling-back map; `M` is the value type, which must carry a distinguished zero element (supplied by the `[Zero M]` instance). The argument `f` is the function along which the domain is pulled back. The argument `l` is the finitely supported function being pulled back. The argument `hf` is the injectivity witness: it states that `f` is injective on the preimage of `l`'s support, which is exactly the condition needed so that the preimage of the support stays finite and the resulting function is still finitely supported.

## Conventions

No special junk-value or edge-case conventions are declared for this definition: the output is fully determined by the three inputs for all valid inputs, and outside the domain the definition is not invoked.

## Worked examples

- Claim: For the finitely supported function `l : Fin 3 →₀ ℕ` that sends `0 ↦ 7, 1 ↦ 0, 2 ↦ 3`, and `f : Fin 3 → Fin 3` the identity, `VTask.comapDomain f l hf` agrees with `l` pointwise.

- Claim: If `l : β →₀ M` is the zero finsupp (empty support), then `VTask.comapDomain f l hf` is also the zero finsupp for any `f` and trivially-satisfied `hf`, since `l(f(a)) = 0` for every `a`.

- Claim: Given `f : Fin 2 → Fin 4` mapping `0 ↦ 1` and `1 ↦ 3`, and `l : Fin 4 →₀ ℕ` with `l 1 = 5` and `l 3 = 9` (all other values 0), the result `VTask.comapDomain f l hf` satisfies `(VTask.comapDomain f l hf) 0 = 5` and `(VTask.comapDomain f l hf) 1 = 9`.

- Claim: The support of `VTask.comapDomain f l hf` equals the preimage of `l.support` under `f` (as a `Finset`), so an element `a : α` lies in the support of the result precisely when `f a` lies in the support of `l`.

## Boundaries

- **Empty support**: If `l.support = ∅` (i.e., `l` is the zero function), the injectivity hypothesis `hf` is vacuously satisfied for any `f`, and `VTask.comapDomain f l hf` is the zero function on `α` with empty support.
- **Non-injective `f` away from the preimage**: `f` need not be globally injective — only injective on `f ⁻¹' l.support`. Collisions of `f` outside that set are irrelevant, since those points map to zero anyway.
- **Surjectivity is irrelevant**: Elements of `β` not in the image of `f` are simply not represented; their values in `l` do not appear in the result.
- **Values at non-support points**: For any `a` with `f a ∉ l.support`, we have `(VTask.comapDomain f l hf) a = 0` because `l(f(a)) = 0` by definition of `Finsupp`.

## Not to be confused with

- `Finsupp.mapDomain`: pushes a finsupp *forward* along `f : α → β` (summing values that collide), rather than pulling it back.
- `Finsupp.comap`: a related notion in certain algebraic settings that may conflate the injectivity hypothesis or work in a different category.
- Ordinary function composition `l ∘ f`: this is the underlying `toFun`, but `VTask.comapDomain` packages it as a `Finsupp`, with finiteness of support made explicit and verified.