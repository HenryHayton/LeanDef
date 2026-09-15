## VTask.prodLift

### Object

`VTask.prodLift f g` is the **product lifting** of two partial functions sharing a common domain type. Given partial functions `f : α →. β` and `g : α →. γ`, it produces a new partial function `α →. β × γ` that, on any input `x`, is defined precisely when **both** `f x` and `g x` are defined, and whose output is the ordered pair `(f x, g x)`. In other words, it is the unique partial function whose graph is the set of triples `(x, (b, c))` such that `b ∈ f x` and `c ∈ g x`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prodLift : {α : Type u_1} -> {β : Type u_2} -> {γ : Type u_3} -> (f : α →. β) -> (g : α →. γ) -> α →. β × γ
<!-- PINNED-SIGNATURE:END -->


`VTask.prodLift : {α : Type u_1} -> {β : Type u_2} -> {γ : Type u_3} -> (f : α →. β) -> (g : α →. γ) -> α →. β × γ`

The three type parameters `α`, `β`, and `γ` are the shared input type, the output type of the first partial function, and the output type of the second partial function, respectively; all are inferred implicitly. The argument `f` is the first partial function, contributing the left component of each output pair. The argument `g` is the second partial function, contributing the right component of each output pair.

### Conventions

There are no special junk-value or out-of-domain conventions: `VTask.prodLift` is a total function on its arguments (it accepts any two partial functions) and the notion of "undefined" is already encoded in the partiality of the result — the resulting partial function is simply undefined at any input where either `f` or `g` is undefined.

### Worked examples

- Claim: For the partial functions `f = PFun.lift (· + 1)` and `g = PFun.lift (· * 2)` on natural numbers, the pair `(3, 4)` is a member of `(VTask.prodLift f g) 2` because `f 2 = 3` and `g 2 = 4`.

- Claim: The domain of `VTask.prodLift f g` at a point `x` is the conjunction of the domain of `f` at `x` and the domain of `g` at `x`; formally, `(VTask.prodLift f g).Dom = { x | (f x).Dom ∧ (g x).Dom }`.

- Claim: If `f` is a total function (i.e., `f x` is always defined) but `g x` is undefined at some `x₀`, then `VTask.prodLift f g` is undefined at `x₀`.

- Claim: For partial functions `f : α →. γ` and `g : β →. δ`, lifting `f ∘ Prod.fst` and `g ∘ Prod.snd` via `VTask.prodLift` recovers the product map `prodMap f g`.

### Boundaries

- If either `f` or `g` is the empty partial function (defined nowhere), then `VTask.prodLift f g` is also defined nowhere.
- If both `f` and `g` are total (defined everywhere), then `VTask.prodLift f g` is also total, and equals the ordinary pairing `fun x => (f x, g x)` viewed as a partial function.
- If `f` is defined at `x` but `g` is not, the result is undefined at `x`, even though one component could be computed; the definition strictly requires both to be defined.
- The output pair `(b, c) ∈ VTask.prodLift f g x` if and only if `b ∈ f x` and `c ∈ g x` — there is no interaction between the two components beyond requiring both to be present.

### Not to be confused with

- `PFun.prodMap f g` — takes two partial functions with **different** input types `α →. γ` and `β →. δ` and produces `α × β →. γ × δ`, applying each to a separate component of an input pair, rather than applying both to the same input.
- `PFun.comp f g` — sequential composition of two partial functions, not pairing of two functions on a shared input.
- The ordinary (total) pairing `Prod.mk ∘ f` — applies only to total functions and does not account for the combined definedness condition required here.