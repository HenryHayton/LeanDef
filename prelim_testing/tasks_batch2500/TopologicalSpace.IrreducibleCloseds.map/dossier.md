## Object

Given a continuous map `f : β → α` between topological spaces, `VTask.map f hf c` produces the irreducible closed subset of `α` that is the **closure of the direct image** `f(c)`, where `c` is an irreducible closed subset of `β`. This construction defines the covariant functorial action of continuous maps on the poset of irreducible closed sets (the underlying point set of the Alexandrov-style spectral space).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.map : {α : Type u_2} -> {β : Type u_3} -> [TopologicalSpace α] -> [TopologicalSpace β] -> (f : β → α) -> (hf : Continuous f) -> (c : TopologicalSpace.IrreducibleCloseds β) -> TopologicalSpace.IrreducibleCloseds α
<!-- PINNED-SIGNATURE:END -->


The first argument `f` is the underlying continuous map from `β` to `α`. The second argument `hf` is the proof that `f` is continuous. The third argument `c` is an irreducible closed subset of `β` whose image is to be pushed forward.

## Conventions

No special junk-value or boundary conventions are declared for this definition: the map is total and well-defined whenever the inputs satisfy the stated types, and there are no degenerate edge inputs that receive a non-obvious prescribed value.

## Worked examples

- Claim: For the identity map `id : α → α` with continuity proof `continuous_id`, `VTask.map id continuous_id c` has the same carrier as `c` (i.e., the closure of the image of an irreducible closed set under the identity is the set itself, since it is already closed).

- Claim: For a constant map `f : β → α` sending everything to a fixed closed point `x`, `VTask.map f hf c` has carrier equal to `{x}` (the closure of the singleton `{f(b)}` for any `b ∈ c`, which is the closure of `{x}`).

- Claim: For composable continuous maps `g : γ → β` and `f : β → α`, the carrier of `VTask.map f hf (VTask.map g hg c)` equals the carrier of `VTask.map (f ∘ g) (hf.comp hg) c`, because closure of closure of image equals closure of image under composition.

## Boundaries

- If `c` is the whole space `β` (viewed as an irreducible closed set, when `β` is irreducible), then the result is the closure of `f(β)`, which is the closure of the image of `f`.
- If `c` is a singleton irreducible closed set `{b}` (the closure of a point), then the result is the closure of `{f(b)}` in `α`, i.e., the irreducible closed set associated to the point `f(b)`.
- The closure step is essential: the direct image of a closed set under a continuous map need not be closed, but its closure is always closed; the irreducibility of the closure follows from the irreducibility of the image, which in turn follows from the irreducibility of `c` and continuity of `f`.

## Not to be confused with

- `TopologicalSpace.IrreducibleCloseds.comap`-style constructions: the present map goes **covariant** (forward along `f`), not contravariant.
- Taking the direct image `f '' c` without closing: that set is irreducible but not necessarily closed, so it is not itself an element of `IrreducibleCloseds α`.
- The Zariski-topology generic point map: while related in spirit (both track irreducible closed sets), the generic-point correspondence requires a sober space and is an equivalence, whereas `VTask.map` is defined for any continuous map between arbitrary topological spaces.