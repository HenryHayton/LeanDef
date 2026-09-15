## Object

`VTask.cons` constructs a dependent tuple of length `n+1` by prepending a single element to an existing dependent tuple of length `n`. Concretely, given a type family `α` over `Fin (n+1)`, it takes a value for index `0` and a function assigning values to the remaining indices `1, 2, …, n`, and produces a single function from `Fin (n+1)` to the appropriate types. It is the "cons" (prepend) operation for heterogeneous finite tuples indexed by `Fin`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.cons : {n : ℕ} -> {α : Fin (n + 1) → Sort u} -> (x : α 0) -> (p : (i : Fin n) → α i.succ) -> (i : Fin (n + 1)) -> α i
<!-- PINNED-SIGNATURE:END -->


`VTask.cons : {n : ℕ} -> {α : Fin (n + 1) → Sort u} -> (x : α 0) -> (p : (i : Fin n) → α i.succ) -> (i : Fin (n + 1)) -> α i`

The implicit argument `n` is the length of the tail tuple. The implicit argument `α` is the dependent type family over `Fin (n+1)` that specifies the type at each index. The argument `x` is the head element, i.e., the value placed at position `0`. The argument `p` is the tail, i.e., the existing `n`-tuple giving values at positions `1` through `n` (each of the form `i.succ` for `i : Fin n`). The final argument `i : Fin (n+1)` is the index at which the resulting `(n+1)`-tuple is evaluated.

## Conventions

No special junk-value or out-of-domain conventions are declared: the function is total over all its arguments and every case is handled definitionally by case-splitting on whether the index is zero or a successor.

## Worked examples

- Claim: For the constant type family `α _ = ℕ`, `VTask.cons 5 (fun _ => 7) (0 : Fin 3)` equals `5`.
  ```lean
  example : VTask.cons (α := fun _ => ℕ) 5 (fun _ => 7) (0 : Fin 3) = 5 := by decide
  ```

- Claim: For the constant type family `α _ = ℕ`, `VTask.cons 5 (fun _ => 7) (1 : Fin 3)` equals `7`.
  ```lean
  example : VTask.cons (α := fun _ => ℕ) 5 (fun _ => 7) (1 : Fin 3) = 7 := by decide
  ```

- Claim: For the constant type family `α _ = Bool`, `VTask.cons true (fun i => [false, true].get i) (0 : Fin 3)` equals `true`.
  ```lean
  example : VTask.cons (α := fun _ => Bool) true (fun i => [false, true].get i) (0 : Fin 3) = true := by decide
  ```

## Boundaries

- When `n = 0`, the resulting tuple has length `1`. The tail `p` is a function from `Fin 0`, which is vacuous, so the only meaningful argument is the head `x`, and the result at the unique index `0 : Fin 1` is `x`.
- The function is defined for every index `i : Fin (n+1)` without exception; there is no out-of-range case.
- When `i = 0`, the result is always `x` regardless of `p`.
- When `i = j.succ` for some `j : Fin n`, the result is `p j` regardless of `x`.

## Not to be confused with

- `Fin.snoc`: appends an element at the *end* of a tuple rather than the beginning.
- `List.cons`: prepends to a `List`, which is not a fixed-length dependent function; `VTask.cons` works on `Fin`-indexed dependent tuples.
- `Fin.append`: concatenates two finite tuples of potentially different lengths, rather than prepending a single element.