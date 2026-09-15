## Object

`VTask.noBotOrderSentence` is the first-order sentence (over an ordered language) expressing that the underlying order has **no bottom element**: for every element $x$ there exists an element $y$ such that $y < x$ (equivalently, $x$ is not a lower bound for everything, i.e., $\forall x,\, \exists y,\, \neg(x \le y)$).

Wait — the docstring reads $\forall x,\, \exists y,\, \neg(x \le y)$, which says for every $x$ there is some $y$ that $x$ does NOT reach from below. This is equivalent to saying there is no minimum element: no element $x$ satisfies $x \le y$ for all $y$.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.noBotOrderSentence : (L : FirstOrder.Language) -> [L.IsOrdered] -> L.Sentence
<!-- PINNED-SIGNATURE:END -->


VTask.noBotOrderSentence : (L : FirstOrder.Language) -> [L.IsOrdered] -> L.Sentence

The first argument `L` is the first-order language in which the sentence is written; it must carry an ordering structure (supplied by the implicit `IsOrdered` instance), which provides the binary relation symbol $\le$ used to build the sentence.

## Conventions

No junk-value or edge conventions apply: the sentence is a fully determined closed formula once `L` and its `IsOrdered` instance are fixed. There are no degenerate inputs to speak of.

## Worked examples

- Claim: The structure $(\mathbb{Z}, \le)$ (the integers with the usual order) satisfies `VTask.noBotOrderSentence` because the integers have no minimum element — for every integer $x$ there exists $y = x - 1$ with $\neg(x \le x-1)$.

- Claim: The structure $(\mathbb{N}, \le)$ (the natural numbers with the usual order) does **not** satisfy `VTask.noBotOrderSentence`, because $0$ is a bottom element: there is no $y$ with $\neg(0 \le y)$, i.e., every $y$ satisfies $0 \le y$.

- Claim: The structure $(\mathbb{Q}, \le)$ (the rationals) satisfies `VTask.noBotOrderSentence` because for every rational $x$, the rational $x - 1$ satisfies $\neg(x \le x-1)$.

## Boundaries

- The sentence is a **closed** formula (a sentence with no free variables), so it makes sense to ask whether any $L$-structure *models* it without specifying a variable assignment.
- For any structure that has a least element (a bottom element $\bot$ with $\bot \le y$ for all $y$), the sentence is false, because the existential $\exists y,\, \neg(\bot \le y)$ fails.
- For the one-element structure (a single-element order), every element is both top and bottom, so the sentence is false there as well.
- The sentence is logically consistent: it is satisfiable (e.g., by $\mathbb{Z}$) and its negation is also satisfiable (e.g., by $\mathbb{N}$).

## Not to be confused with

- **`noTopOrderSentence`**: the dual sentence $\forall x,\, \exists y,\, \neg(y \le x)$ asserting no top (maximum) element exists, not no bottom.
- **`denselyOrderedSentence`**: the sentence asserting that between any two elements there is a third; a different order-theoretic property.
- **The negation / `hasBot` sentence**: the sentence asserting that a bottom element *does* exist, which is the direct logical negation of this one.