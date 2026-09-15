## Object

`VTask.ofList` converts an ordinary Lean `List` of ZFA lists (elements of type `Lists α`) into a ZFA *prelist* of type `Lists' α true`. In the ZFA (Zermelo–Fraenkel with atoms) set-theoretic hierarchy encoded in Mathlib, a *prelist* tagged with `true` is a well-formed sequence of ZFA sets ready to be treated as a set-of-sets; `ofList` bridges the familiar `List` type and this ZFA structure by translating each element in order.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofList : {α : Type u_1} -> List (Lists α) → Lists' α true
<!-- PINNED-SIGNATURE:END -->


VTask.ofList : {α : Type u_1} -> List (Lists α) → Lists' α true

The implicit type parameter `α` is the type of atoms that the ZFA lists are built over. The explicit argument is the ordinary Lean list of ZFA lists that is to be converted into a ZFA prelist.

## Conventions

The empty list `[]` maps to the distinguished ZFA prelist constructor `nil`, representing the empty prelist. This is the natural base-case junk-free convention: there is no special sentinel value since the function is total and covers every possible input.

## Worked examples

- Claim: `VTask.ofList []` equals the nil ZFA prelist (the empty prelist `Lists'.nil`).

- Claim: For any ZFA list `a : Lists α` and ordinary list `l : List (Lists α)`, `VTask.ofList (a :: l)` equals `Lists'.cons a (VTask.ofList l)`, prepending `a` to the prelist obtained by converting the tail.

- Claim: `VTask.ofList` applied to a singleton `[a]` yields a prelist whose sole element is `a`, i.e., `Lists'.cons a Lists'.nil`.

- Claim: `VTask.ofList` applied to a two-element list `[a, b]` yields `Lists'.cons a (Lists'.cons b Lists'.nil)`.

## Boundaries

- The empty list `[]` is a valid input and produces `Lists'.nil`; there is no undefined or error case.
- The function is defined for all finite lists; since Lean's `List` type contains only finite lists, the function is total with no partial-application concerns.
- The length of the resulting ZFA prelist mirrors the length of the input list, so the conversion is length-preserving.
- The order of elements is preserved: the head of the list becomes the head of the prelist.

## Not to be confused with

- `Lists'.cons` / `Lists'.nil`: these are the raw ZFA prelist constructors that `VTask.ofList` is built from, not a conversion function from `List`.
- `Lists.ofList` (if it existed): `VTask.ofList` targets `Lists' α true` (a prelist), not `Lists α` (a full ZFA list or set).
- `List.toFinset` or similar: those convert lists into mathematical sets with deduplication; `VTask.ofList` preserves duplicates and order, producing a sequential prelist.