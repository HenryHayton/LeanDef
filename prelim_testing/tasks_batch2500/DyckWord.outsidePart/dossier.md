## Object

Every non-empty Dyck word `p` has a canonical decomposition: the first time the word returns to ground level after its opening step identifies a distinguished prefix. Concretely, one writes `p = U · insidePart(p) · D · outsidePart(p)`, where `U` and `D` are a matched up-step/down-step pair. `outsidePart p` is the suffix of `p` that lies *after* that initial matched `U…D` pair — the part "outside" (to the right of) the first-return bracket. For the empty Dyck word, `outsidePart` is defined to be the empty Dyck word `0`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.outsidePart : (p : DyckWord) -> DyckWord
<!-- PINNED-SIGNATURE:END -->


The single argument is the Dyck word being decomposed. It plays the role of the word `p` whose outermost first-return decomposition is being analysed.

## Conventions

`outsidePart 0 = 0`: the empty Dyck word is mapped to the empty Dyck word, serving as a junk/base value for the case where no first-return decomposition exists.

## Worked examples

- Claim: For the empty Dyck word `0`, `outsidePart 0 = 0`.

- Claim: For any Dyck word `p`, wrapping it in a single matched pair via `p.nest` (i.e., forming `U · p · D`) gives `outsidePart (p.nest) = 0`, because the entire content lies *inside* the first-return pair and nothing is left outside.

- Claim: For a concatenation `p + q` of two Dyck words, `(p + q).outsidePart = p.outsidePart + q`. That is, the outside part of a concatenation is the outside part of the first summand, followed by the entirety of the second summand.

- Claim: The reconstruction identity holds: `p.insidePart.nest + p.outsidePart = p`, confirming that `insidePart` and `outsidePart` together recover the original word.

- Claim: For any non-empty Dyck word `p`, `p.outsidePart.semilength < p.semilength`, so `outsidePart` strictly reduces the half-length, enabling well-founded recursion.

## Boundaries

- **Empty word**: `outsidePart 0 = 0`. This is a defined convention rather than a structural fact, since the empty word has no first-return decomposition.
- **Single matched pair `nest 0 = U D`**: `outsidePart (nest 0) = 0`, as there is nothing after the single `U D` pair.
- **Nested words `p.nest`**: Always yield `outsidePart = 0` regardless of `p`, because the whole word is enclosed in one first-return bracket.
- **Concatenations**: The outside part picks up the entirety of the second summand together with the outside part of the first, reflecting that `firstReturn` is determined by the first summand alone.

## Not to be confused with

- `DyckWord.insidePart`: the *inside* (left inner) part of the first-return decomposition, i.e., what sits between the first `U` and its matching `D`.
- `DyckWord.firstReturn`: the *index* (natural number position) of the first return to zero, which is used to compute where `outsidePart` begins, not the word itself.
- `DyckWord.nest`: the operation that wraps a Dyck word in a single matched `U…D` pair, which is the *inverse* building block from which `insidePart`/`outsidePart` together reconstruct the original word.