## Object

`VTask.erase a f` is the finitely supported function obtained from `f` by setting the value at `a` to zero, leaving all other values unchanged. Concretely, it is the unique finitely supported function `g : α →₀ M` satisfying `g a = 0` and `g a' = f a'` for every `a' ≠ a`. Its support is the support of `f` with the element `a` removed.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.erase : {α : Type u_1} -> {M : Type u_5} -> [Zero M] -> (a : α) -> (f : α →₀ M) -> α →₀ M
<!-- PINNED-SIGNATURE:END -->


`VTask.erase : {α : Type u_1} -> {M : Type u_5} -> [Zero M] -> (a : α) -> (f : α →₀ M) -> α →₀ M`

The implicit type `α` is the index type, and `M` is the value type, which need only carry a distinguished zero element (given by the `Zero M` instance). The explicit argument `a : α` is the index at which the function is zeroed out. The explicit argument `f : α →₀ M` is the finitely supported function being modified.

## Conventions

If `a` is not in the support of `f` (i.e., `f a = 0` already), then `VTask.erase a f` returns `f` unchanged — no normalization or truncation occurs.

## Worked examples

- Claim: Erasing an index from the zero finitely supported function returns zero: `VTask.erase a (0 : α →₀ M) = 0`.

- Claim: The value of `VTask.erase a f` at `a` is always `0`, regardless of what `f a` was: `(VTask.erase a f) a = 0`.

- Claim: The value of `VTask.erase a f` at any `a' ≠ a` equals `f a'`: if `a' ≠ a` then `(VTask.erase a f) a' = f a'`.

- Claim: Erasing `a` from `single a b` (the function supported only at `a` with value `b`) gives the zero function: `VTask.erase a (Finsupp.single a b) = 0`.

- Claim: The decomposition identity holds in an additive commutative monoid: `Finsupp.single a (f a) + VTask.erase a f = f`, showing that `f` splits into its value at `a` and the remainder.

- Claim: Erasing is idempotent: `VTask.erase a (VTask.erase a f) = VTask.erase a f`.

## Boundaries

- **`a` not in support**: If `f a = 0` (equivalently `a ∉ f.support`), then `VTask.erase a f = f` exactly; the support is unchanged and no recomputation is needed.
- **Zero function**: `VTask.erase a 0 = 0` for all `a`; the zero finitely supported function is a fixed point.
- **Repeated erasure**: Applying `VTask.erase a` twice has the same effect as applying it once; it is idempotent.
- **Support characterization**: The support of `VTask.erase a f` is precisely `f.support` with `a` removed, even if `a` was not in `f.support` (removing a non-member is a no-op on the set).
- **Non-erased indices**: For every `a' ≠ a`, `(VTask.erase a f) a' = f a'`; the function is strictly a local modification.

## Not to be confused with

- `Finsupp.update f a 0`: Setting `f` to `0` at `a` via the general update operation — this is provably equal to `VTask.erase a f`, but `update` takes the finitely supported function as its first argument and is stated for general values, not specifically for zeroing.
- `Finset.erase`: The analogous operation on finite sets that removes an element from a `Finset`; `VTask.erase` uses this internally on the support but operates on finitely supported functions, not sets.
- `Finsupp.single a b`: Creates a function supported only at `a` with value `b`; this is essentially the complement of erasure, and together they satisfy `single a (f a) + VTask.erase a f = f`.
