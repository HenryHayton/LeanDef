"""The first-3 gate: a cheap sanity check on a model's opening samples, so a broken prompt
template costs 3 generations instead of 410.

This is the single highest-value safety mechanism in prelim testing. The run is unattended and
overnight; the failure it protects against is not a model being *bad* (that is the measurement)
but our own wrapper being *wrong* for one model -- a chat template the server rejects, a system
prompt that makes the model answer in prose, a framing that makes it emit a theorem instead of a
definition. That failure looks identical to "this model is terrible" in the final numbers, which
is exactly why it must be caught while it is still cheap and obvious.

**Deliberately permissive.** The gate asks only whether output is *structurally plausible as
Lean*, never whether it is correct -- correctness is the whole experiment and must not be
pre-judged here. One extractable, `def`-and-`:=`-bearing, non-trivial sample out of three is
enough to pass. A model that produces two failures and one rough definition is a legitimate low
scorer whose run should proceed; a model that produces three unextractable blobs is far more
likely to be our bug than its incompetence.
"""

from dataclasses import dataclass, field

from prelim.extract import Extraction, extract_definition

# A definition shorter than this is a stub, not an answer -- `def f := 0` is 12 characters, and
# nothing meeting the pinned signatures in this corpus fits in 40.
MIN_DEFINITION_CHARS = 40

# How many opening samples the gate inspects, and how many must look plausible.
GATE_SAMPLE_COUNT = 3
GATE_MIN_PLAUSIBLE = 1


@dataclass(frozen=True)
class SampleVerdict:
    """Per-sample detail, so a failing gate report says exactly what each sample did."""

    index: int
    extracted: bool
    reason: str = ""          # extraction failure reason when `extracted` is False
    has_def: bool = False
    has_assign: bool = False
    length: int = 0
    plausible: bool = False


@dataclass(frozen=True)
class GateResult:
    model_slug: str
    passed: bool
    n_checked: int
    n_plausible: int
    verdicts: list[SampleVerdict] = field(default_factory=list)
    summary: str = ""

    def report_lines(self) -> list[str]:
        """Human-facing lines for the driver to log loudly on failure."""
        head = (
            f"[gate] {self.model_slug}: {'PASS' if self.passed else 'FAIL'} "
            f"({self.n_plausible}/{self.n_checked} plausible) -- {self.summary}"
        )
        return [head] + [
            f"    sample {v.index}: extracted={v.extracted} def={v.has_def} ':='={v.has_assign} "
            f"len={v.length}{'' if v.extracted else f' reason={v.reason}'}"
            for v in self.verdicts
        ]


def check_early_samples(
    model_slug: str,
    samples: list[tuple[str, str | None]],
    *,
    min_chars: int = MIN_DEFINITION_CHARS,
    min_plausible: int = GATE_MIN_PLAUSIBLE,
) -> GateResult:
    """Judge a model's opening samples.

    `samples` is `[(completion_text, finish_reason), ...]` -- the driver passes the first
    `GATE_SAMPLE_COUNT` it has. Fewer is allowed (a model whose first sample already errored out
    should still be judgeable), and an empty list FAILS: no evidence of working output is not the
    same as evidence of working output, and proceeding to 410 samples on no evidence is the
    precise mistake this gate exists to prevent.
    """
    verdicts: list[SampleVerdict] = []
    for i, (text, finish_reason) in enumerate(samples):
        result = extract_definition(model_slug, text, finish_reason=finish_reason)
        if isinstance(result, Extraction):
            code = result.code
            has_def = "def" in code
            has_assign = ":=" in code
            length = len(code.strip())
            verdicts.append(
                SampleVerdict(
                    index=i, extracted=True, has_def=has_def, has_assign=has_assign, length=length,
                    plausible=has_def and has_assign and length > min_chars,
                )
            )
        else:
            verdicts.append(SampleVerdict(index=i, extracted=False, reason=result.reason))

    n_plausible = sum(1 for v in verdicts if v.plausible)
    passed = bool(verdicts) and n_plausible >= min_plausible

    if not verdicts:
        summary = "no samples supplied -- cannot establish that the template works at all"
    elif passed:
        summary = "output is structurally plausible as Lean; proceeding"
    else:
        reasons = sorted({v.reason for v in verdicts if v.reason})
        detail = f" (extraction reasons: {', '.join(reasons)})" if reasons else ""
        summary = (
            f"no sample produced a plausible definition{detail} -- suspect this model's prompt "
            f"template or endpoint style before concluding anything about the model"
        )

    return GateResult(
        model_slug=model_slug, passed=passed, n_checked=len(verdicts),
        n_plausible=n_plausible, verdicts=verdicts, summary=summary,
    )
