## VTask.map

### Object

Given a function `f` between alphabets, `VTask.map f` is the operation that transforms a formal language over alphabet `α` into a formal language over alphabet `β` by applying `f` letter-by-letter to every word in the language. Concretely, a word `w` over `β` belongs to `VTask.map f L` if and only if there exists some word `v` in `L` such that `w` is obtained by replacing each letter `a` in `v` with `f(a)`. This operation is moreover a semiring homomorphism from the language semiring over `α` to the language semiring over `β`, respecting the empty language (zero), the singleton-empty-word language (one), union (addition), and concatenation (multiplication).

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.map : {α : Type u_1} -> {β : Type u_2} -> (f : α → β) -> Language α →+* Language β
<!-- PINNED-SIGNATURE:END -->


`VTask.map : {α : Type u_1} -> {β : Type u_2} -> (f : α → β) -> Language α →+* Language β`

The implicit argument `α` is the source alphabet type; the implicit argument `β` is the target alphabet type. The explicit argument `f` is the letter-to-letter function used to rewrite words. The result is a semiring homomorphism — a structure-preserving map between the two language semirings — so it carries both the underlying set-theoretic function on languages and the proofs that it respects zero, one, addition, and multiplication.

### Conventions

There are no junk-value or edge conventions to declare: `VTask.map` is a total construction defined for every function `f : α → β` and every language `L : Language α`, with no degenerate inputs requiring special treatment beyond the standard algebraic identities (which are provable theorems, not conventions).

### Worked examples

- Claim: Applying `VTask.map` with the identity function to any language yields the same language (i.e., `VTask.map id l = l` for all `l : Language α`).

- Claim: Applying two successive maps composes: `VTask.map g (VTask.map f l) = VTask.map (g ∘ f) l` for all compatible `f`, `g`, and `l`.

- Claim: `VTask.map` commutes with the Kleene star: `VTask.map f (l∗) = (VTask.map f l)∗` for all `f` and `l`.

- Claim: The word `[2]` belongs to `VTask.map (· * 2) {[1]}`, since applying `(· * 2)` letter-by-letter to the word `[1]` yields `[2]`.

- Claim: The empty language maps to the empty language: `VTask.map f ∅ = ∅` for any `f`, reflecting that `VTask.map f` is a semiring homomorphism preserving zero.

### Boundaries

- When `f` is not injective, distinct words in the source language may collapse to the same word in the image; the image language can be strictly smaller (in word variety) than expected.
- When `f` is not surjective, the image language only ever contains words whose letters lie in the range of `f`; letters outside the range never appear.
- The empty language (zero) maps to the empty language, and the one-element language containing only the empty word (one) maps to itself, because applying any `f` letter-by-letter to the empty word yields the empty word.
- For the Kleene star, `VTask.map f (l∗) = (VTask.map f l)∗`, so the star and map operations commute perfectly.
- When `α = β` and `f = id`, the map is the identity on languages.

### Not to be confused with

- `Language.image` (or `Set.image`): the raw set-theoretic image operation, which does not carry the semiring homomorphism structure that `VTask.map` provides.
- Alphabet relabeling on `RegularExpression`: `RegularExpression.map f` renames letters inside a regular expression syntactically; `VTask.map f` acts on the semantic language (the set of accepted words).
- `List.map`: the function that maps `f` over a single word (list); `VTask.map f` lifts this to act on every word in an entire language.