## Object

Given a proof that two sets `s` and `t` (subsets of the same ambient type `α`) are equal, `VTask.setCongr h` is the canonical equivalence (bijection) between the subtype `↑s` (elements of `α` together with a proof of membership in `s`) and the subtype `↑t` (elements of `α` together with a proof of membership in `t`). It is the "transport" of the subtype structure along the equality `h : s = t`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.setCongr : {α : Type u_3} -> {s t : Set α} -> (h : s = t) -> ↑s ≃ ↑t
<!-- PINNED-SIGNATURE:END -->


`VTask.setCongr : {α : Type u_3} -> {s t : Set α} -> (h : s = t) -> ↑s ≃ ↑t`

The implicit argument `α` is the ambient type whose elements are being considered. The implicit arguments `s` and `t` are the two sets being compared. The explicit argument `h` is the proof that `s` and `t` are the same set; it is the sole computational input driving the equivalence.

## Conventions

When `h` is `rfl` (the proof that `s = s`), the resulting equivalence is the identity equivalence on `↑s`.

## Worked examples

- Claim: For `s t : Set α` with `h : s = t`, the forward map of `VTask.setCongr h` sends an element `⟨x, hx⟩ : ↑s` to the element `⟨x, h ▸ hx⟩ : ↑t`; in particular, the underlying value `x` is preserved.

- Claim: When `h : s = t` and `h' : t = u`, the composition `(VTask.setCongr h).trans (VTask.setCongr h')` equals `VTask.setCongr (h.trans h')`.

- Claim: For any `h : s = t`, the equivalence `(VTask.setCongr h).symm` is the same as `VTask.setCongr h.symm`.

- Claim: When `h = rfl`, the equivalence `VTask.setCongr h` acts as the identity: applying it to any `x : ↑s` returns `x` with the same underlying value.

## Boundaries

- The function is total: it is defined for any proof `h : s = t`, regardless of the content of `s` and `t` (including empty sets).
- When both `s` and `t` are the empty set and `h : s = t`, the equivalence is the unique equivalence between two empty types.
- When `s = t = Set.univ`, the equivalence is between two copies of `α` itself viewed as subtypes, and reduces to the identity.
- The equivalence is definitionally the identity on underlying values: the forward and backward maps do not change the element of `α`, only its membership proof.

## Not to be confused with

- `Equiv.subtypeEquivProp`: a more general equivalence between subtypes determined by a proof of equal predicates, of which `VTask.setCongr` is a special case for sets.
- `Equiv.Set.ofEq`: a possible alias or variant for the same concept; care should be taken that both the input and output types agree.
- `Equiv.finsetCongr`: an equivalence between `Finset` values (not `Set` subtypes) induced by an equivalence on the element type, a conceptually different construction.