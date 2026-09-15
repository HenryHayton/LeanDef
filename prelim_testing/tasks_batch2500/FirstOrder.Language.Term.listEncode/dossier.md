## Object

`VTask.listEncode` converts a first-order term (built from variables and function applications) into a flat list whose elements are either variables (tagged with `Sum.inl`) or function symbols (tagged with `Sum.inr`, paired with their arity). The list is a linear, left-to-right serialisation of the term's tree: function symbols appear before the encodings of their arguments, and variables appear as single-element sublists. This encoding is intended to be injective, so that distinct terms produce distinct lists.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.listEncode : {L : FirstOrder.Language} -> {α : Type u'} -> L.Term α → List (α ⊕ (i : ℕ) × L.Functions i)
<!-- PINNED-SIGNATURE:END -->


`VTask.listEncode : {L : FirstOrder.Language} -> {α : Type u'} -> L.Term α → List (α ⊕ (i : ℕ) × L.Functions i)`

The implicit argument `L` is the first-order language, which fixes what function symbols and their arities are available. The implicit argument `α` is the type of variable names used in the term. The explicit argument is the term to be encoded; it is a `L.Term α`, built from variables drawn from `α` and function symbols of `L`.

## Conventions

There are no junk-value or out-of-domain conventions to declare: `VTask.listEncode` is a total function defined on all first-order terms without restriction.

## Worked examples

- Claim: For a variable term `var x`, `VTask.listEncode (var x)` is the singleton list `[Sum.inl x]`.

- Claim: For a constant (0-ary function) `c` with no arguments, `VTask.listEncode (func c Fin.elim0)` begins with `Sum.inr ⟨0, c⟩` and is followed by no further elements, yielding `[Sum.inr ⟨0, c⟩]`.

- Claim: For a unary function symbol `f` applied to a variable `x`, `VTask.listEncode (func f (fun _ => var x))` is `[Sum.inr ⟨1, f⟩, Sum.inl x]` — the function symbol first, then the encoding of its single argument.

- Claim: For a binary function symbol `g` applied to variables `x` and `y` (in argument order), `VTask.listEncode (func g ![var x, var y])` equals `[Sum.inr ⟨2, g⟩, Sum.inl x, Sum.inl y]`.

## Boundaries

- A variable `var x` encodes to exactly a one-element list `[Sum.inl x]`.
- A 0-ary (constant) function symbol `c` encodes to exactly a one-element list `[Sum.inr ⟨0, c⟩]`, since there are no arguments to append.
- The length of the list grows with the size (number of nodes) of the term tree: each variable contributes one element, each function application contributes one element (for the symbol) plus the recursive encodings of all its arguments.
- The `Sum.inr` entries carry the arity of the function symbol as part of the pair, so the same function name at different arities produces distinct list elements.
- The encoding is prefix-free in the sense used by injectivity: the list uniquely determines the term.

## Not to be confused with

- `FirstOrder.Language.Term.toString` or similar pretty-printing: `VTask.listEncode` is a mathematical serialisation into a typed list, not a human-readable string.
- The *set* of subterms of a term: `VTask.listEncode` produces a flat ordered list with repetitions determined by the recursive structure, not the collection of distinct subterms.
- `Encodable`/`Encodable.encode` (natural-number Gödel numbering): `VTask.listEncode` maps to a list of typed tokens, not a single natural number.