## Object

`VTask.consElim` is the **recursion/elimination principle for non-empty vectors**. Given a length-`(n+1)` vector over a type `α`, it reduces the proof or construction of any property `C` of that vector to the case where the vector is of the form `cons a t` — i.e., a head element `a : α` followed by a tail `t : Vector3 α n`. It guarantees that every non-empty vector can be treated as if it were built by `cons`, which is the unique way to construct a non-empty vector.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.consElim : {α : Type u_1} -> {n : ℕ} -> {C : Vector3 α (n + 1) → Sort u} -> (H : (a : α) → (t : Vector3 α n) → C (Vector3.cons a t)) -> (v : Vector3 α (n + 1)) -> C v
<!-- PINNED-SIGNATURE:END -->


VTask.consElim : {α : Type u_1} -> {n : ℕ} -> {C : Vector3 α (n + 1) → Sort u} -> (H : (a : α) → (t : Vector3 α n) → C (Vector3.cons a t)) -> (v : Vector3 α (n + 1)) -> C v

- `α` is the element type of the vector (implicit).
- `n` is the natural number such that the vector has length `n + 1` (implicit); the `+ 1` guarantees non-emptiness.
- `C` is the motive — a type family (or predicate) over length-`(n+1)` vectors of `α`, which may land in any `Sort u` (i.e., it can produce a type, a proposition, or a term in a universe).
- `H` is the single branch of the recursion: a function that, given a head element `a` and a tail vector `t`, produces a value of `C (Vector3.cons a t)`.
- `v` is the non-empty vector being eliminated; the result has type `C v`.

## Conventions

No special junk-value or boundary conventions are declared for this definition: it is a total function on its stated domain (non-empty vectors of any element type), and every such vector is definitionally equal to some `cons a t`, so there are no degenerate or out-of-domain inputs to handle.

## Worked examples

- Claim: For any `α` and any `v : Vector3 α 1`, applying `VTask.consElim` with the branch that returns the head yields the head of `v`.

- Claim: For any `v : Vector3 Nat 2`, applying `VTask.consElim` with the branch `(fun a t => a)` returns the first component (the head) of `v`.

- Claim: `VTask.consElim (fun a t => a) (Vector3.cons 7 (Vector3.cons 3 Vector3.nil)) = 7` — extracting the head of a concrete two-element nat vector via the eliminator gives `7`.

- Claim: `VTask.consElim (fun a t => t) (Vector3.cons 5 Vector3.nil) = Vector3.nil` — extracting the tail of a singleton vector gives the empty vector.

## Boundaries

- The length index must be of the form `n + 1`; the empty-vector case (`Vector3 α 0`) is excluded by the type. There is no `nilElim` branch because the length guarantees non-emptiness.
- When `v` is already syntactically `Vector3.cons a t`, the eliminator reduces definitionally (via `cons_head_tail`) to `H a t`.
- The motive `C` can target any `Sort u`, so `VTask.consElim` works uniformly for computing values, proving propositions, and constructing types.
- There is no partiality: every vector of positive length has a unique head and tail, so `H` is always applicable.

## Not to be confused with

- `Vector3.cons` — the *constructor* for non-empty vectors; `VTask.consElim` is its *eliminator* (going the other direction).
- The eliminator for *all* vectors (including empty ones), which would require both a `nil` case and a `cons` case; `VTask.consElim` handles only the non-empty case.
- `Vector3.head` / `Vector3.tail` — these extract specific components rather than providing a general-purpose dependent elimination principle.
