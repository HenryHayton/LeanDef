## Object

The **alternating product** of a list `[g₀, g₁, g₂, g₃, …]` over a group-like structure is the product obtained by multiplying the elements at even positions and dividing by (inverting) the elements at odd positions. Formally, if the list has elements at indices 0, 1, 2, …, the result is

  g₀ · g₁⁻¹ · g₂ · g₃⁻¹ · …

processed in pairs from left to right, with the convention that the empty list yields the identity element and a singleton list yields its unique element unchanged.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.alternatingProd : {G : Type u_4} -> [One G] -> [Mul G] -> [Inv G] -> List G → G
<!-- PINNED-SIGNATURE:END -->


`VTask.alternatingProd : {G : Type u_4} -> [One G] -> [Mul G] -> [Inv G] -> List G → G`

- `G` is the type of the group elements; it is inferred from context.
- `[One G]` provides the identity element `1`, used as the value for the empty list.
- `[Mul G]` provides the binary multiplication `·`.
- `[Inv G]` provides the inversion operation `⁻¹`, used on odd-indexed elements.
- The final argument is the `List G` whose alternating product is to be computed.

## Conventions

The alternating product of the empty list is `1` (the identity provided by `[One G]`). The alternating product of a singleton list `[g]` is `g` itself, with no inversion applied.

## Worked examples

- Claim: The alternating product of `[]` (in any group) is `1`.

- Claim: The alternating product of `[g]` for any `g : G` is `g`.

- Claim: The alternating product of `[a, b]` is `a * b⁻¹`.

- Claim: For a list `[a, b, c]`, `VTask.alternatingProd [a, b, c] = a * b⁻¹ * c` (since the third element is at an even index and appears without inversion).

- Claim: For a list `[a, b, c, d]`, `VTask.alternatingProd [a, b, c, d] = a * b⁻¹ * (c * d⁻¹)` because the list is processed in consecutive pairs.

- Claim: In a commutative division monoid, `VTask.alternatingProd L = ∏ i : Fin L.length, L[i] ^ ((-1 : ℤ) ^ (i : ℕ))`, expressing each element raised to `+1` or `−1` depending on parity of its index.

## Boundaries

- **Empty list**: Returns `1`. No elements to multiply, so the identity is the natural answer.
- **Singleton list `[g]`**: Returns `g` unchanged. There is no second element to invert against.
- **Two-element list `[g, h]`**: Returns `g * h⁻¹`.
- **Odd-length lists**: The last element always appears at an even index (0-based) and is therefore contributed positively (without inversion).
- **Even-length lists**: The last element is at an odd index and appears inverted in the product.
- **Appending two lists**: `alternatingProd (l₁ ++ l₂) = alternatingProd l₁ * alternatingProd l₂ ^ ((-1 : ℤ) ^ length l₁)`, so the sign with which the second half contributes depends on the parity of the first list's length.
- **Reversal**: `alternatingProd (reverse l) = alternatingProd l ^ ((-1 : ℤ) ^ (length l + 1))`.

## Not to be confused with

- **`List.prod`**: The ordinary (non-alternating) product of all elements, where every element is multiplied in without inversion.
- **`Finset.prod` / `∏`**: A big-operator product over a finite set or a `Finset`, not a list-structured recursion; does not inherently alternate signs.
- **`List.alternatingSum`**: The additive analogue (for additive groups), computing `a₀ - a₁ + a₂ - …`; structurally identical but written with `+`/`-` rather than `*`/`⁻¹`.