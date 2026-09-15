## VTask.sumElim

### Object

Given two first-order language homomorphisms `ϕ : L →ᴸ L'` and `ψ : L'' →ᴸ L'` that both target the same language `L'`, `VTask.sumElim ϕ ψ` is the unique language homomorphism from the coproduct (sum) language `L.sum L''` into `L'` induced by the universal property of the sum. Concretely, it sends every function or relation symbol that comes from the `L`-factor of `L.sum L''` through `ϕ`, and every symbol that comes from the `L''`-factor through `ψ`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sumElim : {L : FirstOrder.Language} -> {L' : FirstOrder.Language} -> (ϕ : L →ᴸ L') -> {L'' : FirstOrder.Language} -> (ψ : L'' →ᴸ L') -> L.sum L'' →ᴸ L'
<!-- PINNED-SIGNATURE:END -->


`{L : FirstOrder.Language} -> {L' : FirstOrder.Language} -> (ϕ : L →ᴸ L') -> {L'' : FirstOrder.Language} -> (ψ : L'' →ᴸ L') -> L.sum L'' →ᴸ L'`

The implicit argument `L` is the first component language of the sum. The implicit argument `L'` is the common target language. The explicit argument `ϕ` is the language homomorphism from `L` into `L'`. The implicit argument `L''` is the second component language of the sum. The explicit argument `ψ` is the language homomorphism from `L''` into `L'`. The result is a language homomorphism from the sum language `L.sum L''` into `L'`.

### Conventions

No junk-value or boundary conventions are declared for this definition: it is a total construction on all language homomorphisms and all arities, with no degenerate inputs that require special casing.

### Worked examples

- Claim: For any `ϕ : L →ᴸ L'` and `ψ : L'' →ᴸ L'`, applying `VTask.sumElim ϕ ψ` to a function symbol coming from the left (L) factor of `L.sum L''` at arity `n` yields the same result as applying `ϕ.onFunction` to that symbol.

- Claim: For any `ϕ : L →ᴸ L'` and `ψ : L'' →ᴸ L'`, applying `VTask.sumElim ϕ ψ` to a relation symbol coming from the right (L'') factor of `L.sum L''` at arity `n` yields the same result as applying `ψ.onRelation` to that symbol.

- Claim: For any `ϕ : L →ᴸ L'` and `ψ : L'' →ᴸ L'`, the restriction of `VTask.sumElim ϕ ψ` to function symbols at every arity acts as a case-split: left-injected symbols are handled by `ϕ` and right-injected symbols are handled by `ψ`.

### Boundaries

- When `L` is the empty language (no function or relation symbols), the map `VTask.sumElim ϕ ψ` acts entirely through `ψ`, since all symbols in `L.sum L''` come from `L''`.
- Symmetrically, when `L''` is the empty language, the map acts entirely through `ϕ`.
- The construction is defined for every arity `n : ℕ` simultaneously; there is no restriction to any particular arity.
- If both `ϕ` and `ψ` are the identity map on `L'` (when `L = L'' = L'`), then `VTask.sumElim ϕ ψ` witnesses that the sum `L'.sum L'` maps into `L'` by folding.

### Not to be confused with

- `FirstOrder.Language.LHom.sumInl` / `sumInr`: these are the canonical *inclusions* of `L` or `L''` *into* `L.sum L''`, going in the opposite direction from `VTask.sumElim`.
- `FirstOrder.Language.sum`: the coproduct language itself (the domain of `VTask.sumElim`), not a map.
- `Sum.elim` (for types): the term-level eliminator on `Sum α β`; `VTask.sumElim` is its analogue lifted to the level of language homomorphisms.