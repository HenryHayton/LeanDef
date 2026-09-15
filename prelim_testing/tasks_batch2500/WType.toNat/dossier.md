## VTask.toNat

### Object

A canonical bijection (isomorphism of types) from the W-type encoding of the natural numbers to the ordinary natural number type `ℕ`. The W-type in question, `WType WType.Natβ`, is the initial algebra for the signature of the natural numbers (one nullary constructor for zero, one unary constructor for successor), and `VTask.toNat` converts each element of this abstract tree-based representation into its concrete `ℕ` counterpart.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toNat : WType WType.Natβ → ℕ
<!-- PINNED-SIGNATURE:END -->


`VTask.toNat : WType WType.Natβ → ℕ`

The sole argument is an element of the W-type built from the natural-number signature `WType.Natβ`, i.e., a well-founded tree whose branching type encodes either a zero node (no children) or a successor node (one child). The function returns the natural number that this tree represents.

### Conventions

There are no junk-value or out-of-domain conventions to declare: the function is defined by structural recursion and is total on all elements of `WType WType.Natβ`; every such element maps to a unique natural number.

### Worked examples

- Claim: The W-type node for zero (constructed with the zero label and an empty family of children) maps to `0`.

- Claim: Applying `VTask.toNat` to the W-type node for successor applied once to the zero node yields `1`.

- Claim: `VTask.toNat` is a bijection; in particular, applying it to the double-successor of zero gives `2`.

### Boundaries

- The function is total: every element of `WType WType.Natβ` has a unique preimage in `ℕ` and a unique image under `VTask.toNat`.
- The zero node maps to `0` with no recursive calls needed.
- Each successor node peels off one layer, recursively converts its unique child, and increments by one, so the recursion terminates because W-types are well-founded.
- There are no elements of `WType WType.Natβ` that fall outside the image of this function; the map is surjective onto all of `ℕ`.

### Not to be confused with

- `WType.Natβ` itself — that is the branching-arity function defining the signature, not the conversion map.
- The inverse direction (the map `ℕ → WType WType.Natβ`) — `VTask.toNat` goes from W-type to `ℕ`, not the other way around.
- Generic W-type recursors — `VTask.toNat` is a specific semantic map to `ℕ`, not the general eliminator for arbitrary W-types.
