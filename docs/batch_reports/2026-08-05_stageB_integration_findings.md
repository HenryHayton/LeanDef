# Stage B integration findings (2026-08-05)

Material for the eventual Stage F write-up. Every item here was found by *integration*, not by
unit tests — each is an argument for the smoke-before-box discipline.

## The declaration-vs-body contract violation

A latent **cross-stage contract violation** that only integration could catch. Two stages held
incompatible conventions for what a candidate *is*:

- `authoring/prompts/round_trip.txt`: *"Respond with ONLY the Lean term/expression that fills
  the hole in `def <name> : <type> := <body>`"* — a **body**.
- `prelim/prompts.py` (Stage 2): *"Your answer must be a complete Lean 4 declaration that begins
  with `def VTask.clog`"* — a **declaration**.

Stage B's scorer inherited the authoring convention, so `PinnedSignature.splice(body)` produced
`def VTask.clog : T := noncomputable def VTask.clog …`. **1040 of 1040** extractable field
candidates are declarations, so every single one would have been recorded `COMPILE_ERROR`.

Neither stage was wrong in isolation and neither stage's tests could see it: the mismatch lived
in the *seam*. Unit tests on either side pass with either convention. Only running real
candidates through the real scorer surfaced it — on the first smoke, at a cost of minutes, on a
laptop. Had it reached the box it would have produced a complete, plausible, entirely worthless
run: every candidate inadmissible, no crash, no error, a funnel that looked merely pessimistic.

**Resolution** (a design improvement, not a workaround): splice the candidate's declaration
verbatim with `@[reducible]` merged in, and enforce the pinned type by *kernel* check
(`#check (VTask.x : <pinned type>)`) rather than by construction. Strictly stronger than the old
guarantee — it accepts a defeq-but-differently-phrased signature the constructor could never
express — and it removes the fragile declaration→body parse that would have mis-handled implicit
and instance binders, equation-style definitions and `where` clauses, each a fresh source of
differential-by-output-style false negatives.

## Two more the same smoke caught

**The type probe's form matters.** `example : T := VTask.clog` additionally *compiles* the
definition and therefore fails every noncomputable candidate with "consider marking it as
'noncomputable'". Using it would have produced systematic false `WRONG_TYPE` against exactly the
classical-construction population. `#check (VTask.clog : T)` only elaborates, and still catches
wrong arity and wrong result type. Both verified against live Lean.

**A stuck `Decidable` instance is not broken machinery.** A noncomputable candidate (`sInf`,
`Classical.propDecidable`) type-checks and *has* a `Decidable` instance, but the instance cannot
evaluate: Lean says ``did not reduce to `isTrue` or `isFalse` ``. That was landing in tier 1's
ERRORED default — mis-reported as infrastructure failure and burning a wasted retry on each of
14 facts for a single candidate. It is semantically identical to a missing instance: untestable
through this splice, no evidence about the proposition. Now UNKNOWN.

## An interpretation hazard for Stage F

The smoke produced candidates with `fidelity = 1.0` computed over **9 resolved facts out of 29**,
the other 20 being UNKNOWN because the candidate is noncomputable and its decide facts cannot
evaluate. That is *correct* under the scoring rule (UNKNOWN is excluded from the denominator),
but 1.0-from-9-of-29 is plainly not the same evidence as 1.0-from-29-of-29.

Fidelity therefore needs a companion **resolution rate** (`resolved / total`) reported beside it,
and the pre-registration should say how low-resolution candidates are treated. Without that, the
headline metric systematically flatters noncomputable formulations — a differential-by-style
effect of exactly the kind this project keeps having to hunt down.
