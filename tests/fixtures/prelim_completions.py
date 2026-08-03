"""Hand-written realistic completions, one per candidate model, in that model's documented
output style.

These are the best available proxy for real output until Stage 2's live smoke test: each is
modelled on the shape the model's own card/paper advertises (CoT-then-fence for the provers,
`by sorry`-terminated statements for the autoformalizer, plain ChatML prose+fence for Qwen), not
invented freely. They exist so the extractor is exercised against six genuinely different output
dialects rather than six variations of one.

Every fixture answers the SAME task (`VTask.clog`), so differences between them are purely
stylistic -- which is the point: extraction must be robust to dialect, not to content.

FLAGGED: these are proxies. The live smoke test replaces them as the source of truth, and any
fixture that turns out to misrepresent its model should be corrected there and then.
"""

# Goedel-Prover-V2: prompted to plan first, so a long prose plan precedes a ```lean4 fence.
GOEDEL = """\
### Proof Plan

We need to define the ceiling logarithm. The key observations are:

1. When the base `b ≤ 1`, no power of `b` grows, so the function must return the junk value `0`.
2. When `n ≤ 1`, we have `n ≤ b^0 = 1`, so the answer is `0`.
3. Otherwise we recurse on `(n + b - 1) / b`, adding one each time.

The recursion terminates because for `b ≥ 2` and `n ≥ 2` the argument strictly decreases.

Now the Lean 4 code:

```lean4
def VTask.clog (b n : ℕ) : ℕ :=
  if h : 1 < b ∧ 1 < n then
    have : (n + b - 1) / b < n := by
      sorry
    VTask.clog b ((n + b - 1) / b) + 1
  else
    0
```

This handles all the boundary cases described in the dossier.
"""

# DeepSeek-Prover-V2: same lineage, same plan-first framing; tends to use ```lean.
DEEPSEEK = """\
Let me work through this step by step.

The ceiling logarithm of `n` in base `b` is the least `k` with `n ≤ b^k`. The dossier specifies
junk value `0` for `b ≤ 1` or `n ≤ 1`.

```lean
def VTask.clog (b n : ℕ) : ℕ :=
  if 1 < b ∧ 1 < n then
    VTask.clog b ((n + b - 1) / b) + 1
  else 0
decreasing_by sorry
```
"""

# Kimina-Prover-Distill: reasoning-heavy, often with an explicit <think> section.
KIMINA_PROVER = """\
<think>
The problem asks for a ceiling logarithm on natural numbers. I need to be careful about the
junk-value conventions: base 0 or 1 gives 0, and n ≤ 1 gives 0 as well.

A structural recursion won't work directly here; I'll use well-founded recursion on n.
</think>

Here is the definition:

```lean
noncomputable def VTask.clog (b n : ℕ) : ℕ :=
  if 1 < b ∧ 1 < n then VTask.clog b ((n + b - 1) / b) + 1 else 0
```
"""

# Kimina-Autoformalizer: trained to emit statements ending in `by sorry`, and to include a
# header. A realistic risk: it may formalize as a theorem stub rather than a definition.
KIMINA_AUTOFORMALIZER = """\
import Mathlib

def VTask.clog (b n : ℕ) : ℕ :=
  if 1 < b ∧ 1 < n then VTask.clog b ((n + b - 1) / b) + 1 else 0
"""

# Herald: a translator model; card is thin, so we assume a fairly bare fenced answer.
HERALD = """\
```lean
def VTask.clog (b n : ℕ) : ℕ :=
  if 1 < b ∧ 1 < n then
    VTask.clog b ((n + b - 1) / b) + 1
  else
    0
```
"""

# Qwen2.5-Coder-Instruct: general-purpose instruct model -- explains, fences, then explains more.
QWEN = """\
I'll write the ceiling logarithm definition for you.

Looking at the specification, we need a function that returns the smallest `k` such that
`n ≤ b^k`, with junk value `0` in the degenerate cases.

```lean
def VTask.clog (b n : ℕ) : ℕ :=
  if 1 < b ∧ 1 < n then
    VTask.clog b ((n + b - 1) / b) + 1
  else
    0
```

Note that this uses well-founded recursion. You may need a `termination_by` clause depending on
your Lean version. Let me know if you'd like me to adjust it!
"""

# Goedel-Formalizer-V2: its card's distinguishing feature is "think before you provide the lean
# statement", so an explicit reasoning section precedes the fenced answer. Modelled on that
# framing; note it is an autoformalizer, so like Kimina-Autoformalizer it may reach for a
# statement-shaped output.
GOEDEL_FORMALIZER = """\
Let me think about this before writing the Lean statement.

The object is a ceiling logarithm on ℕ. The dossier pins the signature as
`VTask.clog : (b n : ℕ) -> ℕ` and specifies junk value 0 when the base is ≤ 1 or the argument
is ≤ 1. So the formalization needs a total function with those two guard cases, and a recursive
step that divides by the base rounding up.

```lean4
def VTask.clog (b n : ℕ) : ℕ :=
  if 1 < b ∧ 1 < n then
    VTask.clog b ((n + b - 1) / b) + 1
  else
    0
```
"""

BY_MODEL = {
    "goedel-prover-v2-8b": GOEDEL,
    "deepseek-prover-v2-7b": DEEPSEEK,
    "kimina-prover-distill-7b": KIMINA_PROVER,
    "kimina-autoformalizer-7b": KIMINA_AUTOFORMALIZER,
    "herald-7b": HERALD,
    "goedel-formalizer-v2-8b": GOEDEL_FORMALIZER,
    "qwen2.5-coder-7b-instruct": QWEN,
}

# --- Adversarial / failure-mode fixtures -------------------------------------------------------

# Pure prose refusal: no declaration anywhere.
NO_DEF = """\
I'm not able to write this definition without more information about the intended
behaviour at the boundary. Could you clarify what should happen when the base is zero?
"""

# Cut off mid-body by the token budget (paired with finish_reason="length").
TRUNCATED = """\
Here is the definition:

```lean
def VTask.clog (b n : ℕ) : ℕ :=
  if 1 < b ∧ 1 < n then
    VTask.clog b ((n + b - 1) /\
"""

# Two competing declarations, NEITHER using the requested VTask name.
AMBIGUOUS = """\
There are two reasonable readings. Either:

```lean
def clogFloor (b n : ℕ) : ℕ := Nat.log b n
```

or alternatively:

```lean
def clogCeil (b n : ℕ) : ℕ := Nat.log b (n - 1) + 1
```
"""

# Exactly one declaration, but under the model's own name rather than the pinned symbol.
RENAMED = """\
```lean
def clog (b n : ℕ) : ℕ :=
  if 1 < b ∧ 1 < n then clog b ((n + b - 1) / b) + 1 else 0
```
"""

# A plan sketch in a first fence, then the real answer in a second.
TWO_FENCES_LAST_WINS = """\
First, a sketch of the shape:

```lean
def VTask.clog (b n : ℕ) : ℕ := sorry
```

Now filling in the body:

```lean
def VTask.clog (b n : ℕ) : ℕ :=
  if 1 < b ∧ 1 < n then VTask.clog b ((n + b - 1) / b) + 1 else 0
```
"""

# No fence at all -- a bare declaration sitting directly in prose.
BARE_NO_FENCE = """\
The definition is as follows.

noncomputable def VTask.clog (b n : ℕ) : ℕ :=
  if 1 < b ∧ 1 < n then VTask.clog b ((n + b - 1) / b) + 1 else 0

That should satisfy all the stated boundary conventions.
"""
