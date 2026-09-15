## Object

`VTask.copy` produces a new subsemigroup of a multiplicative semigroup `M` that is identical in all structural respects to a given subsemigroup `S`, but whose underlying carrier set is replaced by a (definitionally distinct yet propositionally equal) set `s`. The result is a subsemigroup with carrier `s` and the same closure under multiplication as `S`, justified by the proof that `s` and the carrier of `S` are the same set.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {M : Type u_1} -> [Mul M] -> (S : Subsemigroup M) -> (s : Set M) -> (hs : s = ↑S) -> Subsemigroup M
<!-- PINNED-SIGNATURE:END -->


The implicit argument `M` is the ambient type, which carries a multiplication. The instance `[Mul M]` supplies that multiplication. `S` is the source subsemigroup being copied. `s` is the set that will serve as the carrier of the returned subsemigroup. `hs` is a proof that `s` equals the coercion of `S` to a plain set (i.e., the carrier of `S`); it is the logical bridge that allows the multiplication-closure property to be transferred.

## Conventions

No special junk-value or edge conventions have been declared for this definition: it is a total function whose output is fully determined whenever the inputs are well-typed, and no boundary inputs produce degenerate or silently-defaulted outputs.

## Worked examples

- Claim: For any subsemigroup `S` of a semigroup `M`, `VTask.copy S ↑S rfl` has the same carrier as `S`.

- Claim: For any subsemigroup `S` and any set `s` with a proof `hs : s = ↑S`, every element `x` belongs to `VTask.copy S s hs` if and only if `x` belongs to `S`.

- Claim: For any subsemigroup `S` and proof `hs : ↑S = ↑S`, `VTask.copy S ↑S rfl` equals `S` as a `Subsemigroup`.

## Boundaries

- The function is total: it is defined for every subsemigroup `S`, every set `s`, and every proof `hs`. There are no inputs for which the function is undefined or produces a fallback value.
- The set `s` must be propositionally equal to the carrier of `S` (enforced by `hs`), so the copy cannot silently change the mathematical content of the subsemigroup.
- When `s` is literally `↑S` and `hs` is `rfl`, the copy is the simplest possible duplication: it reproduces `S` with the same carrier representation.
- The copy is definitionally a `Subsemigroup` (not merely a `Set`), so it satisfies all subsemigroup axioms automatically.

## Not to be confused with

- `Subsemigroup.closure`: builds the *smallest* subsemigroup containing a given set, which may be larger than that set; `VTask.copy` does not expand the carrier at all.
- `Submonoid.copy`: the analogous operation for submonoids, which additionally requires a unit element and thus applies only in the monoid setting.
- Set-level coercion `↑S : Set M`: merely extracts the underlying set of `S` without producing a new `Subsemigroup` structure.