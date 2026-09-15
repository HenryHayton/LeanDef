## Object

`VTask.Rel` is a binary relation on the disjoint union `Σ i, D.U i` of the open sets in a topological gluing datum `D`. Two points `a = ⟨i, x⟩` and `b = ⟨j, y⟩` are related if and only if they are identified by the gluing: concretely, there exists a point in the overlap region `D.V (i, j)` that maps to `x` under the first gluing map and whose image under the transition map then maps to `y` under the second gluing map. Informally, `a` and `b` are related precisely when the canonical maps from each piece into the glued space send them to the same point.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Rel : (D : TopCat.GlueData) -> (a b : (i : D.J) × ↑(D.U i)) -> Prop
<!-- PINNED-SIGNATURE:END -->


The first argument `D` is a topological gluing datum (`TopCat.GlueData`), which packages an index type, a family of open topological spaces `D.U i`, pairwise overlap spaces `D.V (i, j)`, restriction maps `D.f i j`, and transition maps `D.t i j`. The second and third arguments `a` and `b` are points in the disjoint union: each is a dependent pair `⟨i, x⟩` where `i` is an index and `x` is a point of `D.U i`.

## Conventions

The relation is defined via an existential witness in the overlap space; no junk-value or out-of-domain conventions apply because the definition is total over all pairs of points in `Σ i, D.U i`.

## Worked examples

- Claim: `VTask.Rel D` is an equivalence relation for any gluing datum `D`.
  (This is the content of `TopCat.GlueData.rel_equiv`: the relation is reflexive, symmetric, and transitive, making it a genuine equivalence relation on the disjoint union.)

- Claim: If `a = ⟨i, x⟩` and `b = ⟨j, y⟩` satisfy `VTask.Rel D a b`, then in the glued space the canonical inclusion maps satisfy `D.ι i x = D.ι j y`.
  (This is the substance of `TopCat.GlueData.ι_eq_iff_rel`: the relation exactly captures when two points of the disjoint union are sent to the same point in the colimit.)

- Claim: For any point `a : Σ i, D.U i`, `VTask.Rel D a a` holds (reflexivity).
  (Follows from `rel_equiv`, which asserts the full equivalence.)

## Boundaries

- When `a` and `b` lie in the same piece (i.e., `a.1 = b.1 = i`), the relation holds if and only if `a.2 = b.2`, since the diagonal of the overlap `D.V (i, i)` together with the identity-like transition on it reduces to equality.
- When the overlap region `D.V (i, j)` is empty (for distinct `i` and `j`), no witness exists, so `VTask.Rel D ⟨i, x⟩ ⟨j, y⟩` is always `False` in that case.
- The relation is defined for all pairs without any restriction; it is `False` precisely when no gluing-compatible overlap witness can be found.

## Not to be confused with

- `Function.Coequalizer.Rel`: the coequalizer relation on the sigma type used internally to construct the colimit; `VTask.Rel` is the user-facing gluing-identification relation, which agrees with it only up to equivalence generation.
- `Relation.EqvGen (VTask.Rel D)`: the equivalence closure of `VTask.Rel`; since `VTask.Rel D` is already an equivalence relation (`rel_equiv`), this coincides with `VTask.Rel D` itself, but the two are syntactically distinct.
- Setoid equality on the quotient type: the quotient of `Σ i, D.U i` by `VTask.Rel D` is homeomorphic to the glued space, but `VTask.Rel` is a relation on the sigma type, not a `Setoid` instance by name.