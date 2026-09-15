## Object

`VTask.copy` constructs a new `ContDiffMapSupportedIn E F n K` — a compactly supported, *n*-times continuously differentiable function from `E` to `F` with support inside the compact set `K` — whose underlying function is replaced by a definitionally different but propositionally equal function `f'`. The resulting element of `ContDiffMapSupportedIn E F n K` carries `f'` as its underlying map while retaining all the analytic and support properties of the original `f`. This is a standard Mathlib pattern for repairing definitional equality issues without changing mathematical content.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {E : Type u_2} -> {F : Type u_3} -> [NormedAddCommGroup E] -> [NormedSpace ℝ E] -> [NormedAddCommGroup F] -> [NormedSpace ℝ F] -> {n : ℕ∞} -> {K : TopologicalSpace.Compacts E} -> (f : ContDiffMapSupportedIn E F n K) -> (f' : E → F) -> (h : f' = ⇑f) -> ContDiffMapSupportedIn E F n K
<!-- PINNED-SIGNATURE:END -->


`VTask.copy : {E : Type u_2} -> {F : Type u_3} -> [NormedAddCommGroup E] -> [NormedSpace ℝ E] -> [NormedAddCommGroup F] -> [NormedSpace ℝ F] -> {n : ℕ∞} -> {K : TopologicalSpace.Compacts E} -> (f : ContDiffMapSupportedIn E F n K) -> (f' : E → F) -> (h : f' = ⇑f) -> ContDiffMapSupportedIn E F n K`

The type parameters `E` and `F` are the domain and codomain normed real vector spaces (inferred implicitly), equipped with their respective `NormedAddCommGroup` and `NormedSpace ℝ` instances. The natural number `n : ℕ∞` is the order of differentiability (possibly infinite). The compact set `K : TopologicalSpace.Compacts E` specifies where the support of functions in the type is required to live. The argument `f` is the original compactly supported smooth map being copied. The argument `f'` is the replacement underlying function — a bare map `E → F`. The proof `h` witnesses that `f'` is propositionally equal to the coercion of `f` as a function, ensuring the copy is mathematically identical to the original.

## Conventions

The copy operation does not change any mathematical data: the resulting element is propositionally equal to the original `f`. The only purpose of `VTask.copy` is to adjust definitional (not propositional) equality of the underlying function, so it is purely a bookkeeping device and carries no new mathematical content.

## Worked examples

- Claim: The coercion of `VTask.copy f f' h` to a function equals `f'` (i.e., the supplied replacement function becomes the new underlying map).
  This is `VTask.coe_copy`: for any `f`, `f'`, `h`, the coercion `⇑(f.copy f' h) = f'`.

- Claim: `VTask.copy f f' h` is propositionally equal to `f` as an element of `ContDiffMapSupportedIn E F n K`, regardless of what `f'` is (as long as `h : f' = ⇑f` holds).
  This is `VTask.copy_eq`: for any `f`, `f'`, `h`, we have `f.copy f' h = f`.

## Boundaries

- The proof argument `h` must be a proof that `f' = ⇑f` (propositional equality of functions); there is no meaningful edge case here since the operation is total and well-typed whenever this proof is supplied.
- When `f' = ⇑f` holds definitionally (not merely propositionally), `VTask.copy` is a no-op in all respects, and `f.copy (⇑f) rfl = f` holds trivially.
- The operation is defined for all smoothness orders `n`, including `n = ∞` (i.e., `⊤ : ℕ∞`), and for any compact set `K` (including the empty compact set).

## Not to be confused with

- `ContDiffMapSupportedIn` itself — the type of compactly supported smooth maps; `VTask.copy` is a constructor-like operation on this type, not the type itself.
- Restriction or truncation of smoothness order — `VTask.copy` does not change `n` or `K`; it only swaps the underlying function for a definitionally distinct but equal one.
- The coercion `⇑f : E → F` — this is the bare function underlying `f`; `VTask.copy` takes such a bare function and wraps it back into the structured type.