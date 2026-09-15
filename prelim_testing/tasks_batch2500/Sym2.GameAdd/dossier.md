## Object

`VTask.GameAdd rα x y` is a binary relation on unordered pairs (elements of `Sym2 α`). It holds when the unordered pair `x` can be obtained from the unordered pair `y` by strictly decreasing one of its two entries with respect to the relation `rα`, while the other entry is left unchanged. Because the pairs are *unordered*, decreasing either the "first" or the "second" element (in any labelling of the two) suffices.

Intuitively, this is the combinatorial game analog of a lexicographic or product well-founded relation, lifted from ordered pairs to unordered pairs: a position `x` in a two-player game beats `y` if a single move (a decrease in one component under `rα`) transforms `y` into `x`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.GameAdd : {α : Type u_1} -> (rα : α → α → Prop) -> Sym2 α → Sym2 α → Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.GameAdd : {α : Type u_1} -> (rα : α → α → Prop) -> Sym2 α → Sym2 α → Prop`

The type `α` is the implicit universe-polymorphic carrier type whose elements form the entries of the unordered pairs. The argument `rα` is the well-order (or more generally, any binary relation) on `α` that measures "decrease"; it determines what it means for one entry to be smaller than another. The second argument is the unordered pair being tested as the *smaller* (reachable) position; the third argument is the unordered pair being tested as the *larger* (starting) position. So `VTask.GameAdd rα x y` reads: "x is reachable from y by one decreasing step."

## Conventions

No special junk-value or boundary conventions are declared for this definition: it is a straightforwardly total relation on all elements of `Sym2 α`, and its behaviour on arbitrary or degenerate inputs (such as diagonal pairs `s(a, a)`) is fully determined by `rα` without any special casing.

## Worked examples

- Claim: For the strict less-than relation on `ℕ`, `VTask.GameAdd (· < ·) s(1, 5) s(3, 5)` holds, because 1 < 3 and the other entry 5 is unchanged.

- Claim: For the strict less-than relation on `ℕ`, `VTask.GameAdd (· < ·) s(5, 1) s(3, 5)` also holds, because the pair `s(5, 1)` equals `s(1, 5)` as an unordered pair, and 1 < 3 with 5 unchanged.

- Claim: If `rα` is well-founded on `α`, then `VTask.GameAdd rα` is well-founded on `Sym2 α`.

- Claim: `VTask.GameAdd rα s(a₁, b) s(a₂, b)` holds whenever `rα a₁ a₂`, i.e., decreasing the first listed entry while keeping the second fixed gives a smaller unordered pair.

- Claim: `VTask.GameAdd rα s(a, b₁) s(a, b₂)` holds whenever `rα b₁ b₂`, i.e., decreasing the second listed entry while keeping the first fixed is equally valid.

## Boundaries

- **Diagonal pairs** (`s(a, a)`): The relation behaves normally; `VTask.GameAdd rα s(a', a') s(a, a)` holds if and only if `rα a' a` (decreasing both equal entries simultaneously, which in an unordered pair is the same as decreasing one).
- **Irreflexivity**: `VTask.GameAdd rα x x` is false whenever `rα` is irreflexive (e.g., strict orders), since no entry can strictly decrease to itself.
- **Empty/trivial relation**: If `rα` is the empty relation (never holds), then `VTask.GameAdd rα` is also everywhere false.
- **Well-foundedness transfer**: If `rα` is well-founded, `VTask.GameAdd rα` is well-founded on `Sym2 α`, enabling well-founded induction over unordered game positions.
- **Symmetry of unordered pairs**: Because elements of `Sym2 α` are unordered, `VTask.GameAdd rα s(a, b) s(c, d)` and `VTask.GameAdd rα s(b, a) s(c, d)` are the same proposition.

## Not to be confused with

- `Prod.GameAdd rα rβ`: The ordered-pair version of this relation, where the two entries have potentially different types and their positions are distinguished; unlike `VTask.GameAdd`, swapping the components changes the meaning.
- `Sym2.Rel`: The symmetric relation used to define `Sym2` itself (the quotient), not a well-founded game relation on pairs.
- `Sym2.lift₂`: The general tool for defining functions out of `Sym2 α × Sym2 α` respecting symmetry; not itself a game-theoretic relation.