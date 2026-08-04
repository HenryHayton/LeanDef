"""The pinned signature a candidate's body fills in.

Split into its own module (rather than living in `harness.scoring`) so both
`harness.scoring` and `harness.admissibility` can depend on it without a circular import.
"""

import re
from dataclasses import dataclass

# Characters that may appear inside a Lean identifier. THE definition for this repo:
# `authoring.namematch` imports this rather than keeping its own copy (2026-08-04) -- that
# module's own docstring records what three independently-drifted copies of a name matcher
# cost the last time, and root-qualification below needs exactly the same notion of "glued to
# more identifier characters". Deliberately NOT Python's `\w`: Lean allows a trailing prime,
# and treating `'` as a boundary is what made `Equiv.ofLeftInverse` match inside the entirely
# distinct `Equiv.ofLeftInverse'`.
LEAN_IDENT_CHAR = r"[A-Za-z0-9_']"


def root_qualify(name: str) -> str:
    """`_root_.<name>` -- the ONE definition of what root-qualification means here.

    Both splice paths route through this: the truth-side alias (`splice_real_name`, which
    qualifies a whole bare declaration name) and the candidate-side retry
    (`PinnedSignature.root_qualified_body`, which qualifies bare references *inside* a body).
    The two operations differ -- one prefixes a name, the other rewrites occurrences in a
    larger expression -- but "what a root-qualified reference looks like" must not be spelled
    out twice.
    """
    return f"_root_.{name}"



# The head of a Lean declaration: optional attribute groups, optional modifiers, the keyword,
# then the declared name. Used to locate where a declaration's HEADER ends and its body begins,
# which is what lets root-qualification rewrite only the body (see `root_qualified_declaration`).
_DECL_HEAD_RE = re.compile(
    r"^\s*((?:@\[[^\]]*\][ \t]*)*)"                                    # 1: attribute groups
    r"((?:private[ \t]+|protected[ \t]+|noncomputable[ \t]+|partial[ \t]+|unsafe[ \t]+)*)"  # 2: modifiers
    r"(def|abbrev|instance)[ \t]+"                                       # 3: keyword
    r"([A-Za-z_][A-Za-z0-9_.']*)",                                        # 4: declared name
)


def reducible_declaration(decl_text: str, *, noncomputable: bool = False) -> str:
    """Return `decl_text` with `@[reducible]` applied, preserving whatever the model wrote.

    Splicing a candidate's declaration VERBATIM (2026-08-05) replaced the old
    `PinnedSignature.splice(body)` construction for real candidate scoring: the prelim prompt
    asks models for a complete declaration, not a body expression, and parsing declarations back
    into bodies is fragile against implicit/instance binders, equation-style definitions and
    `where` clauses -- every parse failure would be another differential-by-output-style false
    negative. The pinned type is enforced by kernel check instead of by construction, which is
    strictly stronger: it accepts a defeq-but-differently-phrased signature the constructor could
    never have expressed.

    Two mechanics, both confirmed against live Lean rather than assumed:

    - **Attributes MERGE, they do not stack.** `@[reducible] @[simp] def` is a syntax error
      ("unexpected token '@['"); `@[reducible, simp] def` is fine. So `reducible` is folded into
      the model's first attribute group when it has one.
    - **`noncomputable` goes after the attributes**, the only order Lean accepts. It is inserted
      only when asked for and not already present -- a model that wrote it keeps it, since it is
      load-bearing for classical constructions.
    """
    m = _DECL_HEAD_RE.match(decl_text)
    if m is None:
        # Not a recognisable declaration head. Prepend and let Lean produce the honest error
        # rather than silently mangling text we do not understand.
        return f"@[reducible] {decl_text}"

    attrs, modifiers = m.group(1).strip(), m.group(2)
    rest = decl_text[m.end(2):]

    if attrs:
        inner = attrs.strip()[2:-1].strip() if attrs.startswith("@[") and attrs.endswith("]") else None
        merged = f"@[reducible, {inner}]" if inner else f"@[reducible] {attrs}"
    else:
        merged = "@[reducible]"

    if noncomputable and "noncomputable" not in modifiers:
        modifiers = f"noncomputable {modifiers.strip()} ".replace("  ", " ")
    return f"{merged} {modifiers.strip()} {rest.strip()}".replace("  ", " ").strip()


def declaration_body_offset(decl_text: str) -> int:
    """Index just past the declared name -- everything after it is body/binders.

    Root-qualification must not touch the header: a declaration always spells its own task
    symbol there (`def VTask.clog ...`), so treating the header as a self-reference would make
    `references_self_explicitly` true for every candidate and disable the rescue entirely.
    """
    m = _DECL_HEAD_RE.match(decl_text)
    return m.end(4) if m else 0

@dataclass(frozen=True)
class PinnedSignature:
    """A task's pinned definition name and type -- the hole a candidate body fills.

    Previously (`archive/n1_tau/score.py`) the name and type were retyped as a literal
    substring inside every one of 9 candidate strings; see `docs/repo_audit.md` §3 ("Pinned
    signature representation") and observation 5.
    """

    name: str
    type_sig: str

    @property
    def base_name(self) -> str:
        """The last dotted component of the pinned name -- `VTask.Monotone` -> `Monotone`.

        This is the string a candidate body can accidentally self-reference: inside
        `def VTask.Monotone`, a bare `Monotone` resolves against the enclosing `VTask`
        namespace and finds the declaration currently being elaborated. See
        `root_qualified_body`.
        """
        return self.name.rsplit(".", 1)[-1]

    def references_self_explicitly(self, body: str) -> bool:
        """True when `body` names the pinned symbol IN FULL (`VTask.Monotone`), as opposed to
        a bare `Monotone` that merely resolves to it.

        Spelling the whole symbol out is an unambiguous statement of intent to recurse, so
        `harness.scoring`'s root-qualification retry declines to touch such a body at all --
        it would be rewriting a reference the candidate clearly meant. A bare reference is
        genuinely ambiguous (it could be intended recursion OR an intended reference to the
        shadowed real declaration), and is only ever rewritten after the plain attempt has
        already failed with a self-reference-shaped error.
        """
        pattern = rf"(?<!{LEAN_IDENT_CHAR})(?<!\.){re.escape(self.name)}(?!{LEAN_IDENT_CHAR})(?!\.)"
        return re.search(pattern, body) is not None

    def root_qualified_body(self, body: str) -> tuple[str, int]:
        """`(rewritten_body, n_rewrites)` -- bare references to `base_name` become
        `_root_.<base_name>`.

        Rewrites ONLY occurrences standing alone as a complete identifier: not preceded or
        followed by an identifier character, and not adjacent to a dot on either side. That
        last exclusion is what keeps the rewrite safe:

        - `Nat.clog` (base `clog` preceded by `.`) is already a dotted path that resolves
          correctly -- untouched.
        - `VTask.clog` (the task symbol itself) is likewise dotted -- untouched, so a
          deliberately recursive body survives this function even if it is ever called on one.
        - `clog2` / `clog'` are different identifiers -- untouched, per `LEAN_IDENT_CHAR`.
        - bare `clog`, the one shape that mis-resolves, is rewritten.

        Known limitation, stated rather than papered over: this is a regex over the body text,
        so a base name appearing inside a string literal or comment would also be rewritten.
        Writing a Lean lexer to avoid that is not worth it for definition bodies, and the
        rewrite is only ever *attempted* after a real self-reference failure, never speculatively.
        """
        pattern = rf"(?<!{LEAN_IDENT_CHAR})(?<!\.){re.escape(self.base_name)}(?!{LEAN_IDENT_CHAR})(?!\.)"
        rewritten, n = re.subn(pattern, root_qualify(self.base_name), body)
        return rewritten, n

    def declaration_references_self_explicitly(self, decl_text: str) -> bool:
        """`references_self_explicitly`, but skipping the declaration HEADER.

        A declaration always spells its own task symbol in its head (`def VTask.clog ...`), so
        checking the whole text would report every candidate as deliberately self-referential
        and permanently disable the root-qualification rescue. Only a mention in the BODY is
        evidence of intended recursion.
        """
        offset = declaration_body_offset(decl_text)
        return self.references_self_explicitly(decl_text[offset:])

    def root_qualified_declaration(self, decl_text: str) -> tuple[str, int]:
        """`root_qualified_body` applied to the body region only, for the same reason: the
        header's own `VTask.clog` is the declaration being made, not a reference to rewrite."""
        offset = declaration_body_offset(decl_text)
        rewritten, n = self.root_qualified_body(decl_text[offset:])
        return decl_text[:offset] + rewritten, n

    def splice(self, body: str, *, noncomputable: bool = False) -> str:
        """Render `@[reducible] def <name> : <type> := <body>` for a well-formed, single-
        declaration candidate. For a candidate that needs to be more than one declaration
        (helper lemmas -- or, deliberately, for admissibility-gate testing, adversarial extra
        declarations), build the raw command text directly instead of using this helper.

        `@[reducible]` (2026-07-30, `docs/design/llm_io_contract_v1.md` §4.4): Lean's
        typeclass search only unfolds `@[reducible]`-marked definitions, not plain `def`s. A
        plain-`def` task-symbol splice is therefore opaque to instance search -- confirmed the
        hard way against a real gate task (`Nat.ModEq`): `Nat.ModEq`'s own `Decidable` instance
        is keyed to `Nat.ModEq`'s head symbol (`Mathlib/Data/Nat/ModEq.lean`), so
        `Decidable (VTask.ModEq n a b)` failed to synthesize under a plain-`def` splice even
        though the underlying proposition is genuinely decidable. `@[reducible]` (chosen over
        `abbrev`, which is strictly more than needed here -- `abbrev` also marks `@[inline]`
        and widens unification-default transparency beyond typeclass search, neither of which
        this fix requires) is the minimal attribute that makes instance search see through the
        splice. Applies uniformly to every splice this method produces -- truth-splice
        (`authoring.pipeline`) and candidate splice (`authoring.roundtrip`, and
        `harness.scoring.score_candidate`'s future real-candidate path) both call this single
        method, so both are covered by one change; there is no separate "candidate normalizes
        its own attribute" step because a candidate never writes this line itself, the harness
        always does. Confirmed NOT to change outcomes on the value-typed path (`Nat.clog`):
        decidable-equality facts on a value-typed definition's OUTPUT resolve via a generic
        instance on the output's own type (e.g. `Nat.decEq`), never needing to unfold the
        definition's own name for instance search, so reducibility was never the blocker there
        -- see the regression tests this change shipped with.

        `noncomputable` (2026-08-04, candidate/truth parity) renders the same
        `@[reducible] noncomputable def` word order `splice_real_name` established -- the only
        order Lean accepts, attributes before modifiers. It defaults to False, so every
        existing single-argument call site emits byte-identical text. The modifier is supplied
        by the HARNESS, never by the candidate: `splice` keeps only the body expression, so a
        model that wrote its own `noncomputable def` header has already had it discarded by
        extraction. `harness.scoring.splice_candidate_body`'s retry is therefore the only path
        by which such a candidate can ever compile."""
        modifier = "noncomputable " if noncomputable else ""
        return f"@[reducible] {modifier}def {self.name} : {self.type_sig} := {body}"

    def splice_real_name(self, real_name: str, *, noncomputable: bool = False) -> str:
        """The TRUTH-splice specifically: alias an EXISTING Mathlib declaration (`real_name`)
        under this pinned signature -- as opposed to `splice`, which takes an arbitrary
        candidate body expression (a round-trip attempt, a real candidate). Two things `splice`
        alone gets wrong for this specific case, both confirmed empirically (2026-07-31, the
        "Harness Fixes" session, against the 41-name batch's real `truth_splice` casualties):

        1. **Root-qualification.** `real_name` is passed bare (e.g. `Monotone`, not
           `_root_.Monotone`) whenever the real declaration lives at the top level with no
           namespace prefix. `def VTask.Monotone := Monotone` then fails Lean's termination
           checker with a baffling "well-founded recursion cannot be used" error -- not because
           of any real recursion, but because Lean's name resolution for the bare `Monotone` in
           the body matches the CURRENTLY-BEING-ELABORATED `VTask.Monotone` (both end in
           `.Monotone`) instead of the real top-level one, producing a bogus self-referential
           definition. Confirmed via a 4-name x 3-attribute-variant repro matrix that this has
           nothing to do with `@[reducible]`/`abbrev` (identical failure under plain `def` too)
           and via direct isolation that root-qualifying (`_root_.Monotone`) or renaming the
           task symbol's own base name each independently fix it, while leaving every
           already-working name (`Nat.clog`, `Nat.ModEq`, ...) unaffected -- `_root_.` is always
           safe to prepend, so it is applied unconditionally here, not just for no-dot names.
        2. **Noncomputability.** Some real declarations are noncomputable at an ALIAS site even
           though their own source line carries no explicit `noncomputable` keyword (confirmed:
           `Function.extend`'s body is `open scoped Classical in if h : ... then ... else ...`,
           which Mathlib's own declaration is permitted to elaborate without the keyword, but a
           downstream `def X := Function.extend` is not). This is NOT reliably detectable from
           source text -- `miner.scan`'s own text-scan for a literal `noncomputable` prefix
           would (and did, when checked directly against the real source line) miss this exact
           case -- so `noncomputable` is a caller-supplied flag, discovered by trying without it
           first and retrying with it on Lean's own specific compiler error
           (`authoring.pipeline`'s truth-splice call site owns that retry; this method only
           knows how to render the modifier when told to)."""
        modifier = "noncomputable " if noncomputable else ""
        return f"@[reducible] {modifier}def {self.name} : {self.type_sig} := {root_qualify(real_name)}"
