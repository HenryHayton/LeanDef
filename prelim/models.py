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
    "deepseek-prover-v2-7b": ModelSpec(
        slug="deepseek-prover-v2-7b",
        hf_name="deepseek-ai/DeepSeek-Prover-V2-7B",
        endpoint_style=CHAT,  # NOT completion -- see card_notes; corrects Stage 1's assumption
        system_prompt=None,
        lead_in="Complete the following Lean 4 code:",
        tail=(
            "Before producing the Lean 4 code, provide a detailed plan outlining the main steps "
            "and strategies."
        ),
        card_url="https://huggingface.co/deepseek-ai/DeepSeek-Prover-V2-7B",
        card_notes=(
            "ASSUMPTION CORRECTED: the V2 card uses apply_chat_template with a single user turn, "
            "not the raw-completion style V1.5 was known for. Endpoint style is therefore CHAT. "
            "Same 'Complete the following Lean 4 code' + plan-first framing as Goedel (both "
            "descend from the same DeepSeek-Prover lineage). No system message."
        ),
        card_sampling={"max_new_tokens": 8192},
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
    "kimina-autoformalizer-7b": ModelSpec(
        slug="kimina-autoformalizer-7b",
        hf_name="AI-MO/Kimina-Autoformalizer-7B",
        endpoint_style=CHAT,
        system_prompt="You are an expert in mathematics and Lean 4.",
        lead_in="Please formalize the following definition in Lean 4.",
        tail="",
        card_url="https://huggingface.co/AI-MO/Kimina-Autoformalizer-7B",
        card_notes=(
            "Chat template, same system prompt as the Kimina prover. Card's user framing is "
            "'Please autoformalize the following problem in Lean 4 with a header. Use the "
            "following theorem names: ...'. Adapted: 'problem'->'definition' (we want a "
            "definition, not a theorem stub) and the theorem-names clause dropped, since our "
            "shared block already pins the exact symbol and signature. Note this model is trained "
            "to emit statements ending in 'by sorry' -- a real risk of sorry-terminated output "
            "that the extractor tolerates and scoring will catch."
        ),
        card_sampling={"temperature": 0.6, "top_p": 0.95, "max_tokens": 2048},
    ),
    "herald-7b": ModelSpec(
        slug="herald-7b",
        hf_name="FrenzyMath/Herald_translator",
        endpoint_style=CHAT,
        system_prompt=None,
        lead_in="Translate the following definition into Lean 4.",
        tail="",
        card_url="https://huggingface.co/FrenzyMath/Herald_translator",
        card_notes=(
            "HF id VERIFIED as FrenzyMath/Herald_translator (Herald: A Natural Language Annotated "
            "Lean 4 Dataset, ICLR 2025, arXiv 2410.10878). Card is THIN: it ships a chat template "
            "and shows a bare user turn, but documents no system prompt and no sampling "
            "recommendations. Wrapper is therefore deliberately neutral -- a 'translate this into "
            "Lean 4' framing matching the model's stated translator purpose. Lowest-confidence "
            "entry of the six; the live smoke test should scrutinise this one first."
        ),
        card_sampling={},
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

MODEL_SLUGS = tuple(MODELS)


def get_model(slug: str) -> ModelSpec:
    if slug not in MODELS:
        raise KeyError(f"unknown model slug {slug!r}; known: {', '.join(MODEL_SLUGS)}")
    return MODELS[slug]
