## Object

`VTask.inductionOn` is the structural induction principle for length-indexed vectors (`List.Vector α n`). Given a motive `C` that assigns a type (or proposition) to every vector of every length, and given proofs of the base case (the empty vector) and the inductive step (prepending an element), `VTask.inductionOn` produces a term of type `C v` for any concrete vector `v`. It is the canonical eliminator for `List.Vector`, analogous to `List.rec` for ordinary lists.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.inductionOn : {α : Type u_1} -> {C : {n : ℕ} → List.Vector α n → Sort u_6} -> {n : ℕ} -> (v : List.Vector α n) -> (nil : C List.Vector.nil) -> (cons : {n : ℕ} → {x : α} → {w : List.Vector α n} → C w → C (x ::ᵥ w)) -> C v
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_1} -> {C : {n : ℕ} → List.Vector α n → Sort u_6} -> {n : ℕ} -> (v : List.Vector α n) -> (nil : C List.Vector.nil) -> (cons : {n : ℕ} → {x : α} → {w : List.Vector α n} → C w → C (x ::ᵥ w)) -> C v`

- `α` is the element type of the vectors, implicit and inferred from context.
- `C` is the motive: a family of types (or propositions) indexed by both the length `n` and the vector itself; it is what we are constructing or proving by induction.
- `n` is the length of the vector being eliminated; it is implicit and inferred from `v`.
- `v` is the specific vector on which induction is performed.
- `nil` is the base case: a proof or value of type `C List.Vector.nil` (the empty vector).
- `cons` is the inductive step: given any element `x`, any shorter vector `w`, and a value `C w` already constructed for `w`, it produces `C (x ::ᵥ w)` for the extended vector.

## Conventions

All arguments except `v`, `nil`, and `cons` are implicit; the elaborator infers `α`, `C`, and `n` from usage. There are no junk-value conventions because the function is total over all well-typed inputs.

## Worked examples

- Claim: Applying `VTask.inductionOn` to the empty vector with base case `b` and step `s` returns `b` unchanged.
  ```lean
  example {α : Type*} {C : ∀ {n}, List.Vector α n → Sort*}
      (b : C List.Vector.nil)
      (s : ∀ {n} {x : α} {w : List.Vector α n}, C w → C (x ::ᵥ w)) :
      VTask.inductionOn List.Vector.nil b s = b := List.Vector.inductionOn_nil b s
  ```

- Claim: Applying `VTask.inductionOn` to a cons vector `x ::ᵥ w` with step `s` reduces to `s` applied to the result of the induction on `w`.
  ```lean
  example {α : Type*} {C : ∀ {n}, List.Vector α n → Sort*}
      (x : α) {n : ℕ} (w : List.Vector α n)
      (b : C List.Vector.nil)
      (s : ∀ {n} {x : α} {w : List.Vector α n}, C w → C (x ::ᵥ w)) :
      VTask.inductionOn (x ::ᵥ w) b s = s (VTask.inductionOn w b s) :=
    List.Vector.inductionOn_cons x w b s
  ```

- Claim: For a constant motive `C v = ℕ`, `VTask.inductionOn` on a length-2 vector computes by two applications of the `cons` step.

- Claim: `VTask.inductionOn` serves as the default induction principle invoked by the `induction` tactic on a `List.Vector` hypothesis, decomposing the goal into a `nil` subgoal and a `cons` subgoal.

## Boundaries

- When `n = 0`, the only possible vector is `List.Vector.nil`, so `VTask.inductionOn` always returns the `nil` argument directly.
- When `n > 0`, every vector must have the form `x ::ᵥ w` for some `x` and `w` of length `n - 1`, so `VTask.inductionOn` always invokes the `cons` argument exactly once and recurses.
- The function is total: it is defined for every combination of `α`, `C`, `n`, and `v`.
- The `cons` argument receives `n`, `x`, and `w` as implicit arguments; the explicit argument is only the inductive hypothesis `C w`.
- The motive `C` ranges over `Sort u_6`, so `VTask.inductionOn` works uniformly for both data (computing a value) and proof (proving a proposition).

## Not to be confused with

- `List.Vector.casesOn`: a case-analysis principle that does not provide a recursive hypothesis for `w` in the `cons` branch; it handles one level of structure without recursion.
- `List.Vector.recOn`: a direct recursor that may differ in argument order or implicit-argument structure; `VTask.inductionOn` is the user-facing induction principle chosen as the default for the `induction` tactic.
- `List.rec` (ordinary list recursion): operates on `List α` without a length index and does not enforce the length invariant that `List.Vector` carries.