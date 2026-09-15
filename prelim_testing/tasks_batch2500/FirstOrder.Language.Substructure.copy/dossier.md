## Object

`VTask.copy` constructs a new first-order substructure of a model `M` (for language `L`) whose carrier set is a given set `s`, under the guarantee that `s` equals the carrier of an already-known substructure `S`. The result is a substructure that is definitionally equal to `S` in every sense except that its carrier field holds `s` rather than `↑S`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {L : FirstOrder.Language} -> {M : Type w} -> [L.Structure M] -> (S : L.Substructure M) -> (s : Set M) -> (hs : s = ↑S) -> L.Substructure M
<!-- PINNED-SIGNATURE:END -->


```
VTask.copy : {L : FirstOrder.Language} -> {M : Type w} -> [L.Structure M] -> (S : L.Substructure M) -> (s : Set M) -> (hs : s = ↑S) -> L.Substructure M
```

The implicit argument `L` is the first-order language. The implicit argument `M` is the ambient model (a type), equipped with an `L`-structure via the instance argument. The explicit argument `S` is the source substructure whose algebraic data (closure under function symbols) is being transferred. The explicit argument `s` is the set that will serve as the carrier of the new substructure. The explicit argument `hs` is a proof that `s` equals the coercion of `S` to a set, justifying why `s` inherits the substructure axioms from `S`.

## Conventions

There are no junk-value or boundary conventions declared for this definition: it is a total operation on well-typed inputs, and no special case produces an arbitrary or degenerate output.

## Worked examples

- Claim: For any substructure `S`, `VTask.copy S ↑S rfl` has the same carrier as `S` itself.

- Claim: An element `m : M` belongs to `VTask.copy S s hs` if and only if it belongs to `S`.

- Claim: `VTask.copy S s hs` and `S` are equal as `L.Substructure M` values whenever `s = ↑S` (i.e., the copy is definitionally the same substructure, just with a potentially syntactically different carrier field).

## Boundaries

- The proof `hs : s = ↑S` must be supplied; without it, `s` could be any set and the closure properties might fail. The definition is not available for arbitrary sets.
- When `s` is literally `↑S` and `hs` is `rfl`, the copy is definitionally equal to `S`.
- The function-membership axioms of the copy are inherited wholesale from `S` via the equality proof, so there is no loss of structure.
- The definition does not check whether `s` itself carries any independent substructure structure; it purely delegates to `S`.

## Not to be confused with

- `L.Substructure.mk` — constructs a substructure from scratch by providing a carrier and all closure proofs directly, rather than delegating to an existing substructure.
- `L.Substructure.comap` / `L.Substructure.map` — produce new substructures via homomorphisms, not by carrier-set substitution.
- Set-theoretic equality of substructures (via `ext`) — asserts that two independently defined substructures have equal carriers, whereas `copy` repackages one substructure under a definitionally equal carrier set.