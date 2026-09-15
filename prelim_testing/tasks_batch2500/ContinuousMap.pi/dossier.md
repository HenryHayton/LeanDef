## Object

`VTask.pi` constructs the **product map** into a product of topological spaces: given a family of continuous maps `f i : A → X i` (one for each index `i : I`), it produces the single continuous map `A → Π i, X i` that sends each point `a : A` to the tuple `(f i a)_{i ∈ I}`. This is the universal property of a product: a map into a product is the same as a compatible family of maps into the factors.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.pi : {I : Type u_5} -> {A : Type u_6} -> {X : I → Type u_7} -> [TopologicalSpace A] -> [(i : I) → TopologicalSpace (X i)] -> (f : (i : I) → C(A, X i)) -> C(A, (i : I) → X i)
<!-- PINNED-SIGNATURE:END -->


`VTask.pi : {I : Type u_5} -> {A : Type u_6} -> {X : I → Type u_7} -> [TopologicalSpace A] -> [(i : I) → TopologicalSpace (X i)] -> (f : (i : I) → C(A, X i)) -> C(A, (i : I) → X i)`

- `I` is the index type parametrising the family of target spaces.
- `A` is the common source (domain) space shared by all maps in the family.
- `X` is the family of target spaces, indexed by `I`; the product space `Π i, X i` carries the product topology.
- The first instance argument supplies the topology on the source `A`.
- The second instance argument supplies a topology on each factor `X i`.
- `f` is the family of continuous maps: for each index `i`, `f i` is a continuous map from `A` to `X i`.

The result is the continuous map from `A` to `Π i, X i` that evaluates pointwise: it sends `a` to the dependent function `i ↦ f i a`.

## Conventions

No junk-value or boundary conventions are declared for this definition: it is a total constructor on well-typed input and its output is always meaningful when the arguments are supplied.

## Worked examples

- Claim: For `f = fun (i : Fin 2) => ContinuousMap.id ℝ` (a constant family of identity maps), `VTask.pi f` sends any real number `a` to the pair `fun i => a`; in particular `(VTask.pi f) 3 = fun _ => 3`.

- Claim: `VTask.pi (fun (i : Fin 1) => ContinuousMap.const A (0 : ℝ))` is the continuous map that sends every point of `A` to the single-component tuple `fun _ => 0`.

- Claim: Composing `VTask.pi f` with the projection `Function.eval i` recovers `f i`; that is, for all `a : A`, `(VTask.pi f) a i = (f i) a` (this is `pi_eval`).

## Boundaries

- When `I` is empty (`I = Empty` or `I = Fin 0`), `VTask.pi f` is the unique continuous map from `A` to the one-point product space `Π i : Empty, X i ≅ Unit`, regardless of what `f` is (it is vacuously defined).
- When `I` is a single-element type, `VTask.pi f` is essentially the same as `f` itself, up to the canonical homeomorphism `(Π _ : Unit, X ⋆) ≅ X ⋆`.
- The construction is purely pointwise and does not depend on any algebraic or metric structure beyond the topologies; it works for any topological spaces.

## Not to be confused with

- `ContinuousMap.prodMk` (the binary product version `C(A, X) × C(A, Y) → C(A, X × Y)`): this is the special case `I = Fin 2` of `VTask.pi`, but the spelling and arguments differ.
- `ContinuousMap.comp` (composition `C(B, A) → C(A, X) → C(B, X)`): that chains two maps end-to-end, whereas `VTask.pi` fans one map out into multiple targets simultaneously.
- The topological product object `TopCat.pi` or `Pi.topologicalSpace`: those describe the *space* `Π i, X i` with its topology, not the *map* into it.
