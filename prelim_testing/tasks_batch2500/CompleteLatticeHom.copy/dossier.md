## Object

`VTask.copy` constructs a new `CompleteLatticeHom` (a homomorphism of complete lattices, preserving arbitrary suprema and infima) from an existing one, but with its underlying function replaced by a provably equal alternative. The resulting homomorphism is definitionally equal to the original as a bundled map, but its underlying function field is literally the supplied replacement. This is a standard "copy" constructor used to repair or adjust definitional equalities without changing mathematical content.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {α : Type u_2} -> {β : Type u_3} -> [CompleteLattice α] -> [CompleteLattice β] -> (f : CompleteLatticeHom α β) -> (f' : α → β) -> (h : f' = ⇑f) -> CompleteLatticeHom α β
<!-- PINNED-SIGNATURE:END -->


`VTask.copy : {α : Type u_2} -> {β : Type u_3} -> [CompleteLattice α] -> [CompleteLattice β] -> (f : CompleteLatticeHom α β) -> (f' : α → β) -> (h : f' = ⇑f) -> CompleteLatticeHom α β`

The implicit type arguments `α` and `β` are the source and target complete lattices, inferred automatically. The complete lattice structure on each type is supplied by instance arguments. `f` is the original complete-lattice homomorphism being copied. `f'` is the new underlying function that will be stored in the returned homomorphism. `h` is a proof that `f'` is pointwise equal to the coercion of `f` to a bare function, guaranteeing that `f'` carries all the same homomorphism properties.

## Conventions

No special junk-value or edge conventions are declared: the definition is total and every combination of inputs satisfying the stated types is meaningful. There is no convention for any degenerate case.

## Worked examples

- Claim: For any `CompleteLatticeHom f` and replacement function `f'` with proof `h : f' = ⇑f`, the coercion of `VTask.copy f f' h` to a bare function equals `f'`.

- Claim: For any `CompleteLatticeHom f` and replacement function `f'` with proof `h : f' = ⇑f`, `VTask.copy f f' h` equals `f` as a `CompleteLatticeHom`.

## Boundaries

- The proof `h` must establish that `f'` is *equal* (not merely pointwise equivalent) to the coercion of `f`; the equality is at the function level, so it covers all inputs simultaneously.
- When `f' = ⇑f` holds by `rfl` (i.e., `f'` is definitionally the coercion of `f`), `VTask.copy` simply returns an object that is propositionally identical to `f` and whose coercion is literally `f'`.
- No element of `α` or `β` is excluded; the definition is total over all complete lattices and all homomorphisms between them.

## Not to be confused with

- `CompleteLatticeHom.mk`: the primary constructor for building a `CompleteLatticeHom` from scratch, supplying all components manually rather than modifying an existing one.
- `SSupHom.copy` / `SInfHom.copy`: analogous copy constructors for homomorphisms preserving only suprema or only infima, not both; `VTask.copy` wraps both of these internally.
- Function extensionality (`funext`): a proof technique that establishes equality of functions; `VTask.copy` instead changes the stored function field at the *data* level within the bundled structure, which `funext` alone cannot do.