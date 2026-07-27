"""Loads and renders the versioned prompt template files under `authoring/prompts/` (contract
§8 item 3: "prompt templates as versioned files ... each carrying its input-assembly spec as
comments").

File format, by convention (not enforced by any external tool -- these are plain text files,
not a templating library's native format): a leading `#`-comment block (the input-assembly
spec, human-facing only) up to a `===SYSTEM===` marker, then the system prompt template up to
a `===USER===` marker, then the user prompt template to end of file. Both templates use plain
`str.format()` placeholders (`{name}`) -- no external templating dependency, matching this
project's "no heavyweight deps" constraint (CLAUDE.md "Constraints").
"""

from dataclasses import dataclass
from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"

_SYSTEM_MARKER = "===SYSTEM==="
_USER_MARKER = "===USER==="


class PromptTemplateError(ValueError):
    """A prompt template file under `authoring/prompts/` is missing its `===SYSTEM===`/
    `===USER===` markers, or a `render()` call is missing a placeholder the template needs."""


@dataclass(frozen=True)
class PromptTemplate:
    name: str
    system_template: str
    user_template: str

    def render(self, **inputs: str) -> tuple[str, str]:
        """Returns `(system, user)`, both fully substituted. Raises `PromptTemplateError`
        (wrapping the original `KeyError`) if a placeholder in the template has no matching
        keyword -- fails loudly rather than shipping a prompt with a literal `{missing_field}`
        in it."""
        try:
            system = self.system_template.format(**inputs)
            user = self.user_template.format(**inputs)
        except KeyError as e:
            raise PromptTemplateError(
                f"prompt template {self.name!r}: missing input {e} for rendering"
            ) from e
        return system, user


def load_prompt_template(name: str, *, prompts_dir: Path | None = None) -> PromptTemplate:
    """Load `<prompts_dir>/<name>.txt` and split it into system/user templates. `name` is one
    of `"classification" | "dossier" | "fact_proposal" | "round_trip"` (the four contract
    calls), but this function does not hardcode that set -- any correctly-shaped file works,
    so a fifth call added later needs no change here."""
    prompts_dir = prompts_dir if prompts_dir is not None else PROMPTS_DIR
    path = prompts_dir / f"{name}.txt"
    text = path.read_text(encoding="utf-8")

    if _SYSTEM_MARKER not in text or _USER_MARKER not in text:
        raise PromptTemplateError(f"{path}: missing {_SYSTEM_MARKER!r}/{_USER_MARKER!r} markers")

    _header, _, rest = text.partition(_SYSTEM_MARKER)
    system_part, _, user_part = rest.partition(_USER_MARKER)
    return PromptTemplate(name=name, system_template=system_part.strip("\n"), user_template=user_part.strip("\n"))
