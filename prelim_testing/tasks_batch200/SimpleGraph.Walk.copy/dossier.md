## Object

`VTask.copy` transports a walk in a simple graph along equalities of its endpoints. Given a walk from `u` to `v`, and proofs that `u = u'` and `v = v'`, it produces a walk from `u'` to `v'` that is the same walk with its endpoint types adjusted. The result is propositionally and definitionally the same path; only the *type-level* labels of the start and end vertices change. This operation is the canonical way in Mathlib to reconcile walks whose endpoints are provably but not definitionally equal.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {V : Type u} -> {G : SimpleGraph V} -> {u v u' v' : V} -> (p : G.Walk u v) -> (hu : u = u') -> (hv : v = v') -> G.Walk u' v'
<!-- PINNED-SIGNATURE:END -->


```
VTask.copy : {V : Type u} -> {G : SimpleGraph V} -> {u v u' v' : V} -> (p : G.Walk u v) -> (hu : u = u') -> (hv : v = v') -> G.Walk u' v'
```

The implicit argument `V` is the type of vertices. The implicit argument `G` is the simple graph on `V`. The implicit arguments `u`, `v` are the original start and end vertices of the walk, while `u'`, `v'` are the desired new start and end vertices. The explicit argument `p` is the walk to be transported. The argument `hu` is the proof that the old start vertex equals the new start vertex. The argument `hv` is the proof that the old end vertex equals the new end vertex.

## Conventions

When both endpoint equalities are `rfl`, `VTask.copy` returns the walk unchanged: `p.copy rfl rfl = p`. The simp-normal form pushes `copy` outward through walk constructors (cons, append, etc.), so that rewriting and calculation happen inside the copy context rather than around it.

## Worked examples

- Claim: Copying a walk with `rfl` proofs for both endpoints yields the original walk.

- Claim: Copying the nil walk at vertex `u` along a proof `hu : u = u'` and the same proof yields the nil walk at `u'`.

- Claim: For a cons walk `cons h p`, copying with equalities `hu` and `hw` gives `cons (hu ▸ h) (p.copy rfl hw)`, i.e., the copy distributes into the cons, adjusting the adjacency proof and recursively copying the tail.

- Claim: Appending two copied walks `(p.copy hu hv).append (q.copy hv hw)` equals `(p.append q).copy hu hw`, showing copy and append commute in the expected way.

## Boundaries

- When `hu = rfl` and `hv = rfl`, the operation is definitionally the identity, and `p.copy rfl rfl = p` holds by the theorem `copy_rfl_rfl`.
- Copying the nil walk `Walk.nil` at `u` with `hu : u = u'` and `hu : u = u'` yields `Walk.nil` at `u'`.
- The function is total: it is defined for all walks and all equality proofs, with no restrictions.
- Because `copy` is merely transport along equalities, it does not alter the length, edges, or vertex sequence of the walk — only its endpoint types.

## Not to be confused with

- `SimpleGraph.Walk.transfer`: transfers a walk from one graph to another (rather than just relabelling endpoints within the same graph).
- `SimpleGraph.Walk.map`: applies a graph homomorphism to a walk, changing both the vertex type and the graph, not just endpoint labels.
- `Eq.mpr` / `Eq.rec` used directly on walk types: `VTask.copy` is the canonical, simp-friendly wrapper around such transport, providing predictable normal forms.