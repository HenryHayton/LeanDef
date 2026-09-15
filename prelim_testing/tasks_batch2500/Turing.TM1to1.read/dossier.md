## 1. Object

`VTask.read` constructs a Turing machine statement (instruction) for a binary-tape TM1 machine that reads one logical symbol of type `Γ` from the current tape position and then dispatches on that symbol. Concretely, it scans forward through the `n` consecutive Boolean tape cells that encode one `Γ`-symbol (collecting them into a length-`n` bit vector), decodes that vector back to a `Γ`-value using the supplied decoder `dec`, and finally steps `n` positions back to the left (restoring the head to where it started) before handing control to the continuation `f` applied to the decoded symbol.

In short, `VTask.read dec f` is the TM1 statement that "reads one multi-bit symbol, decodes it, returns to the original head position, and executes `f` on the result."

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.read : {Γ : Type u_1} -> {Λ : Type u_2} -> {σ : Type u_3} -> {n : ℕ} -> (dec : List.Vector Bool n → Γ) -> (f : Γ → Turing.TM1.Stmt Bool (Turing.TM1to1.Λ' Γ Λ σ) σ) -> Turing.TM1.Stmt Bool (Turing.TM1to1.Λ' Γ Λ σ) σ
<!-- PINNED-SIGNATURE:END -->


The implicit type parameters `Γ`, `Λ`, `σ`, and `n` fix, respectively, the type of logical tape symbols, the type of original machine labels, the type of machine states, and the number of Boolean tape cells used to encode one `Γ`-symbol. The explicit argument `dec` is the decoding function that converts a length-`n` Boolean vector back into a logical symbol of type `Γ`; it is the inverse of the encoding used when the tape was written. The explicit argument `f` is the continuation: a function that, given a decoded `Γ`-symbol, produces the next TM1 statement to execute.

## 3. Conventions

No special junk-value or edge-case conventions are declared for this definition: it is a total constructor of a `Stmt` value and the natural invariant is simply that `dec` and `f` are the user-supplied decoder and continuation — there are no distinguished degenerate inputs.

## 4. Worked examples

- Claim: For any tape `L R`, stepping `VTask.read dec f` on the translated tape `trTape' enc0 L R` with state `v` is the same as stepping `f R.head` on the same tape — that is, the net effect of reading and repositioning is equivalent to directly applying `f` to the head logical symbol.

- Claim: If every statement `f a` (for all `a : Γ`) is supported by a finite label set `S`, then `VTask.read dec f` is also supported by `S`.

## 5. Boundaries

- When `n = 0`, there are no tape cells to traverse; the bit vector is empty, `dec` receives the empty vector, and no leftward moves are performed. The statement reduces to `f (dec <empty-vector>)` immediately.
- The definition does not check whether `dec` is actually a left inverse of the encoding used on the tape. If `dec` is inconsistent with the encoding, the dispatched continuation `f` receives a logically incorrect symbol, but the statement itself is still well-formed.
- The leftward repositioning always makes exactly `n` steps regardless of tape content; this relies on the invariant that the head was indeed at the start of an encoded block before `VTask.read` was invoked.

## 6. Not to be confused with

- `Turing.TM1to1.readAux`: the internal helper that performs only the forward scanning phase, collecting bits into a vector, without decoding or repositioning the head.
- `Turing.TM1.Stmt.read` (the base TM1 read constructor): reads a single tape symbol directly in a single-symbol-per-cell machine, with no encoding/decoding or multi-step traversal.
- `Turing.TM1to1.move`: performs only the `n`-step head repositioning, with no reading or decoding logic.