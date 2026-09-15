## Object

`VTask.insertNth` constructs a dependent tuple of length `n + 1` by inserting a specified element at a given position into a shorter tuple of length `n`. Given a position `i` in `{0, …, n}`, a value `x` of the appropriate type at that position, and an `n`-tuple `p` whose `j`-th entry has the type dictated by the `j`-th index obtained by skipping over `i`, the result is an `(n+1)`-tuple that places `x` at position `i` and distributes the entries of `p` into the remaining positions (those that are images of `succAbove i`).

Special cases: when `i = 0` the construction coincides with prepending (`Fin.cons`); when `i` is the last index it coincides with appending (`Fin.snoc`).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.insertNth : {n : ℕ} -> {α : Fin (n + 1) → Sort u_1} -> (i : Fin (n + 1)) -> (x : α i) -> (p : (j : Fin n) → α (i.succAbove j)) -> (j : Fin (n + 1)) -> α j
<!-- PINNED-SIGNATURE:END -->


`VTask.insertNth : {n : ℕ} -> {α : Fin (n + 1) → Sort u_1} -> (i : Fin (n + 1)) -> (x : α i) -> (p : (j : Fin n) → α (i.succAbove j)) -> (j : Fin (n + 1)) -> α j`

- `n` (implicit): the length of the shorter tuple; the result has length `n + 1`.
- `α` (implicit): the dependent type family over `Fin (n + 1)`, assigning a sort to each index of the result tuple.
- `i`: the insertion position — a concrete index in `Fin (n + 1)` at which the new element will be placed.
- `x`: the element to insert; its type is `α i`, the fiber of the type family at the insertion point.
- `p`: the original `n`-tuple to be extended; entry `j` has type `α (i.succAbove j)`, meaning each position of `p` is mapped to the appropriate slot in the result by skipping over `i`.
- `j`: the output index at which to evaluate the resulting `(n+1)`-tuple; it ranges over `Fin (n + 1)`.

## Conventions

No special junk-value conventions are declared: the function is total and well-typed by construction, with no edge input requiring a special fallback value.

## Worked examples

- Claim: `VTask.insertNth (0 : Fin 3) 10 ![20, 30] = ![10, 20, 30]`
  (Inserting `10` at position `0` of the 2-tuple `[20, 30]` prepends it, giving `[10, 20, 30]`.)

- Claim: `VTask.insertNth (Fin.last 2) 30 ![10, 20] = ![10, 20, 30]`
  (Inserting `30` at the last position of the 2-tuple `[10, 20]` appends it, giving `[10, 20, 30]`.)

- Claim: `VTask.insertNth (1 : Fin 3) 99 ![0, 1] = ![0, 99, 1]`
  (Inserting `99` at position `1` of the 2-tuple `[0, 1]` places it in the middle.)

- Claim: For any `f : ∀ j : Fin (n+1), α j` and position `p`, reconstructing from the value at `p` and the tuple with `p` removed recovers `f` exactly, i.e., `VTask.insertNth p (f p) (Fin.removeNth p f) = f`.

## Boundaries

- When `i = 0` (the first index), the insertion prepends `x` before all entries of `p`, and the result equals `Fin.cons x p`.
- When `i = Fin.last n` (the last index), the insertion appends `x` after all entries of `p`, and the result equals `Fin.snoc p x`.
- The map sending `x` and `p` to the resulting tuple is injective in each argument separately, and jointly injective (injective as a two-argument function).
- Querying the result at `j = i` returns exactly `x`; querying at any `j` in the image of `i.succAbove` returns the corresponding entry of `p`.
- The product over all indices of the resulting tuple satisfies `∏ j, VTask.insertNth i x p j = x * ∏ j, p j` (in a suitable monoid).

## Not to be confused with

- `Fin.cons`: inserts only at position `0` (prepend); a special case of `VTask.insertNth` with `i = 0`.
- `Fin.snoc`: inserts only at the last position (append); a special case of `VTask.insertNth` with `i = Fin.last n`.
- `Fin.succAboveCases`: the eliminator on which `VTask.insertNth` is directly based; identical in content but presented as a recursor/eliminator rather than an insertion operation.