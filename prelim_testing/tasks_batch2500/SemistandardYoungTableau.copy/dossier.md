## Object

`VTask.copy` constructs a semistandard Young tableau on a given Young diagram shape `μ` by packaging a given entry function together with a proof that it equals the coercion of an already-known semistandard Young tableau. The resulting tableau is definitionally equal to the original, but uses the supplied function as its entry map. This is primarily a bookkeeping device: it allows one to swap in a definitionally different (but provably equal) representation of the entry function while preserving all the semistandard conditions (weakly increasing along rows, strictly increasing down columns, zero outside the diagram).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {μ : YoungDiagram} -> (T : SemistandardYoungTableau μ) -> (entry' : ℕ → ℕ → ℕ) -> (h : entry' = ⇑T) -> SemistandardYoungTableau μ
<!-- PINNED-SIGNATURE:END -->


The implicit argument `μ` is the Young diagram that specifies the shape (set of cells) of the tableau. The argument `T` is the source semistandard Young tableau whose conditions are inherited. The argument `entry'` is the new entry function (a map `ℕ → ℕ → ℕ` assigning a natural number to each row-column pair) that will be used in the result. The argument `h` is a proof that `entry'` is equal to the coercion of `T` to a function; this equality is what justifies transferring all semistandard conditions from `T` to the copy.

## Conventions

There are no junk-value or edge conventions to declare: the definition is total and every argument is constrained by the type or the explicit equality proof `h`, leaving no room for undefined or arbitrary behaviour at boundary inputs.

## Worked examples

- Claim: For any semistandard Young tableau `T` on shape `μ`, `VTask.copy T (⇑T) rfl` equals `T` as a semistandard Young tableau (the `copy_eq` fact).

- Claim: For any semistandard Young tableau `T` on shape `μ`, the coercion of `VTask.copy T (⇑T) rfl` to a function equals `⇑T` (the `coe_copy` fact).

## Boundaries

- The only admissible `entry'` values are those provably equal to `⇑T`; the proof `h` enforces this at the type level, so there is no possibility of supplying a genuinely different entry function.
- When `entry' = ⇑T` (as required), the copy is propositionally equal to `T` and its coercion is `entry'`. No information is lost or changed.
- Because `μ` may be the empty Young diagram, the construction works on the trivial tableau just as well as on any other shape.

## Not to be confused with

- A generic record-update or `mk` constructor for semistandard Young tableaux: those require re-supplying and re-verifying all semistandard conditions independently, whereas `VTask.copy` inherits them automatically via the equality proof.
- Standard Young tableaux copy operations: those live on a different type (entries are a bijection with `{1,…,n}`, strict in both directions) and are unrelated.
- The coercion `⇑T` itself: that is just a plain function `ℕ → ℕ → ℕ`, not a bundled semistandard Young tableau.