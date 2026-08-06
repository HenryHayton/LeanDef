"""The decode-and-exemplar battery: two independent interventions, one composition check.

Everything here holds the PROMPT axis fixed at `S-A_R0` -- plain prohibition, no reasoning
scaffold. That is not an arbitrary default. The eight-cell run measured S-A_R0 as the quality
winner on conditional admissibility (40.5% of non-punting attempts admissible, against 33.7% for
the instruction-free control), and measured every R1 cell as worse than its R0 twin on both
metrics while producing FEWER tokens -- prose displacing reasoning rather than adding to it. R1 is
dead; re-testing it here would spend half the session re-deriving a finding we already hold.

**Battery T -- decode interventions**, exemplars held at the eight-cell run's three-plain block:

    T0  control, no intervention        the paired baseline
    T1  ban                             `sorry`/`admit` unsayable at decode time
    T2  prefill                         completion forced to start mid-declaration
    T3  ban + prefill                   both

T0 exists even though last week's SA_R0 numbers are in hand. $0.25 buys immunity to every
cross-run drift argument -- different pod, different GPU, a vLLM point release -- that would
otherwise sit unanswerable underneath a 2-3 point T3 effect.

**Battery A -- exemplar fixes**, no decode intervention:

    A1  zero exemplars                  the floor
    A2  three exemplars, reframed       full dose, salience fixed
    A3  one exemplar, reframed          dose-response against A2

A1 separates the two things the exemplar block was doing at once: it cut compile errors by 9.1
points AND supplied a fallback answer that raised `name_shadowed` by 12.8, netting slightly
NEGATIVE on admission (23.2% -> 21.5%). Without a zero-exemplar floor there is no way to say
which half of that the instruction stack was already delivering on its own.

A2 and A3 encode different causes for the same defect. A2 says the model could not tell example
from task (a salience failure) and fixes framing and structure. A3 says three full worked examples
crowd the task out of an 8B model's attention (a budget failure) and cuts the dose. If A3 beats
A2, the cause is budget; if they tie, reframing alone was sufficient and the third exemplar is
free.

**C1 is deliberately not defined here.** It is the winners composed, and the winners are not known
until T and A are scored -- writing a guess into the source now would invite reading the guess as
the plan. `compose` builds it once the results exist.

Read on T: admissible/100 and non-verbatim admissible, with the bucket table as mechanism.
Read on A: substitution rate FIRST -- a fix that does not kill contamination fails regardless of
what else it moves -- then admissible/100 and reach.
"""

from dataclasses import dataclass

from pretuning.cells import R0, S_A, Cell
from pretuning.prompts import ONE_REFRAMED, THREE_PLAIN, THREE_REFRAMED, ZERO

# The prompt axis, fixed for the whole battery. See the module docstring.
BASE_CELL = Cell(S_A, R0)


@dataclass(frozen=True)
class BatteryCell:
    """One cell. Presents the same surface as `Cell` so `pretuning.driver` needs no cell-type
    branch, and adds the three axes this battery varies."""

    cell_id: str
    battery: str            # "T" | "A" | "C"
    exemplar_mode: str
    ban: bool
    prefill: bool
    rationale: str

    # --- the `Cell` surface, delegated to the fixed prompt base ------------------------------
    @property
    def sorry_level(self) -> str:
        return BASE_CELL.sorry_level

    @property
    def scaffold(self) -> str:
        return BASE_CELL.scaffold

    @property
    def anti_sorry_text(self) -> str:
        return BASE_CELL.anti_sorry_text

    @property
    def scaffold_text(self) -> str:
        return BASE_CELL.scaffold_text

    @property
    def uses_prose_exemplars(self) -> bool:
        return BASE_CELL.uses_prose_exemplars

    @property
    def n_exemplars(self) -> int:
        return {ZERO: 0, ONE_REFRAMED: 1, THREE_PLAIN: 3, THREE_REFRAMED: 3}[self.exemplar_mode]


T_CELLS: list[BatteryCell] = [
    BatteryCell("T0", "T", THREE_PLAIN, ban=False, prefill=False,
                rationale="paired in-session baseline; kills cross-run drift arguments"),
    BatteryCell("T1", "T", THREE_PLAIN, ban=True, prefill=False,
                rationale="is the punt a decode-time format prior rather than a choice?"),
    BatteryCell("T2", "T", THREE_PLAIN, ban=False, prefill=True,
                rationale="starting mid-declaration removes the moment where the punt is chosen"),
    BatteryCell("T3", "T", THREE_PLAIN, ban=True, prefill=True,
                rationale="both, in case each alone leaves a route open"),
]

A_CELLS: list[BatteryCell] = [
    BatteryCell("A1", "A", ZERO, ban=False, prefill=False,
                rationale="the floor: how much of the -9.1pt compile-error gain is the exemplars?"),
    BatteryCell("A2", "A", THREE_REFRAMED, ban=False, prefill=False,
                rationale="full dose, salience fixed by framing plus structural separation"),
    BatteryCell("A3", "A", ONE_REFRAMED, ban=False, prefill=False,
                rationale="dose-response: beats A2 iff contamination is attention-budget-driven"),
]

BATTERY_CELLS: list[BatteryCell] = T_CELLS + A_CELLS
CELL_BY_ID = {c.cell_id: c for c in BATTERY_CELLS}


def compose(t_winner: str, a_winner: str, *, cell_id: str = "C1") -> BatteryCell:
    """The composition cell: T-winner's decode intervention with A-winner's exemplar treatment.

    Run last and alone. Its job is to catch a bad interaction -- a prefill that makes the reframed
    separation unreachable because generation starts past it, say -- before anything is frozen. If
    C1 materially underperforms either winner, the finding is reported and nothing freezes.
    """
    t, a = CELL_BY_ID[t_winner], CELL_BY_ID[a_winner]
    if t.battery != "T" or a.battery != "A":
        raise ValueError(f"compose expects a T cell and an A cell, got {t_winner!r} and {a_winner!r}")
    return BatteryCell(
        cell_id=cell_id, battery="C", exemplar_mode=a.exemplar_mode,
        ban=t.ban, prefill=t.prefill,
        rationale=f"composition of {t_winner} (decode) and {a_winner} (exemplars)",
    )
