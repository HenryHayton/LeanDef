## Object

`VTask.contSupp k` computes the finite set of Turing-machine states (labels in the compiled two-stack machine `TM2`) that can be visited while evaluating the continuation `k`, **excluding** the initial return-entry state `ret k` itself. In other words, it is the "support" — the set of internal machine states that must be present in any valid set of supported states — needed to run `k` to completion once it has been entered.

Continuations here represent the "rest of the computation" in a partial-recursive-function evaluator that has been compiled down to a two-stack Turing machine. Their support sets are used to prove that the compiled machine is self-consistent: every state it can reach is declared in the machine's support.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.contSupp : Turing.PartrecToTM2.Cont' → Finset Turing.PartrecToTM2.Λ'
<!-- PINNED-SIGNATURE:END -->


`VTask.contSupp : Turing.PartrecToTM2.Cont' → Finset Turing.PartrecToTM2.Λ'`

The single argument is a continuation value drawn from the inductive type `Cont'`, whose constructors correspond to the different "calling contexts" that arise during evaluation of partial-recursive functions: building the first element of a `cons` pair (`cons₁`), building the second (`cons₂`), function composition (`comp`), fixed-point recursion (`fix`), and the empty continuation that returns to the top level (`halt`).

## Conventions

The initial state `ret k` is **not** included in `VTask.contSupp k`; it is intentionally excluded. The set only covers states visited *after* `ret k` is entered, not the entry point itself.

For the `halt` continuation, the support is empty (`∅`), because `halt` has no internal states to visit — it immediately terminates.

## Worked examples

- Claim: `VTask.contSupp Cont'.halt = ∅`
  The halt continuation has no internal states, so its support is the empty finset.

- Claim: `VTask.contSupp (Cont'.cons₂ k) = trStmts₁ (head stack (Λ'.ret k)) ∪ VTask.contSupp k`
  The `cons₂` continuation must run a `head` operation on the stack before returning via `ret k`, so its support adds exactly the states from that `head` subroutine to the support already required by the tail continuation `k`.

- Claim: `VTask.contSupp (Cont'.comp f k) = codeSupp f k`
  The `comp` continuation's support coincides with the code-support of `f` under `k`, since composing `f` into `k` requires running all states needed to execute `f` with `k` as its own continuation.

- Claim: `VTask.contSupp (Cont'.fix f k) = codeSupp (Code.fix f) k`
  The `fix` continuation's support equals the code-support of the fixed-point wrapper `Code.fix f` under `k`, capturing all states needed for the recursive loop.

## Boundaries

- **`Cont'.halt`**: returns `∅`; this is the base case of the recursion and the only continuation with an empty support.
- **`Cont'.cons₁ fs k`**: produces the largest support among all constructors, since it must include states for data-movement routines, the normal-form translation of `fs`, and then the support of `Cont'.cons₂ k`.
- The function is total: it is defined for every well-formed `Cont'` value and always returns a finite set.
- The support sets are monotone in the sense that `VTask.contSupp k ⊆ VTask.contSupp (cons₁ fs k)`, because the inner continuation's support is included in the outer one.
- The `ret k` state itself is never a member of `VTask.contSupp k` by design; it belongs to the caller's responsibility.

## Not to be confused with

- **`codeSupp`**: the analogous support set for a `Code` value paired with a continuation; `VTask.contSupp` handles the continuation half while `codeSupp` handles the code half, and they are mutually recursive.
- **`trStmts₁ s`**: the set of *sub-states* of a single compiled statement `s`; `VTask.contSupp` is a union of many such sets across the entire continuation, not just one statement.
- **`Λ'.ret k`** (the state `ret k`): the entry-point state for continuation `k`, which is explicitly *excluded* from `VTask.contSupp k` even though it is the state that dispatches into the support set.
