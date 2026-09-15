## Object

`VTask.casesOn` is a case-analysis principle (eliminator) for the free monoid `FreeMonoid α`. Given any element `xs` of the free monoid, it reduces the task of constructing a value in a motive `C xs` to two sub-tasks: (1) handle the case where `xs` is the identity element `1` (the empty word), and (2) handle the case where `xs` has the form `FreeMonoid.of x * xs'` for some letter `x : α` and some tail `xs' : FreeMonoid α`. This is the multiplicative analogue of `List.casesOn` (emptiness vs. cons).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.casesOn : {α : Type u_1} -> {C : FreeMonoid α → Sort u_6} -> (xs : FreeMonoid α) -> (h0 : C 1) -> (ih : (x : α) → (xs : FreeMonoid α) → C (FreeMonoid.of x * xs)) -> C xs
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_1} -> {C : FreeMonoid α → Sort u_6} -> (xs : FreeMonoid α) -> (h0 : C 1) -> (ih : (x : α) → (xs : FreeMonoid α) → C (FreeMonoid.of x * xs)) -> C xs`

The implicit type parameter `α` is the alphabet whose letters generate the free monoid. The implicit `C` is the motive: a type family indexed by elements of `FreeMonoid α`, specifying what must be produced for each element. The explicit argument `xs` is the free-monoid element being analysed. `h0` is the value to return (or the proof to supply) when `xs` equals the identity `1`. `ih` is a function that, given a head letter `x` and a tail `xs'`, produces the value (or proof) for the element `FreeMonoid.of x * xs'`.

## Conventions

No special junk-value or boundary conventions are declared for this definition: it is a total eliminator whose two branches are exhaustive and cover every element of `FreeMonoid α` with no edge cases requiring special treatment.

## Worked examples

- Claim: `VTask.casesOn (1 : FreeMonoid ℕ) "empty" (fun _ _ => "nonempty") = "empty"` — applying `casesOn` to the identity element `1` always selects the `h0` branch.

- Claim: `VTask.casesOn (FreeMonoid.of 5 * 1 : FreeMonoid ℕ) "empty" (fun x _ => x) = 5` — applying `casesOn` to a singleton word `FreeMonoid.of 5` selects the `ih` branch with head `5` and tail `1`.

- Claim: For any `xs : FreeMonoid α`, `VTask.casesOn xs h0 ih` produces a term of type `C xs`, covering both the empty and non-empty cases.

## Boundaries

- When `xs = 1` (the empty word / identity element), only `h0` is consulted; `ih` is never called.
- When `xs = FreeMonoid.of x * xs'` for any `x` and `xs'`, only `ih x xs'` is consulted; this includes the case `xs' = 1` (a single-letter word).
- The eliminator is exhaustive: every element of `FreeMonoid α` is either `1` or of the form `FreeMonoid.of x * xs'`, so the two branches together cover all inputs without overlap.
- The motive `C` may range over any `Sort`, so `casesOn` works both for constructing data and for proving propositions.

## Not to be confused with

- `FreeMonoid.recOn` — a full induction principle for `FreeMonoid α` that provides an inductive hypothesis for the tail, whereas `casesOn` only splits into two cases with no inductive hypothesis.
- `List.casesOn` — the direct analogue for lists using `[]` and `x :: xs` notation; `VTask.casesOn` is its multiplicative `FreeMonoid` counterpart using `1` and `FreeMonoid.of x * xs`.
- `FreeAddMonoid.casesOn` — the additive version of the same principle, using `0` and `FreeAddMonoid.of x + xs` instead of `1` and `FreeMonoid.of x * xs`.