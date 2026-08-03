## 1. Object

`VTask.sumLexLift` combines four two-argument `Finset`-valued functions into a single function on sum types. Given functions that operate on the four possible combinations of left/right inputs, it produces a unified function `α₁ ⊕ α₂ → β₁ ⊕ β₂ → Finset (γ₁ ⊕ γ₂)` whose output respects the lexicographic structure of the sum type. The result on each pair of tagged inputs is computed from the appropriate component function, with outputs tagged accordingly. The name reflects its intended use in constructing intervals in a lexicographic sum order.

## 2. Signature

```
VTask.sumLexLift : {α₁ : Type u_1} -> {α₂ : Type u_2} -> {β₁ : Type u_3} -> {β₂ : Type u_4} -> {γ₁ : Type u_5} -> {γ₂ : Type u_6} -> (f₁ : α₁ → β₁ → Finset γ₁) -> (f₂ : α₂ → β₂ → Finset γ₂) -> (g₁ : α₁ → β₂ → Finset γ₁) -> (g₂ : α₁ → β₂ → Finset γ₂) -> α₁ ⊕ α₂ → β₁ ⊕ β₂ → Finset (γ₁ ⊕ γ₂)
```

- `f₁ : α₁ → β₁ → Finset γ₁` — the function applied when both inputs are `inl` (both from the left summands); its outputs are tagged with `inl`.
- `f₂ : α₂ → β₂ → Finset γ₂` — the function applied when both inputs are `inr` (both from the right summands); its outputs are tagged with `inr`.
- `g₁ : α₁ → β₂ → Finset γ₁` — the function providing `γ₁`-elements when the first input is `inl` and the second is `inr`; outputs tagged `inl`.
- `g₂ : α₁ → β₂ → Finset γ₂` — the function providing `γ₂`-elements when the first input is `inl` and the second is `inr`; outputs tagged `inr`.
- `α₁ ⊕ α₂` — the tagged first argument.
- `β₁ ⊕ β₂` — the tagged second argument.
- Returns a `Finset (γ₁ ⊕ γ₂)` whose elements are tagged output values assembled from the appropriate component function.

## 3. Conventions

When the first argument is `inr` and the second is `inl` (a "right-then-left" combination, which has no natural component function and is empty in lexicographic order), the result is the empty finset regardless of the component functions provided.

## 4. Worked Examples

- Claim: `VTask.sumLexLift f₁ f₂ g₁ g₂ (inl a) (inl b)` equals the image of `f₁ a b` under the `inl` embedding into `γ₁ ⊕ γ₂`. Every element `c₁ ∈ f₁ a b` appears as `inl c₁` in the result, and all result elements are of the form `inl c₁`.

- Claim: `VTask.sumLexLift f₁ f₂ g₁ g₂ (inr a) (inl b)` is the empty finset for any `a`, `b`, and any choice of component functions. This reflects the lexicographic convention that a right-tagged first element cannot precede a left-tagged second element.

- Claim: `VTask.sumLexLift f₁ f₂ g₁ g₂ (inl a) (inr b)` equals the disjoint sum of `g₁ a b` and `g₂ a b`, i.e., all elements of `g₁ a b` tagged with `inl` followed by all elements of `g₂ a b` tagged with `inr`.

- Claim: `VTask.sumLexLift f₁ f₂ g₁ g₂ (inr a) (inr b)` equals the image of `f₂ a b` under the `inr` embedding into `γ₁ ⊕ γ₂`. Every element `c₂ ∈ f₂ a b` appears as `inr c₂` in the result.

## 5. Boundaries

- **`inr`-then-`inl` always gives `∅`**: When the first argument is `inr a` and the second is `inl b`, the result is always empty, no matter what `f₁`, `f₂`, `g₁`, `g₂` are. This is not a degenerate case — it is the intended behavior for lexicographic order.
- **Empty component functions**: If any component function returns `∅` on given inputs, the corresponding branch also returns `∅`. The `inl a, inr b` branch returns `∅` precisely when both `g₁ a b` and `g₂ a b` are empty.
- **Monotonicity**: If each component function is pointwise a subset of the corresponding primed function, then `VTask.sumLexLift f₁ f₂ g₁ g₂ a b ⊆ VTask.sumLexLift f₁' f₂' g₁' g₂' a b` for all tagged inputs.

## 6. Not to be confused with

- `Finset.disjSum`: Takes two finsets `s : Finset α` and `t : Finset β` and forms a finset in `α ⊕ β`; it does not involve functions on sum types and has no casework on input tags.
- `Sum.Lex`: The lexicographic order on a sum type, which is the order that `VTask.sumLexLift` is designed to serve (computing intervals in it), but is itself a relation, not a function producing finsets.
- `Finset.sumLift₂` (if it existed): A hypothetical simpler lift using only two functions `f₁`, `f₂` on matching summands; `VTask.sumLexLift` is strictly more general, adding the two cross-term functions `g₁`, `g₂` for the mixed `inl`/`inr` case.
