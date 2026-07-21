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
        """Render `def <name> : <type> := <body>` for a well-formed, single-declaration
        candidate. For a candidate that needs to be more than one declaration (helper
        lemmas -- or, deliberately, for admissibility-gate testing, adversarial extra
        declarations), build the raw command text directly instead of using this helper."""
        return f"def {self.name} : {self.type_sig} := {body}"
