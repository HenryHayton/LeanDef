"""Guards the worked JSON examples embedded in `authoring/prompts/*.txt` against drifting out
of sync with the real parser (`authoring.parse`) that a model's imitation of them will face.

Direct regression for the real 2026-07-28 incident: `fact_proposal.txt`'s membership worked
example silently omitted a field the parser (at the time) required, the model copied the
example faithfully, and the resulting task rotated at `fact_proposal` -- burning a full task's
worth of real Bedrock spend before anyone noticed the example itself was wrong. Models copy
concrete examples over abstract prose (see `authoring/prompts/fact_proposal.txt`'s membership
bullet's own note); a wrong example is therefore load-bearing in a way prose typos aren't. This
module extracts every such example the prompt sends and proves each one survives the real
parsing path, so a future edit that reintroduces a bad example fails a test instead of a task.

Only `fact_proposal.txt` currently carries genuine, concrete, standalone-parseable examples --
`classification.txt`/`dossier.txt` show schema-shaped ENVELOPES with placeholder tokens (e.g.
`<integer 1-5>`, `"..."`) that are illustrations of shape, not literal data meant to parse, and
`round_trip.txt`'s output is raw Lean text, not JSON. The extraction below is deliberately
general (any `Example <label> fact: `{...}`` marker, in any prompt file) so it picks up future
examples without needing a rewrite -- it just has nothing else to find right now."""

import json

import pytest

from authoring.parse import parse_facts
from authoring.prompt_loader import PROMPTS_DIR, load_prompt_template

# Every prompt this project currently has, with the placeholder values needed to render it (the
# exact set `.render()` requires -- see each template's own USER section).
_RENDER_INPUTS = {
    "classification": dict(pinned_signature="X : Nat", definition_source="def X := 0", docstring="d", mention_sidecar_excerpt="(none)"),
    "dossier": dict(pinned_signature="X : Nat", definition_source="def X := 0", docstring="d", mention_sidecar_excerpt="(none)", classification="c"),
    "fact_proposal": dict(pinned_signature="X : Nat", dossier_md="# Object\n...", mention_sidecar_excerpt="(none)", classification="c"),
    "round_trip": dict(pinned_signature="X : Nat", dossier_md="# Object\n..."),
}


def _extract_json_examples(text: str) -> list[tuple[str, str]]:
    """Find every `Example <label> fact: `{...}`` marker and return `(label, json_text)`,
    using bracket-depth scanning (not a naive regex) since the JSON objects themselves contain
    nested `{...}` (e.g. `domain_inputs`), which a non-greedy regex would truncate at the first
    inner `}`."""
    results = []
    marker = "fact:"
    search_start = 0
    while True:
        marker_idx = text.find(marker, search_start)
        if marker_idx == -1:
            break
        # Walk backward from the marker to find the label word right before " fact:".
        before = text[:marker_idx].rstrip()
        label = before.split()[-1] if before.split() else ""
        # Find the opening backtick-delimited `{` after the marker.
        tick_start = text.find("`{", marker_idx)
        newline = text.find("\n\n", marker_idx)
        if tick_start == -1 or (newline != -1 and tick_start > newline):
            search_start = marker_idx + len(marker)
            continue
        brace_start = tick_start + 1
        depth = 0
        i = brace_start
        while i < len(text):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    i += 1
                    break
            i += 1
        json_text = text[brace_start:i]
        if text[i:i + 1] == "`":
            results.append((label, json_text))
        search_start = i
    return results


def _rendered_system_prompt(name: str) -> str:
    template = load_prompt_template(name)
    system, _ = template.render(**_RENDER_INPUTS[name])
    return system


@pytest.mark.parametrize("prompt_name", sorted(p.stem for p in PROMPTS_DIR.glob("*.txt")))
def test_every_prompt_renders_cleanly(prompt_name):
    """Baseline: every prompt template must render with real inputs -- catches the exact
    unescaped-brace bug (2026-07-28) that would otherwise only surface as a `str.format()`
    crash the first time a real call used it."""
    _rendered_system_prompt(prompt_name)  # must not raise


def test_fact_proposal_prompt_has_exactly_one_example_per_fact_type():
    examples = _extract_json_examples(_rendered_system_prompt("fact_proposal"))
    labels = [label for label, _ in examples]
    assert set(labels) == {"casework", "membership", "global"}, (
        f"expected exactly one worked example per fact type, found labels: {labels}"
    )


@pytest.mark.parametrize("fact_type", ["casework", "membership", "global"])
def test_fact_proposal_prompt_example_parses_clean(fact_type):
    examples = dict(_extract_json_examples(_rendered_system_prompt("fact_proposal")))
    assert fact_type in examples, f"no worked example found for fact type {fact_type!r}"

    entry = json.loads(examples[fact_type])  # must be valid, complete JSON on its own
    assert entry.get("type") == fact_type, (
        f"example labeled {fact_type!r} has 'type': {entry.get('type')!r} -- label/content mismatch"
    )

    facts, rejections = parse_facts(json.dumps([entry]))
    assert rejections == [], (
        f"the prompt's own {fact_type} worked example was REJECTED by the real parser -- a "
        f"model imitating it would fail the same way: {rejections}"
    )
    assert len(facts) == 1
