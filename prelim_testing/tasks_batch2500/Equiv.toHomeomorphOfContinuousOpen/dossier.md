## VTask.toHomeomorphOfContinuousOpen

### Object

Given a set-theoretic bijection between two topological spaces that happens to be continuous and sends open sets to open sets, this construction packages it as a *homeomorphism* — a bicontinuous bijection — witnessing that the two spaces are topologically identical. Concretely, it promotes a bare equivalence of types (with no topological content) together with two separate topological certificates into a single bundled homeomorphism.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toHomeomorphOfContinuousOpen : {X : Type u_1} -> {Y : Type u_2} -> [TopologicalSpace X] -> [TopologicalSpace Y] -> (e : X ≃ Y) -> (h₁ : Continuous ⇑e) -> (h₂ : IsOpenMap ⇑e) -> X ≃ₜ Y
<!-- PINNED-SIGNATURE:END -->


`{X : Type u_1} -> {Y : Type u_2} -> [TopologicalSpace X] -> [TopologicalSpace Y] -> (e : X ≃ Y) -> (h₁ : Continuous ⇑e) -> (h₂ : IsOpenMap ⇑e) -> X ≃ₜ Y`

The implicit type arguments `X` and `Y` are the source and target types; the instance arguments supply their topologies. The argument `e` is the underlying set-equivalence (bijection) between `X` and `Y`. The argument `h₁` is a proof that the forward direction of `e` is continuous as a map of topological spaces. The argument `h₂` is a proof that the forward direction of `e` is an open map, i.e., it sends every open subset of `X` to an open subset of `Y`. The result is a bundled homeomorphism `X ≃ₜ Y`, which includes both the forward continuity and the continuity of the inverse.

### Conventions

No special junk-value or edge-case conventions are declared for this definition: it is a total constructor whose output is fully determined whenever the three input proofs are supplied, and there are no degenerate inputs that would require a conventional default.

### Worked examples

- Claim: For the identity equivalence on any topological space `X`, supplying `continuous_id` and `isOpenMap_id` yields a homeomorphism whose underlying equivalence is the identity.

- Claim: For `X = Y = ℝ` with the standard topology, the equivalence `Equiv.refl ℝ` together with continuity and open-map witnesses for the identity function produces a homeomorphism `ℝ ≃ₜ ℝ` whose `toFun` is the identity.

- Claim: The homeomorphism produced by `VTask.toHomeomorphOfContinuousOpen e h₁ h₂` has the same underlying function as `e`, i.e., for every `x : X`, `(VTask.toHomeomorphOfContinuousOpen e h₁ h₂) x = e x`.

### Boundaries

- The construction requires *both* continuity of `e` *and* the open-map property. Supplying only one of the two is insufficient — an open bijection need not be continuous, and a continuous bijection need not be open (hence the two hypotheses are genuinely independent).
- When `X` and `Y` carry the discrete or indiscrete topology, the hypotheses are trivially satisfied by any bijection, but the constructor still requires them to be explicitly provided.
- The inverse map's continuity is not an input; it is *derived* automatically from the open-map condition, which ensures that the inverse is continuous without any additional assumption.
- There is no restriction on the cardinality or separation axioms of the spaces; the definition is valid for arbitrary topological spaces.

### Not to be confused with

- `Homeomorph.mk` — a lower-level constructor that directly packages a continuous forward map and a continuous inverse; here the inverse continuity is deduced from the open-map hypothesis rather than supplied.
- The analogue using a *closed* map instead of an open map — a continuous bijection that sends closed sets to closed sets also induces a homeomorphism, but that is a distinct construction.
- `Equiv.toHomeomorphOfIsInducing` — an intermediate helper that constructs a homeomorphism from an equivalence that is an inducing map; `VTask.toHomeomorphOfContinuousOpen` reduces to this after deducing the inducing property from continuity and the open-map condition.
