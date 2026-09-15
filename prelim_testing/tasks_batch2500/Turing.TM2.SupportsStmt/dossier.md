## Object

`VTask.SupportsStmt S q` is a predicate on TM2 (two-stack Turing machine) statements that asserts every *unconditional* or *conditional* jump in the statement `q` targets only states belonging to the finite set `S`. Informally, the statement is "closed over" `S` in the sense that executing it can never transfer control to a state outside `S`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.SupportsStmt : {K : Type u_1} -> {Γ : K → Type u_2} -> {Λ : Type u_3} -> {σ : Type u_4} -> (S : Finset Λ) -> Turing.TM2.Stmt Γ Λ σ → Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.SupportsStmt : {K : Type u_1} -> {Γ : K → Type u_2} -> {Λ : Type u_3} -> {σ : Type u_4} -> (S : Finset Λ) -> Turing.TM2.Stmt Γ Λ σ → Prop`

The implicit type `K` indexes the stack alphabets; `Γ` assigns a type to each stack; `Λ` is the type of machine states (labels); `σ` is the type of the internal register. The explicit argument `S` is the finite set of allowed target states; the second explicit argument is the TM2 statement whose jump targets are being checked.

## Conventions

For every non-jump statement constructor (`push`, `peek`, `pop`, `load`), the predicate reduces to the same predicate applied to the continuation statement, so tape-manipulation steps impose no constraint of their own. For a `branch` statement the predicate holds exactly when it holds for both branches. For `halt`, the predicate is vacuously true since `halt` never transfers control. For `goto l`, the predicate holds exactly when every state reachable through the label function `l` lies in `S`.

## Worked examples

- Claim: For any finite set `S` of type `Finset Λ`, `VTask.SupportsStmt S (Turing.TM2.Stmt.halt)` holds unconditionally, because `halt` makes no jumps.

- Claim: `VTask.SupportsStmt S (Turing.TM2.Stmt.goto l)` holds if and only if `∀ v, l v ∈ S`; in particular, if `l` is the constant function returning some label `a ∉ S`, the predicate fails.

- Claim: If `VTask.SupportsStmt S q₁` and `VTask.SupportsStmt S q₂` both hold, then `VTask.SupportsStmt S (Turing.TM2.Stmt.branch f q₁ q₂)` also holds, since neither branch can escape `S`.

- Claim: If `q₁` is a sub-statement of `q₂` (i.e., `q₁ ∈ stmts₁ q₂`) and `VTask.SupportsStmt S q₂` holds, then `VTask.SupportsStmt S q₁` holds — the property is inherited by all reachable sub-statements.

## Boundaries

- **`halt`**: Always satisfies the predicate regardless of `S`, including the empty set, because it introduces no jump.
- **`goto` with an empty-range label function**: If `l` has an empty domain (impossible in practice since `σ` is a type and always has terms, but formally speaking `∀ v, l v ∈ S` must hold for all `v : σ`), then for `S = ∅` the predicate fails whenever `σ` is inhabited.
- **`branch`**: Both sub-statements must independently satisfy the predicate; it is not enough for only one branch to be safe.
- **Monotonicity in `S`**: If `VTask.SupportsStmt S q` holds and `S ⊆ S'`, then `VTask.SupportsStmt S' q` holds; shrinking `S` can only invalidate the predicate.
- **Nested tape operations**: A chain of `push`/`peek`/`pop`/`load` instructions inherits its support property entirely from the innermost continuation.

## Not to be confused with

- `Turing.TM2.Supports`: a predicate on an entire TM2 *machine* (a function from states to statements) asserting that every reachable statement from every state in `S` supports `S`; `VTask.SupportsStmt` is the per-statement building block used inside that definition.
- `Turing.TM2.stmts₁`: the set of all sub-statements reachable from a given statement by following continuations; related but purely structural, carrying no membership-in-`S` constraint.
- `Turing.TM2.stmts`: the collection of all sub-statements reachable from the machine's transition function over a set `S` of states; again structural, not the same as checking jump targets.