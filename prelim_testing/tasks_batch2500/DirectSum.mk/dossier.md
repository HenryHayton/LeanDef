## Object

`VTask.mk β s x` constructs an element of the direct sum `⨁ i, β i` from a function `x` defined only on a finite index set `s`. The resulting element agrees with `x` on every index in `s` and is zero at every index outside `s`. The construction is packaged as an additive group homomorphism (in its last argument `x`), so it respects addition and sends the zero function to the zero element of the direct sum.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mk : {ι : Type v} -> (β : ι → Type w) -> [(i : ι) → AddCommMonoid (β i)] -> [DecidableEq ι] -> (s : Finset ι) -> ((i : ↑↑s) → β ↑i) →+ DirectSum ι fun i => β i
<!-- PINNED-SIGNATURE:END -->


The implicit argument `ι` is the index type. The argument `β` is the family of abelian groups (or additive commutative monoids) indexed by `ι`; the direct sum is taken over this family. The instance argument `[AddCommMonoid (β i)]` supplies the additive structure on each component. The instance argument `[DecidableEq ι]` is needed to decide index equality when assembling the finitely-supported element. The argument `s` is the finite subset of indices on which the input function is defined. The final argument (the source of the homomorphism) is a function that assigns to each element of `s` a value in the corresponding component `β i`; the homomorphism maps such a function to the corresponding element of `⨁ i, β i`.

## Conventions

For any index `i` not belonging to `s`, the coefficient of `VTask.mk β s x` at `i` is the zero element of `β i`; there is no special sentinel or error value — the direct sum genuinely carries zero there.

## Worked examples

- Claim: For `s = {0, 1} : Finset (Fin 2)` and the family `β i = ℤ`, `VTask.mk (fun _ => ℤ) s x` evaluated at index `0` equals `x ⟨0, mem_s⟩`, and at any index outside `s` equals `0`.

- Claim: `VTask.mk β s` is an `AddMonoidHom`, so `VTask.mk β s (x + y) = VTask.mk β s x + VTask.mk β s y` for any two functions `x y : (↑s : Set ι) → β ·`.

- Claim: `VTask.mk β s 0 = 0` in `⨁ i, β i` — the zero function maps to the zero element of the direct sum.

- Claim: For the empty finset `s = ∅`, `VTask.mk β ∅ x = 0` for the unique function `x` out of the empty type, since all coefficients are zero.

## Boundaries

- When `s = ∅`, the source type `(↑∅ : Set ι) → β i` has a unique inhabitant (the vacuous function), and `VTask.mk β ∅` maps it to the zero element `0 : ⨁ i, β i`.
- When `s` is a singleton `{j}`, the result is an element supported exactly at `j` with the given value, zero everywhere else.
- The homomorphism property holds even when `s` is all of `ι` (provided `ι` is itself finite), in which case every index gets its specified value.
- Indices in `s` receive the exact value supplied by `x`; there is no truncation or modification of those values.

## Not to be confused with

- `DirectSum.of β i` — injects a single component `β i` into `⨁ i, β i` at one specified index, rather than assembling values over a whole finite set.
- `DFinsupp.mk` — the underlying `DFinsupp` (dependent finitely-supported function) constructor on which `VTask.mk` is based, but which is not packaged as an `AddMonoidHom`.
- `DirectSum.toAddMonoid` — maps *out* of a direct sum via a family of homomorphisms, which is the adjoint/universal direction compared to `VTask.mk` which maps *into* the direct sum.