## Object

Given two first-order languages `L` and `L₁`, their **sum language** `L.sum L₁` is the language whose function symbols and relation symbols at each arity are the disjoint union (via `Sum`) of those of `L` and `L₁`. `VTask.sumMap` takes two language homomorphisms — one from `L` to `L'` and one from `L₁` to `L₂` — and produces a language homomorphism from `L.sum L₁` to `L'.sum L₂` by acting componentwise: symbols originating in `L` are translated by the first map and symbols originating in `L₁` are translated by the second map.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sumMap : {L : FirstOrder.Language} -> {L' : FirstOrder.Language} -> (ϕ : L →ᴸ L') -> {L₁ : FirstOrder.Language} -> {L₂ : FirstOrder.Language} -> (ψ : L₁ →ᴸ L₂) -> L.sum L₁ →ᴸ L'.sum L₂
<!-- PINNED-SIGNATURE:END -->


`VTask.sumMap : {L : FirstOrder.Language} -> {L' : FirstOrder.Language} -> (ϕ : L →ᴸ L') -> {L₁ : FirstOrder.Language} -> {L₂ : FirstOrder.Language} -> (ψ : L₁ →ᴸ L₂) -> L.sum L₁ →ᴸ L'.sum L₂`

The implicit arguments `L`, `L'`, `L₁`, `L₂` are the four first-order languages involved. The explicit argument `ϕ` is a language homomorphism from `L` to `L'`, governing how symbols that come from the left factor are translated. The explicit argument `ψ` is a language homomorphism from `L₁` to `L₂`, governing how symbols that come from the right factor are translated.

## Conventions

No special junk-value or edge-case conventions are declared for this definition: it is a total construction over the given inputs with no degenerate regime requiring a conventional choice.

## Worked examples

- Claim: For any `ϕ : L →ᴸ L'` and `ψ : L₁ →ᴸ L₂`, applying `VTask.sumMap ϕ ψ` to a function symbol `Sum.inl f` at arity `n` yields `Sum.inl (ϕ.onFunction f)`. That is, left-factor function symbols are mapped exclusively through `ϕ`.

- Claim: For any `ϕ : L →ᴸ L'` and `ψ : L₁ →ᴸ L₂`, applying `VTask.sumMap ϕ ψ` to a relation symbol `Sum.inr r` at arity `n` yields `Sum.inr (ψ.onRelation r)`. That is, right-factor relation symbols are mapped exclusively through `ψ`.

- Claim: When `ϕ` and `ψ` are both the identity language homomorphism on their respective languages, `VTask.sumMap ϕ ψ` acts as the identity on `L.sum L₁`: every symbol is sent to itself.

- Claim: `VTask.sumMap` is compatible with composition: for composable pairs `ϕ₁ : L →ᴸ L'`, `ϕ₂ : L' →ᴸ L''` and `ψ₁ : L₁ →ᴸ L₂`, `ψ₂ : L₂ →ᴸ L₃`, the composite `(VTask.sumMap ϕ₂ ψ₂).comp (VTask.sumMap ϕ₁ ψ₁)` and `VTask.sumMap (ϕ₂.comp ϕ₁) (ψ₂.comp ψ₁)` agree on all symbols.

## Boundaries

- If either component language has **no function symbols** at some arity, the homomorphism on that component is vacuously well-defined; `VTask.sumMap` handles this without issue.
- If either component language has **no relation symbols**, the same applies for the relation component.
- The construction is entirely symmetric in the roles of functions and relations: each is handled by the respective `onFunction`/`onRelation` fields of the input homomorphisms.
- `VTask.sumMap` is defined for any pair of language homomorphisms, including degenerate cases where either language is the empty language (no symbols at any arity).

## Not to be confused with

- `FirstOrder.Language.sum` (the binary sum operation on languages itself, not a map between sum languages).
- A language homomorphism `L →ᴸ L₁.sum L₂` that injects a single language into a sum (the "inclusion" maps `sumInl` and `sumInr`), which only involve one factor, not two independent maps.
- A product or direct-sum construction on language homomorphisms that might combine two maps into a single target language, rather than mapping between two separate sum languages componentwise.