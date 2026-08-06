"""Decode-time interventions: the `sorry`/`admit` token ban, and the assistant prefill.

Both attack the same finding by a different route than prompting did. The eight-cell experiment
established that the punt rate is not prompt-addressable -- four instruction strengths x two
scaffolds all came out at or above the instruction-free control, and think-block analysis showed
the instruction never entered deliberation at all (mention rate ~47% with and without it). If the
behaviour is a decoding-time format prior rather than a considered choice, then decoding-time is
where it can be reached.

**The ban is not a fix and must not be read as one.** Making `sorry` unsayable does not make the
model able to write the definition; it forces it to route around the token. The routes are
enumerated in `pretuning.buckets`, pre-named before the run, precisely so that "T1 cut the sorry
rate to zero" cannot be reported as a win when what actually happened is that the punt moved to
`by exact?`. The measurement that matters is admissibility, with the bucket table as mechanism.

**Token IDs are resolved from the served tokenizer, never guessed.** vLLM's `bad_words` takes
strings and tokenizes them itself, so passing strings is the correct wire form -- but a variant
that tokenizes differently than assumed would be a silent no-op, and a run whose central
intervention silently did nothing is the expensive failure mode here. `resolve_bad_words` asks
the server's own `/tokenize` endpoint for every variant and returns the id sequences for the run
log.

One mechanic worth stating because it changes what the variant list has to cover: vLLM bans the
LAST token of each tokenized sequence, conditioned on the preceding tokens having just been
emitted. A single-token variant is therefore banned unconditionally; a multi-token variant is
banned only in that exact context. Enumerating leading-space, newline and `:=`-merged forms is
not belt-and-braces -- those are genuinely different first tokens, and a ban on the bare form
does not touch them.
"""

import json
from dataclasses import dataclass
from urllib.parse import urlsplit, urlunsplit

import requests

from harness.signature import PinnedSignature

# The families. `sorryAx` is the constant `sorry` elaborates to -- a model that has seen Lean
# source can write it directly. `admit` is the tactic alias; `stop`/`trivial` are NOT banned, as
# they are legitimate in bodies we would want to score.
BASE_WORDS: tuple[str, ...] = ("sorry", "sorryAx", "admit")

# Context prefixes. Each produces a different first token under a BPE tokenizer, so each has to
# be enumerated separately -- see the module docstring.
_PREFIXES: tuple[str, ...] = ("", " ", "\n", "\n  ", ":= ", ":=", ".", "by ", " by ")


def ban_variants(base_words: tuple[str, ...] = BASE_WORDS) -> list[str]:
    """Every (prefix, word) spelling to hand to vLLM's `bad_words`, de-duplicated, stable order."""
    seen: dict[str, None] = {}
    for word in base_words:
        for prefix in _PREFIXES:
            seen.setdefault(prefix + word, None)
    return list(seen)


@dataclass(frozen=True)
class TokenizedVariant:
    variant: str
    token_ids: list[int]

    @property
    def unconditional(self) -> bool:
        """A single-token variant is banned outright; a multi-token one only in its own context."""
        return len(self.token_ids) == 1

    def log_line(self) -> str:
        kind = "unconditional" if self.unconditional else f"conditional on {self.token_ids[:-1]}"
        return f"  {self.variant!r:<16} -> {self.token_ids}  ({kind})"


def _tokenize_url(endpoint_url: str) -> list[str]:
    """Candidate `/tokenize` URLs for the server behind a chat-completions URL.

    vLLM mounts `/tokenize` at the application root, not under `/v1`, but deployments differ in
    how much path prefix a proxy adds -- so both are tried rather than assumed.
    """
    parts = urlsplit(endpoint_url)
    path = parts.path
    for suffix in ("/v1/chat/completions", "/chat/completions", "/v1/completions", "/completions"):
        if path.endswith(suffix):
            path = path[: -len(suffix)]
            break
    root = path.rstrip("/")
    return [urlunsplit(parts._replace(path=f"{root}{p}", query="", fragment=""))
            for p in ("/tokenize", "/v1/tokenize")]


def resolve_bad_words(
    endpoint_url: str,
    model_name: str,
    *,
    variants: list[str] | None = None,
    api_key: str | None = None,
    timeout_s: float = 30.0,
) -> list[TokenizedVariant]:
    """Ask the SERVED tokenizer for the id sequence of each ban variant.

    Raises rather than falling back to a guess: a run whose ban silently covered nothing is worse
    than a run that refused to start.
    """
    variants = variants if variants is not None else ban_variants()
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    urls = _tokenize_url(endpoint_url)
    last_error = ""
    for url in urls:
        out: list[TokenizedVariant] = []
        try:
            for variant in variants:
                resp = requests.post(
                    url,
                    json={"model": model_name, "prompt": variant, "add_special_tokens": False},
                    headers=headers, timeout=timeout_s,
                )
                if resp.status_code != 200:
                    last_error = f"{url} -> HTTP {resp.status_code}: {resp.text[:200]}"
                    break
                ids = (resp.json() or {}).get("tokens")
                if not isinstance(ids, list) or not ids:
                    last_error = f"{url} -> no token ids for {variant!r}: {resp.text[:200]}"
                    break
                out.append(TokenizedVariant(variant=variant, token_ids=[int(i) for i in ids]))
            else:
                return out
        except requests.RequestException as e:
            last_error = f"{url} -> {type(e).__name__}: {e}"
    raise RuntimeError(
        f"could not resolve ban-variant token ids from the served tokenizer; tried {urls}. "
        f"Last error: {last_error}"
    )


def bad_words_body(variants: list[str]) -> dict:
    """The vLLM request field. Strings, not ids: vLLM tokenizes them with the served tokenizer,
    which is the same resolution `resolve_bad_words` reports -- so the log and the wire agree."""
    return {"bad_words": list(variants)}


def prefill_text(signature: PinnedSignature) -> str:
    """The spliced declaration header, up to and including `:=`.

    Built by `PinnedSignature.splice` with an empty body rather than by re-rendering the string
    here, so the prefill is byte-identical to what scoring would splice -- including the
    `@[reducible]` that typeclass resolution through the splice depends on. Retyping this format
    for a third time is exactly the duplication `PinnedSignature` exists to prevent.

    The trailing space is stripped deliberately: under a BPE tokenizer the model expects to emit
    the next word WITH its leading space as one token, and a prefill that ends mid-space forces a
    tokenization the model never saw in training.
    """
    return signature.splice("").rstrip()


def prefill_body(prefill: str) -> dict:
    """The vLLM request fields that make a trailing assistant message a prefix to continue.

    `continue_final_message` tells the server to append the assistant content raw, without the
    end-of-turn marker; `add_generation_prompt` must be false or the template opens a second
    assistant turn and the prefix becomes part of the conversation instead of the completion.
    """
    return {"continue_final_message": True, "add_generation_prompt": False}


def assemble_prefilled(prefill: str, continuation: str) -> str:
    """The model's answer as a single text, for every downstream consumer.

    The server returns only the CONTINUATION -- the prefix it was given back is not echoed. Every
    consumer downstream (the extractor, the admissibility scorer, the bucket classifier) is
    written against a complete declaration, so the prefix is re-attached here at the one boundary
    where it is known, rather than each of them learning that T2/T3 samples are shaped differently.
    """
    if not continuation:
        return prefill
    # No separator: the prefill ends at `:=` and the continuation carries its own leading space
    # if the tokenizer produced one.
    return prefill + continuation


def describe(bad_words: list[str] | None, prefill: str | None) -> str:
    parts = []
    parts.append(f"ban({len(bad_words)} variants)" if bad_words else "ban(off)")
    parts.append(f"prefill({len(prefill)} chars)" if prefill else "prefill(off)")
    return " ".join(parts)


def dump_resolution(resolved: list[TokenizedVariant]) -> str:
    return json.dumps([{"variant": t.variant, "token_ids": t.token_ids,
                        "unconditional": t.unconditional} for t in resolved], indent=1)
