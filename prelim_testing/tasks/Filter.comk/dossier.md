## Object

A filter on a type `α` built from a property `p` on sets, where a set `s` belongs to the filter precisely when its complement `sᶜ` satisfies `p`. The idea is: think of `p` as describing "small" or "negligible" sets; then the filter collects all sets whose complement is negligible. The hypotheses ensure that `p` is well-behaved enough (closed under subsets and finite unions, and holds for the empty set) for the resulting collection to form a genuine filter. This constructor is the standard way to build filters like `Filter.cofinite` (where `p` = "is finite").

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comk : {α : Type u_1} -> (p : Set α → Prop) -> (he : p ∅) -> (hmono : ∀ (t : Set α), p t → ∀ s ⊆ t, p s) -> (hunion : ∀ (s : Set α), p s → ∀ (t : Set α), p t → p (s ∪ t)) -> Filter α
<!-- PINNED-SIGNATURE:END -->


`VTask.comk : {α : Type u_1} -> (p : Set α → Prop) -> (he : p ∅) -> (hmono : ∀ (t : Set α), p t → ∀ s ⊆ t, p s) -> (hunion : ∀ (s : Set α), p s → ∀ (t : Set α), p t → p (s ∪ t)) -> Filter α`

The implicit argument `α` is the ambient type on which the filter lives. The argument `p` is the predicate on sets of `α` that characterises which sets are "small" (i.e., eligible to be complements of filter members). The proof `he` asserts that `p` holds for the empty set (the complement of `univ` is empty, so `univ` must be in the filter). The proof `hmono` asserts that `p` is downward closed under inclusion: any subset of a `p`-set also satisfies `p` (ensuring the filter is upward closed). The proof `hunion` asserts that `p` is stable under binary unions (ensuring the filter is closed under binary intersections).

## Conventions

There are no junk-value conventions to declare: the constructor is total and every combination of valid arguments produces a well-formed filter. The three proof arguments are genuine mathematical hypotheses that must hold; they are not mere annotations with fallback behaviour.

## Worked examples

- Claim: A set `s` belongs to `VTask.comk p he hmono hunion` if and only if `p sᶜ` holds — membership is characterised entirely by whether the complement satisfies `p`.

- Claim: The complement of a set `s` belongs to `VTask.comk p he hmono hunion` if and only if `p s` holds directly (without complementing again).

- Claim: Taking `p = Set.Finite`, with `he` = finiteness of `∅`, `hmono` = subsets of finite sets are finite, and `hunion` = unions of two finite sets are finite, the resulting filter `VTask.comk Set.Finite he hmono hunion` is exactly `Filter.cofinite` on `α` — it contains precisely the cofinite sets (those with finite complement).

- Claim: `univ` always belongs to `VTask.comk p he hmono hunion`, because `univᶜ = ∅` and `he : p ∅`.

## Boundaries

- The empty set `∅` never belongs to the filter, because `∅ᶜ = univ` and `p univ` is not assumed. (If `p univ` were to hold, the filter would contain `∅` and be the improper filter; `comk` does not prevent this if the user provides such a `p`.)
- If `p` is identically `True`, then every set belongs to the filter, yielding the improper filter (the top element of the filter lattice).
- If `p` is identically `False` except at `∅`, then only `univ` belongs to the filter, yielding the principal filter at `univ`, which is the bottom element.
- The three proof arguments are checked only for their types; the specific proofs supplied do not affect which filter is constructed (proof irrelevance).

## Not to be confused with

- `Filter.principal s` — builds a filter directly from a set `s` (all supersets of `s`), with no complement involvement.
- `Filter.cofinite` — a specific *instance* of `VTask.comk` using `p = Set.Finite`; `VTask.comk` is the general constructor, not this particular filter.
- `Filter.mk` — the raw record constructor for `Filter`, requiring the user to supply the set of filter-members directly and verify all filter axioms by hand, without the complement-based abstraction.