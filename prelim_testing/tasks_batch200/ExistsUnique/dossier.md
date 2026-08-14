## 1. Object

`VTask.ExistsUnique p` is the proposition that the predicate `p` holds for exactly one element of its domain type. More precisely, it asserts two things simultaneously: there is at least one element satisfying `p`, and any two elements satisfying `p` must be equal. This is the standard mathematical concept of "there exists a unique …".

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ExistsUnique : {α : Sort u_1} -> (p : α → Prop) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.ExistsUnique : {α : Sort u_1} -> (p : α → Prop) -> Prop
```

The implicit argument `α` is the ambient type (or sort) from which the unique element is drawn. The explicit argument `p` is the predicate whose unique witness is being asserted: a function that assigns a proposition to each element of `α`.

## 3. Conventions

There are no junk-value conventions declared for this definition: it is a total, Prop-valued function with no edge cases requiring special junk-value treatment — it is well-formed for every predicate `p` on every type `α`.

## 4. Worked examples

- Claim: `VTask.ExistsUnique (fun n : Nat => n = 0)` holds, because `0` is the only natural number equal to `0`.

- Claim: `VTask.ExistsUnique (fun n : Nat => n < 1)` holds, because the only natural number strictly less than `1` is `0`.

- Claim: `VTask.ExistsUnique (fun n : Nat => n = n)` does **not** hold (it is false), because every natural number satisfies `n = n`, so the witness is not unique.

- Claim: `VTask.ExistsUnique (fun n : Nat => n + 1 = 0)` does **not** hold (it is false), because no natural number satisfies `n + 1 = 0`, so existence fails.

## 5. Boundaries

- **Empty type:** If `α` is uninhabited, `VTask.ExistsUnique p` is always false for any `p`, since existence cannot be satisfied.
- **Universally true predicate:** If `p x` holds for all `x : α`, then `VTask.ExistsUnique p` is true if and only if `α` has exactly one element (i.e., `α` is a `Subsingleton` with a witness).
- **Universally false predicate:** If `p x` is false for all `x`, then `VTask.ExistsUnique p` is false because the existence part fails.
- **Singleton type:** For a type `α` with exactly one element, `VTask.ExistsUnique p` is equivalent to `p` holding for that single element.
- The uniqueness direction of the unfolding states: any `y` satisfying `p` must equal the witness `x`, so it canonically picks out a preferred direction (`y = x` rather than `x = y`).

## 6. Not to be confused with

- `∃ x, p x` (bare existential): asserts existence but not uniqueness; `VTask.ExistsUnique p` is strictly stronger.
- `Subsingleton { x | p x }`: asserts that at most one element satisfies `p` but does not require that any element exists; `VTask.ExistsUnique p` additionally requires existence.
- `Function.Injective` / `Function.Bijective`: these concern injectivity or bijectivity of functions, not existence and uniqueness of a predicate's witness.