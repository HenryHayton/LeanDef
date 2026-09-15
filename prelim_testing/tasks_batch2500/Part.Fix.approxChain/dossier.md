## Object

`VTask.approxChain f` is the ascending chain of successive approximations used to compute the least fixed point of a monotone endofunction `f` on the type of dependent partial functions `(a : α) → Part (β a)`. Concretely, it packages the sequence `approx f 0, approx f 1, approx f 2, …` — where `approx f n` is obtained by applying `f` exactly `n` times to the bottom element — together with the proof that this sequence is monotone (each term is below the next in the pointwise ordering), yielding an object of type `OmegaCompletePartialOrder.Chain`. The supremum of this chain is precisely `fix f`, the least fixed point of `f`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.approxChain : {α : Type u_1} -> {β : α → Type u_2} -> (f : ((a : α) → Part (β a)) →o (a : α) → Part (β a)) -> OmegaCompletePartialOrder.Chain ((a : α) → Part (β a))
<!-- PINNED-SIGNATURE:END -->


`VTask.approxChain : {α : Type u_1} -> {β : α → Type u_2} -> (f : ((a : α) → Part (β a)) →o (a : α) → Part (β a)) -> OmegaCompletePartialOrder.Chain ((a : α) → Part (β a))`

The implicit argument `α` is the index type over which the dependent partial functions are defined. The implicit argument `β` is the type family giving the return type of the partial functions at each index. The explicit argument `f` is the monotone endofunction whose least fixed point is being approximated; it is supplied as an order-homomorphism (bundling the function with its monotonicity proof) from the omega-CPO of dependent partial functions to itself.

## Conventions

There are no junk-value or edge-case conventions for this definition: the construction is total and well-defined for any monotone `f`, and the sequence is always infinite (indexed by all natural numbers), so no boundary or default value needs to be declared.

## Worked examples

- Claim: The `n`-th element of `VTask.approxChain f` equals `approx f n` for every `n : ℕ`.

- Claim: `VTask.approxChain f` is an instance of `OmegaCompletePartialOrder.Chain ((a : α) → Part (β a))`, so in particular its underlying function `(VTask.approxChain f).toFun` is monotone.

- Claim: For the identity monotone function `id_mono : ((a : α) → Part (β a)) →o (a : α) → Part (β a)` (the identity map), the 0-th element of `VTask.approxChain id_mono` is the bottom element (the everywhere-`Part.none` function).

- Claim: For any monotone `f`, `(VTask.approxChain f) 0` is the bottom element of the omega-CPO, i.e., the function sending every `a` to `Part.none`.

## Boundaries

- At index `n = 0`, the chain element is the bottom element of the omega-CPO — the dependent partial function that is undefined everywhere.
- At index `n = 1`, the chain element is `f ⊥`, the single application of `f` to the bottom element.
- The chain is infinite; there is no maximum index. The least upper bound (supremum) over all indices is `fix f`.
- The chain is non-strictly ascending in general: if `f` reaches its fixed point at some finite stage, later elements may be equal to earlier ones rather than strictly larger.

## Not to be confused with

- `approx f n` — the individual `n`-th approximation as a bare dependent partial function, without the chain structure or monotonicity bundling.
- `OmegaCompletePartialOrder.Chain` (the type itself) — the general notion of an ω-chain in any omega-CPO; `VTask.approxChain f` is a specific instance of this type built from the iteration of `f`.
- `fix f` — the least fixed point, which is the supremum of `VTask.approxChain f`, not the chain itself.