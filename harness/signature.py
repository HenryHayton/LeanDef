"""The pinned signature a candidate's body fills in.

Split into its own module (rather than living in `harness.scoring`) so both
`harness.scoring` and `harness.admissibility` can depend on it without a circular import.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PinnedSignature:
    """A task's pinned definition name and type -- the hole a candidate body fills.

    Previously (`archive/n1_tau/score.py`) the name and type were retyped as a literal
    substring inside every one of 9 candidate strings; see `docs/repo_audit.md` §3 ("Pinned
    signature representation") and observation 5.
    """

    name: str
    type_sig: str

    def splice(self, body: str) -> str:
        """Render `@[reducible] def <name> : <type> := <body>` for a well-formed, single-
        declaration candidate. For a candidate that needs to be more than one declaration
        (helper lemmas -- or, deliberately, for admissibility-gate testing, adversarial extra
        declarations), build the raw command text directly instead of using this helper.

        `@[reducible]` (2026-07-30, `docs/design/llm_io_contract_v1.md` §4.4): Lean's
        typeclass search only unfolds `@[reducible]`-marked definitions, not plain `def`s. A
        plain-`def` task-symbol splice is therefore opaque to instance search -- confirmed the
        hard way against a real gate task (`Nat.ModEq`): `Nat.ModEq`'s own `Decidable` instance
        is keyed to `Nat.ModEq`'s head symbol (`Mathlib/Data/Nat/ModEq.lean`), so
        `Decidable (VTask.ModEq n a b)` failed to synthesize under a plain-`def` splice even
        though the underlying proposition is genuinely decidable. `@[reducible]` (chosen over
        `abbrev`, which is strictly more than needed here -- `abbrev` also marks `@[inline]`
        and widens unification-default transparency beyond typeclass search, neither of which
        this fix requires) is the minimal attribute that makes instance search see through the
        splice. Applies uniformly to every splice this method produces -- truth-splice
        (`authoring.pipeline`) and candidate splice (`authoring.roundtrip`, and
        `harness.scoring.score_candidate`'s future real-candidate path) both call this single
        method, so both are covered by one change; there is no separate "candidate normalizes
        its own attribute" step because a candidate never writes this line itself, the harness
        always does. Confirmed NOT to change outcomes on the value-typed path (`Nat.clog`):
        decidable-equality facts on a value-typed definition's OUTPUT resolve via a generic
        instance on the output's own type (e.g. `Nat.decEq`), never needing to unfold the
        definition's own name for instance search, so reducibility was never the blocker there
        -- see the regression tests this change shipped with."""
        return f"@[reducible] def {self.name} : {self.type_sig} := {body}"

    def splice_real_name(self, real_name: str, *, noncomputable: bool = False) -> str:
        """The TRUTH-splice specifically: alias an EXISTING Mathlib declaration (`real_name`)
        under this pinned signature -- as opposed to `splice`, which takes an arbitrary
        candidate body expression (a round-trip attempt, a real candidate). Two things `splice`
        alone gets wrong for this specific case, both confirmed empirically (2026-07-31, the
        "Harness Fixes" session, against the 41-name batch's real `truth_splice` casualties):

        1. **Root-qualification.** `real_name` is passed bare (e.g. `Monotone`, not
           `_root_.Monotone`) whenever the real declaration lives at the top level with no
           namespace prefix. `def VTask.Monotone := Monotone` then fails Lean's termination
           checker with a baffling "well-founded recursion cannot be used" error -- not because
           of any real recursion, but because Lean's name resolution for the bare `Monotone` in
           the body matches the CURRENTLY-BEING-ELABORATED `VTask.Monotone` (both end in
           `.Monotone`) instead of the real top-level one, producing a bogus self-referential
           definition. Confirmed via a 4-name x 3-attribute-variant repro matrix that this has
           nothing to do with `@[reducible]`/`abbrev` (identical failure under plain `def` too)
           and via direct isolation that root-qualifying (`_root_.Monotone`) or renaming the
           task symbol's own base name each independently fix it, while leaving every
           already-working name (`Nat.clog`, `Nat.ModEq`, ...) unaffected -- `_root_.` is always
           safe to prepend, so it is applied unconditionally here, not just for no-dot names.
        2. **Noncomputability.** Some real declarations are noncomputable at an ALIAS site even
           though their own source line carries no explicit `noncomputable` keyword (confirmed:
           `Function.extend`'s body is `open scoped Classical in if h : ... then ... else ...`,
           which Mathlib's own declaration is permitted to elaborate without the keyword, but a
           downstream `def X := Function.extend` is not). This is NOT reliably detectable from
           source text -- `miner.scan`'s own text-scan for a literal `noncomputable` prefix
           would (and did, when checked directly against the real source line) miss this exact
           case -- so `noncomputable` is a caller-supplied flag, discovered by trying without it
           first and retrying with it on Lean's own specific compiler error
           (`authoring.pipeline`'s truth-splice call site owns that retry; this method only
           knows how to render the modifier when told to)."""
        modifier = "noncomputable " if noncomputable else ""
        return f"@[reducible] {modifier}def {self.name} : {self.type_sig} := _root_.{real_name}"
