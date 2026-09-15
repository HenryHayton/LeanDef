## Object

`VTask.diagElem` extracts the unique element from a diagonal element of the symmetric square `Sym2 α`. Recall that `Sym2 α` consists of unordered pairs `{a, b}` of elements of `α`. An element is called *diagonal* when both components are equal, i.e., it has the form `{a, a}` for some `a : α`. Given a proof that a particular `Sym2 α` element is diagonal, this function computes and returns that repeated element `a`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.diagElem : {α : Type u_1} -> (z : Sym2 α) -> z.IsDiag → α
<!-- PINNED-SIGNATURE:END -->


VTask.diagElem : {α : Type u_1} -> (z : Sym2 α) -> z.IsDiag → α

The implicit argument `α` is the carrier type. The argument `z` is the element of the symmetric square being examined. The final argument is a proof that `z` is diagonal (i.e., `z.IsDiag`), which certifies that a unique representative element exists. The function returns that representative element of type `α`.

## Conventions

When `z = s(a, b)` is a concrete unordered pair and the supplied `IsDiag` proof witnesses `a = b`, the function returns `a` (the first component as written), consistent with `diagElem_mk`.

## Worked examples

- Claim: For `z = s(3, 3)` with `h : IsDiag s(3, 3)`, `VTask.diagElem s(3, 3) h = 3`.
  (Follows directly from `diagElem_mk`: the diagonal element of the pair `s(a, a)` is `a`.)

- Claim: For any `a : α`, the round-trip identity holds: `VTask.diagElem (Sym2.diag a) (Sym2.isDiag_diag a) = a`.
  (Because `Sym2.diag a = s(a, a)`, applying `diagElem_mk` gives `a`.)

- Claim: For any `a : α` and proof `h : (Sym2.diag a).IsDiag`, the result of `VTask.diagElem` satisfies `Sym2.diag (VTask.diagElem (Sym2.diag a) h) = Sym2.diag a`.
  (This is an instance of the round-trip theorem `diag_diagElem`.)

## Boundaries

- The function is only defined when a proof `z.IsDiag` is supplied; it is not defined (and makes no sense) for non-diagonal elements of `Sym2 α`.
- Since `Sym2 α` identifies `s(a, b)` with `s(b, a)`, and a diagonal element has `a = b`, there is no ambiguity in the choice of representative: both components are the same.
- The function is computable (no classical choice is used), relying on the structural proof that `a = b` to directly return `a`.
- For the empty type `α = Empty`, no diagonal element can be formed, so the function is vacuously total (never actually called).

## Not to be confused with

- `Sym2.diag` — the *constructor* that forms the diagonal element `s(a, a)` from a single `a`; `VTask.diagElem` is its left inverse.
- `Sym2.IsDiag` — the *predicate* asserting an element is diagonal, which is the type of the proof argument, not the extraction function itself.
- `Sym2.mem` or `Sym2.out` — other ways to extract or inspect components of a `Sym2` element that do not require a diagonality hypothesis.