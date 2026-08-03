"""The six candidate models for prelim testing, and the per-model etiquette each one expects.

**The fairness invariant.** Every model receives the same INFORMATION -- the task's dossier, the
pinned signature, and the instruction to write the definition. What differs between entries here
is only *dialect*: whether a system message is used, and how the request is framed in the words
that model's own card recommends. `prelim.prompts` builds the shared task block once and hands
the same string to every wrapper, so a per-model wrapper physically cannot add or remove task
content -- it can only decide what to say around it.

Every field below traces to the model's own HuggingFace card; the `card_url` and `card_notes` are
the record of what that card actually said (checked 2026-08-03), so a later reader can tell a
documented choice from a guess.

Sampling parameters are deliberately NOT taken from the cards. The cards' suggestions are tuned
for competition proof search (Kimina recommends temperature 0.6, Goedel demonstrates 32k tokens);
prelim testing needs one sampling regime applied identically to all six, or the comparison
measures the recommendation rather than the model. The chosen regime is a Stage 3 decision; the
card values are recorded here as `card_sampling` for that decision to reference.
"""

from dataclasses import dataclass, field

CHAT = "chat"  # POST /v1/chat/completions with a messages list
COMPLETION = "completion"  # POST /v1/completions with a single prompt string


@dataclass(frozen=True)
class ModelSpec:
    slug: str
    hf_name: str
    endpoint_style: str = CHAT
    system_prompt: str | None = None
    # Text placed BEFORE the shared task block, in the model's own dialect.
    lead_in: str = ""
    # Text placed AFTER the shared task block.
    tail: str = ""
    # vLLM's --max-model-len for this model, and the generation cap we ask for. Both are
    # per-model (added 2026-08-03) because they are MODEL PROPERTIES, not run policy: Herald is a
    # 4096-context Llama and refuses to serve at 8192 at all, which killed the first smoke run.
    # A single global value cannot be right for a set spanning 4k to 64k context.
    # Invariant the table must preserve: max_tokens + longest prompt (~1300 tok) <= max_model_len.
    max_model_len: int = 16384
    max_tokens: int = 8192
    card_url: str = ""
    card_notes: str = ""
    card_sampling: dict = field(default_factory=dict)


# The shared instruction lines every wrapper wraps. Defined here rather than in `prompts` so the
# model table and the contract it must preserve sit side by side.
MODELS: dict[str, ModelSpec] = {
    "goedel-prover-v2-8b": ModelSpec(
        slug="goedel-prover-v2-8b",
        hf_name="Goedel-LM/Goedel-Prover-V2-8B",
        endpoint_style=CHAT,
        system_prompt=None,  # card's example uses a bare user turn, no system message
        lead_in="Complete the following Lean 4 code:",
        tail=(
            "Before producing the Lean 4 code, provide a detailed plan outlining the main steps "
            "and strategies."
        ),
        card_url="https://huggingface.co/Goedel-LM/Goedel-Prover-V2-8B",
        card_notes=(
            "Chat template via apply_chat_template, single user turn, no system message. Card's "
            "verbatim framing is 'Complete the following Lean 4 code:' followed by a lean4 fence, "
            "then a request for a detailed proof plan before the code. Both borrowed here, with "
            "'proof' softened to 'code' since we ask for a definition, not a proof."
        ),
        card_sampling={"max_new_tokens": 32768},
    ),
    "kimina-prover-distill-7b": ModelSpec(
        slug="kimina-prover-distill-7b",
        hf_name="AI-MO/Kimina-Prover-Preview-Distill-7B",
        endpoint_style=CHAT,
        system_prompt="You are an expert in mathematics and Lean 4.",
        lead_in=(
            "Think about and solve the following problem step by step in Lean 4."
        ),
        tail="",
        card_url="https://huggingface.co/AI-MO/Kimina-Prover-Preview-Distill-7B",
        card_notes=(
            "Chat template with the system prompt 'You are an expert in mathematics and Lean 4.' "
            "(verbatim from the card). Card's user turn is structured as an instruction line then "
            "'# Problem:' and '# Formal statement:' sections; our shared task block already "
            "carries the equivalent headed sections, so only the instruction line is borrowed."
        ),
        card_sampling={"temperature": 0.6, "top_p": 0.95, "max_tokens": 8096},
    ),
    "goedel-formalizer-v2-8b": ModelSpec(
        slug="goedel-formalizer-v2-8b",
        hf_name="Goedel-LM/Goedel-Formalizer-V2-8B",
        endpoint_style=CHAT,
        system_prompt=None,  # card's example is a bare user turn
        lead_in="Please autoformalize the following natural language definition in Lean 4.",
        tail="Think before you provide the Lean statement.",
        card_url="https://huggingface.co/Goedel-LM/Goedel-Formalizer-V2-8B",
        card_notes=(
            "Added 2026-08-03 as the seventh model, to strengthen the autoformalizer column "
            "where Herald is the lowest-confidence entry. Chat template, bare user turn, no "
            "system message. Card's verbatim framing is 'Please autoformalize the following "
            "natural language problem statement in Lean 4. Use the following theorem name: "
            "{problem_name} ... Think before you provide the lean statement.' Adapted per the "
            "Stage-2 method: 'problem statement'->'definition' (we want a definition, not a "
            "theorem), and the theorem-name clause dropped since our shared block already pins "
            "the exact symbol and signature. The 'think before' instruction is kept verbatim as "
            "the tail -- it is this model's distinguishing feature per its own card."
        ),
        card_sampling={"temperature": 0.9, "top_k": 20, "top_p": 0.95, "max_tokens": 16384},
    ),
    "qwen2.5-coder-7b-instruct": ModelSpec(
        slug="qwen2.5-coder-7b-instruct",
        hf_name="Qwen/Qwen2.5-Coder-7B-Instruct",
        endpoint_style=CHAT,
        system_prompt="You are Qwen, created by Alibaba Cloud. You are a helpful assistant.",
        lead_in="Write the following Lean 4 definition.",
        tail="",
        card_url="https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct",
        card_notes=(
            "Standard ChatML instruct. System prompt is the card's own verbatim default. This is "
            "the general-purpose control in the set: no theorem-proving specialisation, so it "
            "measures how much the prover fine-tunes actually buy on this task."
        ),
        card_sampling={"max_new_tokens": 512},
    ),
}



# --- Excluded from the field, 2026-08-03, after live smoke testing -----------------------------
#
# Kept as a record rather than deleted: each exclusion is a result, and a later reader needs to
# know the field was seven and why it became four. The distinction between the two REASONS is
# load-bearing for how the write-up may talk about them.
DROPPED_MODELS = {
    "kimina-autoformalizer-7b": {
        "hf_name": "AI-MO/Kimina-Autoformalizer-7B",
        "reason": "task_mismatch",
        "measured": True,   # a real finding about the model, safe to report as such
        "detail": (
            "Emits theorem STATEMENTS, not definitions. Predicted from its card in Stage 2 "
            "('trained to emit statements ending in by sorry') and confirmed twice live: with "
            "the original prompt it returned `theorem VTask_clog ... := by sorry` (65 tokens), "
            "and with the sharpened output-shape prompt it wrapped the entire prompt in a Lean "
            "comment and still returned a theorem (1122 tokens). This is the wrong instrument "
            "for the task, not a model that performed badly at it -- no prompt change fixes it."
        ),
    },
    "herald-7b": {
        "hf_name": "FrenzyMath/Herald_translator",
        "reason": "detokenizer_corruption",
        "measured": False,  # EXCLUDED-UNMEASURED: we never got a fair reading of this model
        "detail": (
            "Output arrives byte-corrupted under vLLM 0.26 (latin1-rendered UTF-8), and the "
            "content was unrelated training data -- the sample tail was Chinese SEO copy about a "
            "phone launch. Also the only model with no documented chat template, a 4096 context "
            "forcing a smaller token budget than the rest, and 26 GB on disk (2x the others). "
            "This is an infrastructure failure on our side, NOT a measurement of the model: it "
            "must not be reported as having performed poorly."
        ),
    },
    "deepseek-prover-v2-7b": {
        "hf_name": "deepseek-ai/DeepSeek-Prover-V2-7B",
        "reason": "detokenizer_corruption",
        "measured": False,  # EXCLUDED-UNMEASURED, same class as Herald
        "detail": (
            "Same byte-level corruption as Herald: output littered with raw BPE artifacts "
            "(unicode 'G-dot'/'C-dot' for space/newline), and content that ignores the prompt "
            "entirely (returned `theorem exercise_2_1_20` about Function.Injective -- memorised "
            "benchmark text). One bounded rescue was attempted and pre-declared: re-served with "
            "--tokenizer-mode slow, 2026-08-03, one sample -- still 170 artifact characters and "
            "still no mention of the requested symbol. Dropped per that agreement without a "
            "second theory. Note both corrupted models are non-Qwen-family; the three that "
            "decode cleanly are all Qwen-derived, which points at vLLM 0.26's detokenizer rather "
            "than at anything in this repo."
        ),
    },
}

MODEL_SLUGS = tuple(MODELS)


def get_model(slug: str) -> ModelSpec:
    if slug not in MODELS:
        raise KeyError(f"unknown model slug {slug!r}; known: {', '.join(MODEL_SLUGS)}")
    return MODELS[slug]
