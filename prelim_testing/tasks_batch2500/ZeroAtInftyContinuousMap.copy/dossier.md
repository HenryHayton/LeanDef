## Object

`VTask.copy` constructs a new zero-at-infinity continuous map from an existing one by replacing its underlying function with a provably equal function. The result is bundled as a `ZeroAtInftyContinuousMap` carrying the same continuity and zero-at-infinity properties as the original, but whose definitional presentation of the underlying function is `f'` rather than `⇑f`. This is a purely bureaucratic operation: mathematically the output is the same map; the point is to give it a different syntactic form that may be more convenient in certain proof contexts.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {α : Type u} -> {β : Type v} -> [TopologicalSpace α] -> [TopologicalSpace β] -> [Zero β] -> (f : ZeroAtInftyContinuousMap α β) -> (f' : α → β) -> (h : f' = ⇑f) -> ZeroAtInftyContinuousMap α β
<!-- PINNED-SIGNATURE:END -->


The implicit arguments `α` and `β` are the domain and codomain types, equipped respectively with topological-space structures (also implicit); `β` additionally carries a distinguished zero element. The argument `f` is the zero-at-infinity continuous map being copied. The argument `f'` is the new underlying bare function that will appear as the `toFun` field of the result. The argument `h` is a proof that `f'` is definitionally/propositionally equal to the coercion of `f` to a bare function; this equality is what lets the copy inherit `f`'s continuity and zero-at-infinity witnesses.

## Conventions

There are no junk-value or out-of-domain conventions to declare: the definition is total and every input satisfying the type signature is meaningful. The proof `h` is the only constraint, and it is part of the type itself rather than a domain restriction.

## Worked examples

- Claim: For any `f : ZeroAtInftyContinuousMap α β`, `VTask.copy f (⇑f) rfl` has the same underlying function as `f`, namely `⇑f`.

- Claim: `⇑(VTask.copy f f' h) = f'` — the coercion of the copy to a bare function is exactly `f'`, the replacement function supplied by the caller.

- Claim: `VTask.copy f (⇑f) rfl = f` — copying `f` with its own coercion and a reflexivity proof returns a zero-at-infinity continuous map equal to `f`.

## Boundaries

- The proof `h` must be propositional equality `f' = ⇑f`; it cannot merely be a pointwise equality of functions — full function equality is required.
- Because `h` guarantees `f' = ⇑f`, the result is always equal to the original map `f` as a `ZeroAtInftyContinuousMap` (this is the content of `copy_eq`); there is no regime in which the copy differs from the original as a map.
- There is no restriction on `α` or `β` beyond those already in the type signature (topological spaces, zero on `β`); in particular neither space needs to be locally compact, Hausdorff, or otherwise special for `VTask.copy` to be well-formed.

## Not to be confused with

- `ZeroAtInftyContinuousMap.mk` / the structure constructor: that builds a zero-at-infinity continuous map from scratch by supplying continuity and zero-at-infinity proofs directly, without reusing an existing map's witnesses.
- `ContinuousMap.copy`: an analogous utility on plain (not zero-at-infinity) continuous maps; it does not carry the zero-at-infinity condition.
- Pointwise extension or restriction: `VTask.copy` does not change the values of the map on any point; it only changes the syntactic form of the underlying function field.