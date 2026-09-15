## Object

`VTask.SupportsStmt S q` is a predicate expressing that a TM1 (Turing machine) statement `q` is *supported by* a finite set of labels `S`. Concretely, every `goto` instruction appearing anywhere inside `q` (including inside conditional branches, tape-write continuations, etc.) must target only labels that already belong to `S`. In other words, `q` never jumps to a label outside the "allowed" set `S`, so `S` is a closed universe of subroutines with respect to `q`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.SupportsStmt : {Γ : Type u_1} -> {Λ : Type u_2} -> {σ : Type u_3} -> (S : Finset Λ) -> Turing.TM1.Stmt Γ Λ σ → Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.SupportsStmt : {Γ : Type u_1} -> {Λ : Type u_2} -> {σ : Type u_3} -> (S : Finset Λ) -> Turing.TM1.Stmt Γ Λ σ → Prop`

`Γ` is the tape alphabet type; `Λ` is the type of statement labels (the "subroutine identifiers"); `σ` is the type of internal machine state. The explicit argument `S` is the finite set of labels considered admissible — the "support set". The second explicit argument is the TM1 statement being checked for containment within that support.

## Conventions

The predicate is defined by structural recursion on the statement. Sequencing constructors (`move`, `write`, `load`) propagate the predicate to their continuation; `branch` requires both branches to be supported; `goto l` requires that for every tape symbol and every machine state, the label `l a v` lies in `S`; and `halt` is trivially supported by any set (the proposition holds unconditionally).

## Worked examples

- Claim: For any label set `S`, `VTask.SupportsStmt S (.halt)` holds, because `halt` contains no `goto` instructions.

- Claim: `VTask.SupportsStmt {l} (.goto (fun _ _ => l))` holds when `l` is in the singleton set `{l}`, since the only target label is `l` itself.

- Claim: If `VTask.SupportsStmt S q₁` and `VTask.SupportsStmt S q₂`, then `VTask.SupportsStmt S (.branch f q₁ q₂)` holds, because a `branch` statement is supported whenever both of its branches are.

- Claim: `VTask.SupportsStmt ∅ (.goto (fun _ _ => l))` does **not** hold for any `l`, because the required target `l` is not in the empty set.

## Boundaries

- **`halt`**: Always supported by every set, including the empty set, since it contains no `goto` instructions.
- **`goto` with an empty label set**: Never supported (even by vacuously constant jump functions) unless there are no possible inputs — in general, `goto l` against `S = ∅` fails.
- **Monotonicity in `S`**: If `VTask.SupportsStmt S q` holds and `S ⊆ S'`, then `VTask.SupportsStmt S' q` holds, because every target label that was in `S` is also in `S'`.
- **Sub-statements**: If `q₁` is a sub-statement of `q₂` and `q₂` is supported by `S`, then `q₁` is also supported by `S` (captured by `stmts₁_supportsStmt_mono`).
- **`goto` with a function argument**: The label targeted by `goto l` may depend on both the current tape symbol and internal state; support requires the condition to hold for **all** possible tape symbols and states, not just some.

## Not to be confused with

- `Turing.TM1.Supports M S`: A stronger, machine-level predicate asserting that the entire TM program (a function `Λ → Stmt`) is closed under `S`, which additionally requires every label in `S` to map to a statement supported by `S` and an initial label to be in `S`.
- `Turing.TM1.stmts₁ q`: The finite set of all sub-statements reachable from `q`; related but measures reachability rather than label containment.
- `Turing.TM0.Supports`: The analogous support predicate for TM0 machines, which have a different instruction set and a different notion of "goto".