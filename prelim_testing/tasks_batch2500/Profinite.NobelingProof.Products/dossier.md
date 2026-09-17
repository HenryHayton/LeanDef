## VTask.Products

### Object

`VTask.Products I` is the type of strictly decreasing finite lists of elements of a linearly ordered type `I`. A typical element is a list `[i₁, i₂, …, iᵣ]` satisfying `i₁ > i₂ > … > iᵣ`. This includes the empty list as a degenerate case. The type is ordered lexicographically: the empty list is smaller than every non-empty list, and two non-empty lists are compared first by their head elements and then, if those are equal, recursively by their tails. Elements of this type are intended to represent monomials — products of basis functions indexed by the entries of the list.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Products : (I : Type u_1) -> [LinearOrder I] -> Type u_1
<!-- PINNED-SIGNATURE:END -->


`VTask.Products : (I : Type u_1) -> [LinearOrder I] -> Type u_1`

The first argument `I` is the linearly ordered index type whose elements serve as the entries of the decreasing lists. The instance argument `[LinearOrder I]` supplies the linear order on `I` that gives meaning to the strict decrease condition and to the lexicographic ordering on lists.

### Conventions

The empty list `[]` is a valid element of `VTask.Products I` for any `I`; it represents the empty product (the multiplicative identity). There are no junk values because every term of the type is by construction a proof-carrying pair: the underlying list together with evidence that it is strictly decreasing.

### Worked examples

- Claim: For `I = Fin 4`, the list `[3, 1, 0]` (with `3 > 1 > 0`) is a valid element of `VTask.Products (Fin 4)`.

- Claim: For `I = Fin 4`, the list `[2, 2]` is NOT a valid element of `VTask.Products (Fin 4)` because it fails the strict decrease condition (`2 > 2` is false).

- Claim: For `I = Fin 3`, the element `⟨[2, 0], _⟩` is strictly less than `⟨[2, 1], _⟩` in the lexicographic order on `VTask.Products (Fin 3)`, because the heads are equal (`2 = 2`) and the tail `[0]` precedes `[1]` since `0 < 1`.

- Claim: The empty list element of `VTask.Products (Fin 5)` is less than every non-empty element, reflecting the lexicographic rule `[] < [i₁, …]`.

### Boundaries

- The empty list is always a member, regardless of what `I` is (even if `I` is empty). It represents the length-zero monomial.
- If `I` is empty, the only element of `VTask.Products I` is the empty list, since no non-empty strictly decreasing list over an empty type can exist.
- If `I` has a single element, the only elements of `VTask.Products I` are the empty list and the singleton list containing that one element, since a two-element strictly decreasing list would require two distinct elements.
- Lists of length one are always valid (every singleton list trivially satisfies the decreasing chain condition).

### Not to be confused with

- `List I`: the type of all finite lists over `I`, with no monotonicity or order constraint — `VTask.Products I` is a subtype of this.
- `Finset I`: the type of finite sets (unordered, no repetition) of elements of `I` — unlike `VTask.Products I`, a `Finset` carries no notion of ordering of its elements.
- The multilinear / polynomial notion of "monomial": while elements of `VTask.Products I` are used to index monomials via an evaluation map, the type itself is purely the combinatorial data of a strictly decreasing list, not an algebraic object.