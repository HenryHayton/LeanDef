## VTask.write

### Object

`VTask.write` constructs a Turing machine statement (instruction sequence) that writes a given list of Boolean values onto the tape, one cell at a time from left to right, and then continues with a specified continuation statement. Starting at the current tape head position, it writes each `Bool` in the list to the current cell and advances the head one step to the right before writing the next value, finally executing the continuation statement after all values have been written.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.write : {Γ : Type u_1} -> {Λ : Type u_2} -> {σ : Type u_3} -> List Bool → Turing.TM1.Stmt Bool (Turing.TM1to1.Λ' Γ Λ σ) σ → Turing.TM1.Stmt Bool (Turing.TM1to1.Λ' Γ Λ σ) σ
<!-- PINNED-SIGNATURE:END -->


The implicit type parameters `Γ`, `Λ`, and `σ` are the alphabet type of the original TM1 machine, its label (state) type, and its memory (stack) type, respectively; these fix the ambient TM1-to-TM1 encoding context. The first explicit argument is the list of `Bool`s to be written onto the tape in order, left to right. The second explicit argument is the continuation statement — the TM1 statement that will be executed after all bits have been written.

### Conventions

When the list of bits is empty, `VTask.write` returns the continuation statement unchanged, writing nothing to the tape.

### Worked examples

- Claim: `VTask.write [] q = q` for any continuation `q`; writing an empty list leaves the program at the continuation immediately.

- Claim: `VTask.write [true, false] q` produces a two-step instruction sequence that writes `true` to the current cell, moves right, writes `false` to the next cell, moves right, and then runs `q`.

- Claim: `SupportsStmt S (VTask.write l q) = SupportsStmt S q` for any label set `S`, list `l`, and continuation `q`; the support of the written sequence equals the support of the continuation alone, since writing bits introduces no new label references.

- Claim: Executing `VTask.write (enc a).toList q` on a translated tape `trTape' enc0 L (ListBlank.cons b R)` with auxiliary state `v` is equivalent to executing `q` on the tape `trTape' enc0 (ListBlank.cons a L) R` with auxiliary state `v`; that is, writing the encoding of `a` advances the simulated tape head by one encoded-cell's worth of bits.

### Boundaries

- Empty list: `VTask.write [] q` is definitionally equal to `q`; no writes or moves are performed.
- Singleton list `[a]`: writes `a` to the current cell and moves right once, then continues with `q`.
- The function is total; it is defined for every list of `Bool`s and every continuation.
- The tape head is always left one position to the right of the last written cell upon completion (i.e., it moves right after each write, including the last one).

### Not to be confused with

- `Turing.TM1.Stmt.write`: the primitive single-cell write statement for a TM1 machine, which writes one symbol determined by a function of the current state and tape symbol — `VTask.write` sequences multiple such primitives.
- `Turing.TM0.Stmt`: the analogous statement type for TM0 machines, which operates at a lower level of abstraction.
- `Turing.TM1to1.trTape'`: the tape translation function used to encode multi-symbol tapes as binary tapes; `VTask.write` is the *instruction-level* counterpart that writes encoded data, not the tape transformation itself.