## Object

`VTask.trans'` constructs the composition of two open partial homeomorphisms when the target of the first map and the source of the second map are literally equal (as sets). Given an open partial homeomorphism `e : X ⇀ Y` and another `e' : Y ⇀ Z`, their composition is the open partial homeomorphism `X ⇀ Z` whose underlying partial equivalence is the sequential composition, whose source is the (open) source of `e`, whose target is the (open) target of `e'`, and whose forward and inverse maps are continuous on their respective domains by chaining the continuity of the two constituent maps.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.trans' : {X : Type u_1} -> {Y : Type u_3} -> {Z : Type u_5} -> [TopologicalSpace X] -> [TopologicalSpace Y] -> [TopologicalSpace Z] -> (e : OpenPartialHomeomorph X Y) -> (e' : OpenPartialHomeomorph Y Z) -> (h : e.target = e'.source) -> OpenPartialHomeomorph X Z
<!-- PINNED-SIGNATURE:END -->


`VTask.trans' : {X : Type u_1} -> {Y : Type u_3} -> {Z : Type u_5} -> [TopologicalSpace X] -> [TopologicalSpace Y] -> [TopologicalSpace Z] -> (e : OpenPartialHomeomorph X Y) -> (e' : OpenPartialHomeomorph Y Z) -> (h : e.target = e'.source) -> OpenPartialHomeomorph X Z`

The three implicit type arguments `X`, `Y`, `Z` are the topological spaces involved; each carries an implicit topological-space instance. The argument `e` is the first open partial homeomorphism, mapping (partially) from `X` to `Y`. The argument `e'` is the second open partial homeomorphism, mapping (partially) from `Y` to `Z`. The argument `h` is the proof that the target set of `e` is definitionally equal to the source set of `e'`; this matching condition is what makes direct sequential composition possible without any restriction or coercion.

## Conventions

No junk-value or edge conventions apply to this definition: it is a total function on all well-typed inputs, and there is no distinguished degenerate case with a special-cased output. The result is fully determined by assembling the components of `e` and `e'` in the natural way whenever the hypothesis `h` is satisfied.

## Worked examples

- Claim: For any open set `s` in a topological space `X` with associated identity-like open partial homeomorphism `e = ofSet s hs`, composing `e` with any open partial homeomorphism `f : X ⇀ Z` whose source equals `s` via `VTask.trans' e f h` yields an open partial homeomorphism whose source is `s` and whose target is `f.target`.

- Claim: If `e : OpenPartialHomeomorph X Y` and `e' : OpenPartialHomeomorph Y Z` satisfy `e.target = e'.source`, then `(VTask.trans' e e' h).source = e.source`.

- Claim: If `e : OpenPartialHomeomorph X Y` and `e' : OpenPartialHomeomorph Y Z` satisfy `e.target = e'.source`, then `(VTask.trans' e e' h).target = e'.target`.

## Boundaries

- The hypothesis `h : e.target = e'.source` is required to be an exact propositional equality, not merely a set equivalence or inclusion; without this, the composition cannot be formed by this function.
- If `e.target` (= `e'.source`) is the empty set, the composition is an open partial homeomorphism whose source and target are both open (possibly empty, which is open), and the result is still a valid open partial homeomorphism on the empty domain.
- If `e` is the identity on all of `X` and `e'` is any open partial homeomorphism from `X` to `Z`, the composition recovers `e'` (up to source/target matching).
- The openness of the source of the composed map comes from the openness of `e`'s source; the openness of the target comes from the openness of `e'`'s target.

## Not to be confused with

- `OpenPartialHomeomorph.trans` — the general composition of two open partial homeomorphisms, which does not require an exact equality of target and source but instead intersects/restricts as needed; `VTask.trans'` is the stricter variant requiring exact set equality.
- `PartialEquiv.trans'` — the underlying purely set-theoretic / combinatorial composition of partial equivalences under the same target-equals-source hypothesis, without any topological content.
- `OpenPartialHomeomorph.restr` — restriction of an open partial homeomorphism to a smaller open set, a different operation that changes the domain rather than composing two maps end-to-end.