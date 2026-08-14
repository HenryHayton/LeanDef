## VTask.bliminf

### Object

The **bounded limit inferior** (bliminf) of a function `u : β → α` along a filter `f` on `β`, restricted to points satisfying a predicate `p : β → Prop`, is the supremum of all values `a` in `α` such that the inequality `a ≤ u x` holds *eventually* along `f` for every `x` where `p x` is true. Informally, it is the largest lower bound that `u` eventually respects, but only paying attention to those `x` that satisfy `p`.

When `p` is identically `True` this reduces to the ordinary `liminf` of `u` along `f`. When `p` is identically `False` the condition `p x → a ≤ u x` is vacuously true for every `a`, so the supremum ranges over all of `α` and equals `⊤`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.bliminf : {α : Type u_1} -> {β : Type u_2} -> [ConditionallyCompleteLattice α] -> (u : β → α) -> (f : Filter β) -> (p : β → Prop) -> α
<!-- PINNED-SIGNATURE:END -->


The first argument `u` is the real-valued (or lattice-valued) function whose eventual lower bound is being measured. The second argument `f` is the filter encoding the "direction" or "limiting regime" along which the asymptotic behaviour is studied. The third argument `p` is the bounding predicate: only the behaviour of `u` at points where `p` holds is taken into account.

### Conventions

When the predicate `p` is identically `False`, every implication `p x → a ≤ u x` is vacuously true for every `x`, so the set over which the supremum is taken equals all of `α`, and `VTask.bliminf u f (fun _ => False) = ⊤`.

### Worked examples

- Claim: `VTask.bliminf u f (fun _ => False) = ⊤` for any `u`, `f` in a conditionally complete lattice, because every lower-bound condition is vacuously satisfied.

- Claim: If `q` implies `p` pointwise (i.e., `∀ x, q x → p x`), then `VTask.bliminf u f p ≤ VTask.bliminf u f q`. Restricting the predicate to a *stronger* condition (fewer points must satisfy it) can only raise or maintain the infimum.

- Claim: If `f ≤ g` (f is a coarser filter than g), then `VTask.bliminf u g p ≤ VTask.bliminf u f p`. A finer filter imposes more restrictive eventual conditions, making it easier for a lower bound `a` to qualify, so bliminf is antitone in the filter argument.

- Claim: `VTask.bliminf u f p ⊓ VTask.bliminf u f (fun x => ¬ p x) = liminf u f`. Splitting the index set by a predicate and its complement, taking the infimum of both bounded liminfs recovers the ordinary liminf of `u` along `f`.

### Boundaries

- **Vacuously false predicate:** When `p = fun _ => False`, the set `{a | ∀ᶠ x in f, p x → a ≤ u x}` equals the whole type `α` (since the implication is always vacuously true), so `VTask.bliminf u f (fun _ => False) = ⊤`.
- **Universally true predicate:** When `p = fun _ => True`, `VTask.bliminf` coincides with the ordinary `liminf u f`.
- **Predicate monotonicity:** Strengthening `p` (replacing it by a logically stronger predicate) weakens the constraint that `a` must satisfy, so `VTask.bliminf` is antitone in `p`: a larger class of points allowed means a larger (or equal) set of qualifying lower bounds.
- **Filter monotonicity:** `VTask.bliminf` is antitone in the filter: passing to a coarser filter (relaxing eventual conditions) can only decrease the bliminf.
- **Conditionally complete lattice:** The codomain only needs to be a `ConditionallyCompleteLattice`; the supremum is defined but may not be realised if the relevant set is empty or unbounded. If the set over which the supremum is taken is empty, the value defaults according to `sSup ∅` in the lattice, which is junk (conventionally `⊥` in a `CompleteLattice`, but may be arbitrary in a mere `ConditionallyCompleteLattice`).

### Not to be confused with

- **`blimsup u f p`** — the *dual* construction: the infimum of all `a` such that `u x ≤ a` eventually holds for `p`-points, i.e., the smallest eventual upper bound restricted to `p`. It satisfies `bliminf u f p ≤ blimsup u f p` in general.
- **`liminf u f`** — the ordinary limit inferior without any predicate restriction; equal to `VTask.bliminf u f (fun _ => True)` and also equal to `VTask.bliminf u f p ⊓ VTask.bliminf u f (fun x => ¬p x)`.
- **`sSup S`** — the bare supremum of a set `S`; `VTask.bliminf` specifically constructs the set `S` from an "eventually for `p`-points" condition before taking the supremum, so it is not just an arbitrary `sSup`.
