## Object

`VTask.trCont` is the forgetful translation of a high-level *continuation* value (`Turing.ToPartrec.Cont`) into its corresponding low-level *continuation label* (`Turing.PartrecToTM2.Cont'`). The high-level `Cont` type describes what to do after a partial-recursive computation step completes, carrying both the structural shape of the remaining computation *and* the intermediate data values (argument lists, functions) needed by that step. The low-level `Cont'` type retains only the structural shape — the *kind* of continuation and any still-unevaluated code fragments — while the intermediate data values are elided. Those elided values are separately encoded on a stack component of the Turing-machine configuration by `trContStack`. Together, `VTask.trCont` and `trContStack` form a bisimulation between the two levels of the compilation chain.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.trCont : Turing.ToPartrec.Cont → Turing.PartrecToTM2.Cont'
<!-- PINNED-SIGNATURE:END -->


`VTask.trCont : Turing.ToPartrec.Cont → Turing.PartrecToTM2.Cont'`

The sole argument is a continuation in the high-level partial-recursive computation model, describing the pending work after the current sub-computation finishes (possibly `halt`, or one of the structured continuation forms for cons-building, composition, and fixed-point). The result is the corresponding low-level continuation label, keeping only the structural skeleton and discarding all intermediate data payloads.

## Conventions

The function is total and defined on all five constructors of `Cont`; there are no junk values and no undefined cases.

## Worked examples

- Claim: `VTask.trCont Turing.ToPartrec.Cont.halt = Turing.PartrecToTM2.Cont'.halt`

- Claim: For any code `c`, value list `vs`, and continuation `k`, `VTask.trCont (Turing.ToPartrec.Cont.cons₁ c vs k) = Turing.PartrecToTM2.Cont'.cons₁ c (VTask.trCont k)` — the intermediate list `vs` is dropped and only the code fragment `c` and the translated tail continuation are kept.

- Claim: For any value list `vs` and continuation `k`, `VTask.trCont (Turing.ToPartrec.Cont.cons₂ vs k) = Turing.PartrecToTM2.Cont'.cons₂ (VTask.trCont k)` — the accumulated first-component list `vs` is dropped entirely.

- Claim: For any code `c` and continuation `k`, `VTask.trCont (Turing.ToPartrec.Cont.fix c k) = Turing.PartrecToTM2.Cont'.fix c (VTask.trCont k)` — the fixed-point code `c` is preserved and the tail continuation is translated recursively.

## Boundaries

- The `halt` case is the base case of the recursion; it maps to `Cont'.halt` with no sub-continuations to translate.
- For all four recursive constructors (`cons₁`, `cons₂`, `comp`, `fix`), the translation proceeds recursively on the tail continuation `k`, so the depth of the output mirrors the depth of the input.
- The dropped data (intermediate value lists) is not lost from the global simulation; it reappears in the `trContStack` component of the Turing-machine configuration, maintaining the invariant used in the bisimulation theorems `tr_ret_respects` and `trNormal_respects`.
- The function is structurally recursive and terminates on all inputs.

## Not to be confused with

- `trContStack`: the companion function that extracts precisely the data *dropped* by `VTask.trCont` and encodes it as a flat list on the Turing-machine stack; `VTask.trCont` and `trContStack` are complementary, not duplicates.
- `trNormal`: the translation of a *code* term (rather than a continuation), which maps `Code` values and a `Cont` to a `Λ'` (low-level machine state label); it calls `VTask.trCont` internally.
- `Turing.PartrecToTM2.Cont'` itself: the *target type* of the translation, a structurally similar but data-free version of `Cont`; confusing the type with the translation function is a common source of error.