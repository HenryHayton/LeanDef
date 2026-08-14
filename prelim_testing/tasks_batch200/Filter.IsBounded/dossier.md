## Object

`VTask.IsBounded r f` asserts that the filter `f` is *eventually bounded* with respect to the binary relation `r`. Concretely, this means there exists a single element `b` (a "uniform bound") such that, for all elements `x` that `f` eventually produces, the relation `r x b` holds. Intuitively, once you are far enough along in `f`, every element bears the relation `r` to this fixed bound `b`. The typical use-cases are upper boundedness (`r = (· ≤ ·)`, meaning `f` is eventually bounded above) and lower boundedness (`r = (· ≥ ·)`, meaning `f` is eventually bounded below).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsBounded : {α : Type u_1} -> (r : α → α → Prop) -> (f : Filter α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsBounded : {α : Type u_1} -> (r : α → α → Prop) -> (f : Filter α) -> Prop`

The implicit type argument `α` is the carrier type of the filter and the relation. The explicit argument `r` is the binary relation used to define "bounded": an element `x` is bounded by `b` when `r x b` holds. The argument `f` is the filter being tested for eventual boundedness; it encodes the notion of "eventually" or "for large enough" elements.

## Conventions

No special junk-value or boundary conventions are declared for this definition: it is a Prop-valued existential statement that is either true or false depending on the filter and relation supplied, with no edge-case defaults needed.

## Worked examples

- Claim: The `atTop` filter on `ℕ` is NOT eventually bounded above with respect to `(· ≤ ·)`, because no natural number is an upper bound for all sufficiently large naturals.

- Claim: Any principal filter `Filter.principal s` where `s` is a finite set of naturals is eventually bounded above: the filter is eventually inside `s`, and `s` has a maximum element `b`, so `r x b` holds eventually.

- Claim: The `atBot` filter on `ℤ` is eventually bounded above with respect to `(· ≤ ·)`, because `atBot` eventually restricts to elements `x ≤ 0`, so `b = 0` works as a uniform upper bound.

- Claim: For any constant function `u : β → α` with value `a`, the filter `f.IsBoundedUnder (· ≤ ·) u` holds for any filter `f` (by taking the bound to be `a` itself), which in particular means the image filter is `IsBounded (· ≤ ·)`.

## Boundaries

- If `f = ⊥` (the bottom filter, which contains every set), then `VTask.IsBounded r ⊥` holds for *any* relation `r`, because `∀ᶠ x in ⊥, P x` is vacuously true for every predicate `P`.
- If `r` is the total relation `fun _ _ => True`, then `VTask.IsBounded r f` holds for every filter `f`, since any element serves as a bound.
- If `r` is the empty relation `fun _ _ => False`, then `VTask.IsBounded r f` holds only for `f = ⊥`.
- Monotonicity: if `f ≤ g` (i.e. `f` is a finer filter than `g`) and `g` is bounded, then `f` is also bounded. Boundedness can only become easier to satisfy as the filter grows coarser.
- The `atTop` filter on an unbounded-above ordered type is never `IsBounded (· ≤ ·)`.

## Not to be confused with

- `Filter.IsCobounded r f`: asserts that `f` is *cobounded* by `r`, i.e. there exists `b` such that `∀ x, r x b → b ∈ {y | ∀ᶠ z in f, r z y}` — the dual notion, which is distinct and does not follow from `IsBounded` alone.
- `Filter.IsBoundedUnder r f u`: a generalization where boundedness is tested on the image filter `Filter.map u f` rather than on `f` directly; `IsBounded r f` is the special case with the identity function.
- `BddAbove s` / `BddBelow s`: classical set-theoretic upper/lower boundedness of a set `s`, which makes no reference to filters or "eventual" behavior.