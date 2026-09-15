## 1. Object

`VTask.trNormal` is a function that translates a single statement (instruction) of a two-stack Turing machine (TM2) into an equivalent statement of a one-tape Turing machine (TM1), as part of the compilation from TM2 to TM1. Non-stack operations (loading a value into the state register, branching on the state, jumping to a label, halting) are translated directly into their TM1 counterparts. Stack operations (push, peek, pop) cannot be executed immediately on a flat tape without first locating the relevant stack's top; they are therefore deferred by emitting a TM1 `goto` that jumps to a special intermediate `go` state, where the stack top will be sought before the operation is carried out.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.trNormal : {K : Type u_1} -> {Γ : K → Type u_2} -> {Λ : Type u_3} -> {σ : Type u_4} -> Turing.TM2.Stmt Γ Λ σ → Turing.TM1.Stmt (Turing.TM2to1.Γ' K Γ) (Turing.TM2to1.Λ' K Γ Λ σ) σ
<!-- PINNED-SIGNATURE:END -->


The first implicit argument `K` is the type indexing the stacks of the TM2 machine. The second implicit argument `Γ` assigns to each stack index the type of symbols that stack holds. The third implicit argument `Λ` is the type of user-visible labels (jump targets) of the TM2 machine. The fourth implicit argument `σ` is the type of the internal state register shared by both machines. The single explicit argument is the TM2 statement to be translated.

## 3. Conventions

There are no junk-value or default-output conventions for this function: it is a total structural translation defined on every constructor of the TM2 statement type, and every input produces a meaningful TM1 statement.

## 4. Worked Examples

- Claim: Translating a TM2 `halt` statement yields a TM1 `halt` statement, i.e., `VTask.trNormal Turing.TM2.Stmt.halt = Turing.TM1.Stmt.halt`.

- Claim: Translating a TM2 `goto l` statement yields a TM1 `goto` statement that wraps the label via the `normal` embedding, so the resulting TM1 machine jumps to `normal (l s)` for state `s`.

- Claim: Translating a TM2 `push k f q` statement (pushing symbol `f` onto stack `k` and then continuing with `q`) yields a TM1 `goto` that immediately jumps to the `go k (StAct.push f) q` intermediate state, deferring the actual push until the stack top is located on the flat tape.

- Claim: Translating a TM2 `branch f q1 q2` statement yields a TM1 `branch` statement whose two sub-branches are the translations of `q1` and `q2` respectively, and whose condition ignores the tape symbol, consulting only the state register via `f`.

## 5. Boundaries

- The function is total: every TM2 statement constructor has a case.
- For stack operations (`push`, `peek`, `pop`), the translated TM1 statement does not perform the operation immediately; it only redirects control to an intermediate `go` state. The actual stack manipulation happens later during TM1 execution.
- For `load` and `branch`, the translation recurses on the continuation(s), so the entire reachable sub-program is translated eagerly.
- The tape-alphabet type of the resulting TM1 statement is `Γ' K Γ` (a product of optional stack symbols across all stacks), and the label type is `Λ' K Γ Λ σ` (an extended label set that includes both user labels and the auxiliary `go`/`ret` states needed for stack simulation).

## 6. Not to be confused with

- `Turing.TM2to1.tr`: the full TM2-to-TM1 machine translator, which wraps `VTask.trNormal` together with the `go` and `ret` state handlers to produce a complete TM1 machine, not just a statement translation.
- `Turing.TM2to1.trNormal_run`: a lemma stating that `VTask.trNormal` applied to a `stRun s q` compound equals a `goto` to the `go` state; this is a theorem about `VTask.trNormal`, not the function itself.
- `Turing.TM1to2`: a separate, unrelated compilation direction (TM1 to TM2), not the inverse of this translation.