## Object

`VTask.castLE` is the canonical coercion that embeds a bounded first-order formula with at most `m` free bound-variable slots into the larger type of bounded formulas with at most `n` free bound-variable slots, whenever `m ≤ n`. Concretely, a `BoundedFormula α m` may reference bound variables indexed by `Fin m`; `castLE` re-indexes those bound-variable occurrences along the canonical order-preserving injection `Fin m ↪ Fin n` (given by `Fin.castLE`), producing a logically equivalent formula in `BoundedFormula α n`. The free variables drawn from `α` are left untouched.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.castLE : {L : FirstOrder.Language} -> {α : Type u'} -> {m n : ℕ} -> (_h : m ≤ n) -> L.BoundedFormula α m → L.BoundedFormula α n
<!-- PINNED-SIGNATURE:END -->


VTask.castLE : {L : FirstOrder.Language} -> {α : Type u'} -> {m n : ℕ} -> (_h : m ≤ n) -> L.BoundedFormula α m → L.BoundedFormula α n

- `L` is the first-order language (signature) over which formulas are built; it is inferred implicitly.
- `α` is the type of free (non-bound) variables appearing in the formula; it is inferred implicitly.
- `m` is the number of bound-variable slots available in the *source* formula type; it is inferred implicitly.
- `n` is the number of bound-variable slots available in the *target* formula type; it is inferred implicitly.
- `_h` is a proof that `m ≤ n`, which justifies the embedding; it is typically supplied as an underscore or inferred.
- The final argument is the source bounded formula of type `L.BoundedFormula α m` being coerced.

## Conventions

The cast is the identity when `m = n`: applying `VTask.castLE` with a proof of `n ≤ n` returns the formula unchanged.

## Worked examples

- Claim: Casting the formula `falsum : L.BoundedFormula α m` along any `m ≤ n` yields `falsum : L.BoundedFormula α n`.

- Claim: `VTask.castLE` composes transitively — casting first along `k ≤ m` and then along `m ≤ n` gives the same result as casting directly along `k ≤ n` (i.e., `castLE mn ∘ castLE km = castLE (km.trans mn)`).

- Claim: If a formula is atomic (a `BoundedFormula.IsAtomic` instance), its image under `VTask.castLE` is also atomic.

- Claim: If a formula is in prenex normal form (`BoundedFormula.IsPrenex`), its image under `VTask.castLE` is also in prenex normal form.

## Boundaries

- **Reflexive case (`m = n`):** `VTask.castLE h φ = φ` holds definitionally up to the fact that `Fin.castLE (le_refl n)` is the identity on `Fin n`; the named lemma `castLE_rfl` records this equality.
- **Transitive composition:** The two-step cast `(φ.castLE km).castLE mn` equals the single-step cast `φ.castLE (km.trans mn)`; no information is lost or duplicated by composing casts.
- **Semantic content is preserved:** Although the syntactic type changes, the formula's truth value under any interpretation is unchanged: bound variables in the target are read off the prefix of length `m` of any `Fin n`-indexed tuple, exactly as the source formula used its `Fin m`-indexed tuple.
- **Free variables are unaffected:** The coercion does not alter the `α`-typed free variables in any way; only the `Fin`-indexed bound-variable slots are re-indexed.
- **The `all` quantifier increments the bound count:** When casting `all f` (which has type `BoundedFormula α (m+1)` from a sub-formula of type `BoundedFormula α m`), the proof obligation shifts correspondingly, so the cast recurses with a compatible proof.

## Not to be confused with

- `FirstOrder.Language.BoundedFormula.relabel` — relabels *free* variables (the `α` component) rather than re-indexing bound-variable slots.
- `FirstOrder.Language.Term.castLE` — performs the analogous re-indexing for *terms* rather than *formulas*.
- `FirstOrder.Language.BoundedFormula.liftAt` — inserts fresh bound-variable slots at a specific position in the middle of the index range, rather than extending from the top.