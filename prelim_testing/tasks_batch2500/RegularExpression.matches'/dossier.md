## Object

Given a regular expression `P` over an alphabet `α`, `VTask.matches'` produces the **formal language** (a set of finite strings over `α`) consisting of exactly those strings that `P` matches. Concretely:
- The empty regular expression `0` corresponds to the empty language.
- The epsilon expression `1` corresponds to the language containing only the empty string.
- A character expression `char a` corresponds to the singleton language `{[a]}`.
- Alternation `P + Q` corresponds to the union of the two languages.
- Concatenation `P * Q` corresponds to the concatenation product of the two languages.
- The Kleene star `star P` corresponds to the Kleene closure of the language of `P`.

The function is defined by structural recursion on the regular expression.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.matches' : {α : Type u_1} -> RegularExpression α → Language α
<!-- PINNED-SIGNATURE:END -->


`VTask.matches' : {α : Type u_1} -> RegularExpression α → Language α`

The implicit argument `α` is the alphabet type — the type of individual symbols from which strings (finite lists) are formed. The explicit argument is the regular expression whose matching behaviour is being reified as a formal language.

## Conventions

The definition is total; there are no junk-value conventions. Every constructor of `RegularExpression α` is handled, so no input is out of domain.

## Worked examples

- Claim: `VTask.matches' (0 : RegularExpression Char) = 0` — the empty regular expression maps to the empty language.

- Claim: `VTask.matches' (1 : RegularExpression Char) = 1` — the epsilon expression maps to the language containing only the empty string `[]`.

- Claim: `VTask.matches' (RegularExpression.char 'a') = {['a']}` — a single-character expression maps to the singleton language containing exactly the one-character string.

- Claim: For any `P Q : RegularExpression α`, `VTask.matches' (P + Q) = VTask.matches' P + VTask.matches' Q` — alternation maps to language union.

- Claim: For any `P Q : RegularExpression α`, `VTask.matches' (P * Q) = VTask.matches' P * VTask.matches' Q` — concatenation maps to language (concatenation) product.

- Claim: For any `P : RegularExpression α`, `VTask.matches' (P.star) = (VTask.matches' P)∗` — the Kleene star constructor maps to the Kleene closure of the corresponding language.

- Claim: For any `P : RegularExpression α` and string `x : List α`, `P.rmatch x = true` if and only if `x ∈ VTask.matches' P` — the decision procedure `rmatch` is sound and complete with respect to `matches'`.

## Boundaries

- **Empty language (`0`):** `VTask.matches' 0` is the empty set of strings; no string is matched.
- **Epsilon (`1`):** `VTask.matches' 1` contains precisely the empty list `[]`; no non-empty string is matched.
- **Kleene star of zero:** `VTask.matches' (star 0)` equals `(∅)∗`, which is the language containing only the empty string `[]` (since the only way to concatenate zero or more strings from the empty language is the empty concatenation).
- **Kleene star of epsilon:** `VTask.matches' (star 1)` equals `{[]}∗ = {[]}`, also just the empty string.
- **Power:** `VTask.matches' (P ^ n)` equals `(VTask.matches' P) ^ n`, the n-fold language concatenation product.

## Not to be confused with

- `RegularExpression.rmatch` — a Boolean decision procedure that checks whether a *specific* string is matched; `VTask.matches'` produces the entire language as a set, not a yes/no answer for one string.
- `Language` (the type itself) — `Language α` is just `Set (List α)`; `VTask.matches'` is the specific map sending a regular expression to the set of strings it recognises.
- `RegularExpression.map` — transforms a regular expression by applying a function on the alphabet; not to be confused with `VTask.matches'` which interprets a regular expression as a language over the *same* alphabet.