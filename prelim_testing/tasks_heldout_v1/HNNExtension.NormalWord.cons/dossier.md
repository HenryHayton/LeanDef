## Object

`VTask.cons` constructs a new normal word in the sense of the HNN extension theory by prepending a group element `g` and a stable-letter exponent `u` to an existing normal word `w`. The resulting word has `g` as its new head, followed by the letter `t^u`, followed by `w.head`, and then the rest of `w`'s letter sequence. The two hypotheses guarantee that this concatenation is already in normal form — that is, no Britton-lemma cancellation occurs and the transversal conditions are met at each position — so no further reduction or normalization is needed.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.cons : {G : Type u_1} -> [Group G] -> {A B : Subgroup G} -> {d : HNNExtension.NormalWord.TransversalPair G A B} -> (g : G) -> (u : ℤˣ) -> (w : HNNExtension.NormalWord d) -> (h1 : w.head ∈ d.set u) -> (h2 : ∀ u' ∈ Option.map Prod.fst w.toList.head?, w.head ∈ HNNExtension.toSubgroup A B u → u = u') -> HNNExtension.NormalWord d
<!-- PINNED-SIGNATURE:END -->


`VTask.cons : {G : Type u_1} -> [Group G] -> {A B : Subgroup G} -> {d : HNNExtension.NormalWord.TransversalPair G A B} -> (g : G) -> (u : ℤˣ) -> (w : HNNExtension.NormalWord d) -> (h1 : w.head ∈ d.set u) -> (h2 : ∀ u' ∈ Option.map Prod.fst w.toList.head?, w.head ∈ HNNExtension.toSubgroup A B u → u = u') -> HNNExtension.NormalWord d`

- `G` is the ambient group.
- `A` and `B` are the two subgroups involved in the HNN extension (the associated subgroups for the stable letter).
- `d` is the transversal pair, which specifies chosen coset representatives for `A` and `B` with respect to the stable letter `t`.
- `g` is the group element prepended as the new head of the word.
- `u` is the exponent of the stable letter (`t^u`, where `u = 1` or `u = -1` since `u : ℤˣ`) inserted between `g` and the old word.
- `w` is the existing normal word to which `g` and `t^u` are prepended.
- `h1` is the proof that `w.head` (the current head of `w`) lies in the transversal set prescribed by `u`; this ensures the pair `(t^u, w.head)` meets the transversal condition.
- `h2` is the non-cancellation hypothesis: it states that if the first letter of `w`'s letter list has exponent `u'`, and `w.head` lies in the appropriate subgroup `toSubgroup A B u`, then `u = u'` — preventing Britton-style cancellation between the newly inserted `t^u` and the first existing stable letter of `w`.

## Conventions

There are no junk-value conventions for this definition: every argument is constrained by explicit type or hypothesis, so all inputs satisfying the stated types and propositions produce a well-formed normal word. The constructor is total on its stated domain.

## Worked examples

- Claim: The product of `VTask.cons g u w h1 h2` in the HNN extension equals `of g * (t ^ (u : ℤ) * w.prod φ)`, confirming that prepending `g` and `t^u` multiplies on the left by `of g` and `t^u` in sequence.

- Claim: Acting by `g₁` (via the scalar action on normal words) on `VTask.cons g₂ u w h1 h2` yields `VTask.cons (g₁ * g₂) u w h1 h2`, so left-multiplication by a group element only affects the head.

- Claim: The non-cancellation hypothesis `h2` is equivalent to the assertion that no Britton cancellation occurs at the junction, i.e., `¬ Cancels u w` follows from `h2` alone.

- Claim: Applying the `consRecOn` recursion principle to `VTask.cons g u w h1 h2` with cases `ofGroup` and `cons` reduces to the `cons` branch applied to `g`, `u`, `w`, `h1`, `h2`, and the recursion result on `w`.

## Boundaries

- If `w` is the trivial (empty) word (constructed via `ofGroup 1`), then `w.toList` is empty, so the head of `w.toList` does not exist. In this case `h2` is vacuously satisfied (there is no first letter to cancel with), and `h1` is the only substantive condition.
- The exponent `u : ℤˣ` can only be `1` or `-1`, so there are exactly two cases for the stable letter direction.
- If `w.head` does not lie in `d.set u`, hypothesis `h1` cannot be proved and the constructor cannot be invoked; the word would not be in normal form.
- The constructor does not attempt any normalization: it is the caller's responsibility to supply `h1` and `h2` proving the word is already normal. If those conditions are not met, the term cannot be formed.

## Not to be confused with

- `HNNExtension.NormalWord.ofGroup`: constructs a normal word from a single group element with no stable letters, i.e., the base case of the word structure.
- `HNNExtension.NormalWord.mulNormalWord` (or the `smul` action): left-multiplies the head of an existing normal word by a group element, without inserting a new stable letter.
- The raw `NormalWord` structure itself: the struct bundles a head, a list of `(ℤˣ, G)` pairs, and proofs of the transversal and chain conditions; `VTask.cons` is a smart constructor that builds such a structure by prepending one pair.