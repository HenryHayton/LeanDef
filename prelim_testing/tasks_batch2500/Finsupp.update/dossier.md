## Object

`VTask.update f a b` is the finitely-supported function obtained from `f : α →₀ M` by overriding its value at the point `a : α` with the new value `b : M`. When `b ≠ 0` the point `a` belongs to the support of the result; when `b = 0` the point `a` is removed from the support. Every other point retains its value from `f`. This is the finitely-supported analogue of the classical function-update operation.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.update : {α : Type u_1} -> {M : Type u_5} -> [Zero M] -> (f : α →₀ M) -> (a : α) -> (b : M) -> α →₀ M
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_1} -> {M : Type u_5} -> [Zero M] -> (f : α →₀ M) -> (a : α) -> (b : M) -> α →₀ M`

The implicit type `α` is the index type; the implicit type `M` is the value type, which must carry a distinguished zero element (supplied by the `[Zero M]` instance). The argument `f` is the finitely-supported function being modified. The argument `a` is the index at which the value is overridden. The argument `b` is the new value to place at `a`.

## Conventions

When `b = 0` the point `a` is erased from the support of the result, preserving finite support without recording a zero value. When `b ≠ 0` the point `a` is inserted into the support of the result if it was not already present.

## Worked examples

- Claim: For any `f : α →₀ M`, updating `f` at `a` with the value `f a` returns `f` unchanged (i.e., `VTask.update f a (f a) = f`).

- Claim: Updating the zero finitely-supported function at `a` with value `b` yields `Finsupp.single a b` (i.e., `VTask.update 0 a b = Finsupp.single a b`).

- Claim: Updating `f` at `a` with `0` equals `f.erase a` (i.e., `VTask.update f a 0 = f.erase a`).

- Claim: For decidable `α`, `(VTask.update f a b) i = if i = a then b else f i`.

## Boundaries

- If `b = 0`, then `a` is removed from the support even if it was previously present with a non-zero value; the result has support equal to `f.support.erase a`.
- If `b ≠ 0`, the support of the result is a subset of `insert a f.support`; in particular if `a` was already in `f.support` the support does not grow.
- Calling `VTask.update f a (f a)` is a no-op: it returns exactly `f`.
- The support of the result is always a subset of `insert a f.support`, regardless of `b`.
- When `f = 0` (the zero finitely-supported function), `VTask.update 0 a b` coincides with `Finsupp.single a b`.

## Not to be confused with

- `Finsupp.erase f a` — removes the value at `a` entirely (equivalent to `VTask.update f a 0`), but does not accept a replacement value.
- `Finsupp.single a b` — creates a fresh finitely-supported function supported only at `a`; `VTask.update` modifies an existing function and retains all other values.
- `Function.update f a b` — the plain (not finitely-supported) function update on `α → M`; it does not track a finite support and can store zero values.