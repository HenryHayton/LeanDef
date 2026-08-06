"""The eight-cell design: anti-sorry instruction (4 levels) x reasoning scaffold (2 levels).

One model (Goedel-Formalizer-V2-8B), 41 tasks, 10 samples, temperature 0.7 only. Temperature is
held fixed deliberately: this compares PROMPTS, and a sampling split would spend half the run
re-measuring something the prelim already measured.

**The two anti-sorry theories being separated.** `S_B` and `S_C` are not two phrasings of one
idea -- they encode different explanations of why an autoformalizer punts:

- `S_B` (commit-under-uncertainty) assumes the model punts because it is *uncertain* and treats
  `sorry` as the safe move. It changes the decision norm: an incomplete answer scores zero, so
  committing dominates hedging.
- `S_C` (role/norm reframe) assumes the model punts because of a *format prior* -- it was trained
  where `sorry` is the correct output and a downstream prover fills the body. It changes the
  role: there is no downstream prover.

The prelim evidence favours `S_C`: the model stopped at ~700 of 8192 tokens with competent
reasoning in its `<think>` block and emitted miniF2F boilerplate (`set_option maxHeartbeats 0`),
which looks like a convention being followed rather than uncertainty being hedged. If `S_B` and
`S_C` separate cleanly, that distinction is a finding in its own right; `S_A` (plain prohibition)
is the control that says whether either theory was needed at all.
"""

from dataclasses import dataclass

S0 = "S0"
S_A = "S-A"
S_B = "S-B"
S_C = "S-C"
R0 = "R0"
R1 = "R1"

ANTI_SORRY: dict[str, str] = {
    S0: "",
    S_B: (
        "If you are unsure between constructions, commit to the one you believe most likely "
        "correct. A complete definition with a possible flaw is always preferred to an "
        "incomplete one; incomplete answers score zero."
    ),
    S_C: (
        "You are writing the definition itself, not a statement for a prover to fill in later. "
        "There is no downstream prover: anything left unwritten or unproven is simply wrong. "
        "`sorry` is never an acceptable output."
    ),
    S_A: (
        "Your output must be a complete definition. `sorry`, `admit`, and placeholder terms are "
        "not permitted anywhere in your answer."
    ),
}

# R0 carries NO instruction on this axis -- not an empty-ish nudge, genuinely nothing. Whatever
# structure the model then chooses is itself data: it reveals the native prior for this task.
SCAFFOLD: dict[str, str] = {
    R0: "",
    R1: (
        "Before writing the Lean definition, write a brief prose characterization of the object: "
        "what it is mathematically, and how it behaves at its edge or boundary cases. Then write "
        "the definition. The prose is not graded; only the definition is."
    ),
}


@dataclass(frozen=True)
class Cell:
    sorry_level: str
    scaffold: str

    @property
    def cell_id(self) -> str:
        return f"{self.sorry_level}_{self.scaffold}".replace("-", "")

    @property
    def anti_sorry_text(self) -> str:
        return ANTI_SORRY[self.sorry_level]

    @property
    def scaffold_text(self) -> str:
        return SCAFFOLD[self.scaffold]

    @property
    def uses_prose_exemplars(self) -> bool:
        """R1 cells show the exemplars WITH their prose blocks; R0 cells show the same three
        definitions without. Same exemplars either way -- only the demonstrated shape differs."""
        return self.scaffold == R1


# Run order: the six {S0, S-B, S-C} cells first, the two S-A cells last, so analysis of the
# theory-bearing cells can start while the plain-prohibition control is still generating.
CELLS: list[Cell] = [
    Cell(S0, R0), Cell(S0, R1),
    Cell(S_B, R0), Cell(S_B, R1),
    Cell(S_C, R0), Cell(S_C, R1),
    Cell(S_A, R0), Cell(S_A, R1),
]

CELL_IDS = [c.cell_id for c in CELLS]
