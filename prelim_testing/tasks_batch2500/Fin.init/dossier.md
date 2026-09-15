## 1. Object

`VTask.init` extracts the **first `n` entries** of a dependent tuple of length `n+1`. Given a function `q` that assigns a value of type `α i` to every index `i : Fin (n+1)`, it returns the restriction of `q` to the first `n` indices (those of the form `i.castSucc` for `i : Fin n`), thereby dropping the last component.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.init : {n : ℕ} -> {α : Fin (n + 1) → Sort u_1} -> (q : (i : Fin (n + 1)) → α i) -> (i : Fin n) -> α i.castSucc
<!-- PINNED-SIGNATURE:END -->


```
VTask.init : {n : ℕ} -> {α : Fin (n + 1) → Sort u_1} -> (q : (i : Fin (n + 1)) → α i) -> (i : Fin n) -> α i.castSucc
```

- `n` is the natural number such that the source tuple has length `n+1` and the result has length `n`; it is inferred implicitly.
- `α` is the dependent type family over `Fin (n+1)` that specifies the type of each entry; it is inferred implicitly.
- `q` is the full `(n+1)`-tuple (a dependent function on `Fin (n+1)`) from which the initial segment is extracted.
- `i` is an index in `Fin n`; the result at `i` is the value of `q` at the corresponding cast-successor index `i.castSucc : Fin (n+1)`.

## 3. Conventions

There are no junk-value or out-of-domain conventions to declare: the function is defined on all inputs without restriction, and every output is determined by a straightforward restriction of the input tuple.

## 4. Worked Examples

- Claim: For the constant tuple `q : Fin 4 → ℕ` with all entries equal to `7`, `VTask.init q` evaluated at any `i : Fin 3` equals `7`.

- Claim: If `p : Fin n → α` is any tuple and `x : α (Fin.last n)`, then `VTask.init (Fin.snoc p x) = p` (removing the appended last element recovers the original tuple).

- Claim: For the tuple `q : Fin 3 → ℕ` defined by `q ⟨0,_⟩ = 10`, `q ⟨1,_⟩ = 20`, `q ⟨2,_⟩ = 30`, the initial segment `VTask.init q` satisfies `VTask.init q ⟨0,_⟩ = 10` and `VTask.init q ⟨1,_⟩ = 20`.

- Claim: Appending the last component back onto the initial segment reconstructs the original tuple: `Fin.snoc (VTask.init q) (q (Fin.last n)) = q`.

## 5. Boundaries

- When `n = 0`, the result type is a function on `Fin 0`, which is the unique empty dependent function. The `init` of any length-1 tuple is this empty tuple.
- The last entry `q (Fin.last n)` is never included in the output; `VTask.init` strictly excludes the final index.
- Updating `q` at the last index `Fin.last n` does not change `VTask.init q`, since the last index is not among the `castSucc` images.
- Updating `q` at a `castSucc` index propagates correctly: `VTask.init (update q i.castSucc y) = update (VTask.init q) i y`.

## 6. Not to be confused with

- `Fin.tail`: extracts the **last `n`** entries of an `(n+1)`-tuple (i.e., drops the *first* component, not the last).
- `Fin.snoc`: the **inverse operation** that appends a new last element to an `n`-tuple to form an `(n+1)`-tuple.
- `Fin.take m h v`: a more general truncation that keeps the first `m` entries for any `m ≤ n`; `VTask.init` is the special case `m = n`.