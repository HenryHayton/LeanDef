## Object

`VTask.lift` constructs a bounded group homomorphism from a seminormed abelian group `V₁` into the **equalizer** of two bounded group homomorphisms `f, g : V → W`. The equalizer of `f` and `g` is the subgroup of `V` consisting of those elements on which `f` and `g` agree (i.e., elements `v` with `f(v) = g(v)`). Given a morphism `φ : V₁ → V` that already satisfies `f ∘ φ = g ∘ φ` (meaning every element in the image of `φ` lies in the equalizer), this construction produces the canonically induced morphism into the equalizer subgroup, together with a norm bound inherited from `φ`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lift : {V : Type u_1} -> {W : Type u_2} -> {V₁ : Type u_3} -> [SeminormedAddCommGroup V] -> [SeminormedAddCommGroup W] -> [SeminormedAddCommGroup V₁] -> {f g : NormedAddGroupHom V W} -> (φ : NormedAddGroupHom V₁ V) -> (h : f.comp φ = g.comp φ) -> NormedAddGroupHom V₁ ↥(f.equalizer g)
<!-- PINNED-SIGNATURE:END -->


VTask.lift : {V : Type u_1} -> {W : Type u_2} -> {V₁ : Type u_3} -> [SeminormedAddCommGroup V] -> [SeminormedAddCommGroup W] -> [SeminormedAddCommGroup V₁] -> {f g : NormedAddGroupHom V W} -> (φ : NormedAddGroupHom V₁ V) -> (h : f.comp φ = g.comp φ) -> NormedAddGroupHom V₁ ↥(f.equalizer g)

The three implicit universe-polymorphic type arguments `V`, `W`, and `V₁` are the underlying seminormed abelian groups: `V` is the domain shared by `f` and `g`; `W` is their common codomain; `V₁` is the source group from which the morphism `φ` originates. The implicit arguments `f` and `g` are the two parallel bounded group homomorphisms whose equalizer is the target subgroup. The explicit argument `φ` is the bounded group homomorphism from `V₁` into `V` whose image (after composing with both `f` and `g`) coincides, as witnessed by the proof `h` that `f.comp φ = g.comp φ`. The proof `h` is exactly the condition ensuring that every element of `V₁` maps, under `φ`, into the equalizer of `f` and `g`.

## Conventions

There are no junk-value or edge-case conventions to declare: the construction is total and well-defined for all inputs satisfying the stated type constraints; the proof obligation `h` is part of the function's data and fully determines the codomain subgroup.

## Worked examples

- Claim: For `f = g` (so `h` is trivial), `VTask.lift φ h` is a morphism into the full equalizer `f.equalizer f`, and its operator norm satisfies `‖VTask.lift φ h‖ ≤ ‖φ‖`.

- Claim: If `φ` is norm-nonincreasing (i.e., `‖φ v‖ ≤ ‖v‖` for all `v`) and `f.comp φ = g.comp φ`, then `VTask.lift φ h` is also norm-nonincreasing as a morphism into the equalizer.

- Claim: For any `φ` and proof `h`, the underlying map of `VTask.lift φ h` sends `v : V₁` to the element `⟨φ v, _⟩` of the equalizer subgroup, so applying `VTask.lift φ h` and then projecting back to `V` recovers `φ v`.

## Boundaries

- The definition requires the hypothesis `h : f.comp φ = g.comp φ` as an actual argument; without it the image of `φ` need not land in the equalizer and no such morphism can be formed.
- When `φ` is the zero morphism, `VTask.lift φ h` is the zero morphism into the equalizer (by linearity).
- The norm of `VTask.lift φ h` is at most that of `φ` (since the equalizer subgroup carries the subspace norm from `V`); equality need not hold in general.
- If `f = g`, the equalizer is all of `V` and `VTask.lift φ h` is essentially the same morphism as `φ` (up to the isomorphism of `V` with `f.equalizer f`).
- The construction works uniformly for all seminormed abelian groups, including the degenerate case where `V₁`, `V`, or `W` is the zero group.

## Not to be confused with

- `NormedAddGroupHom.Equalizer.ι`: the inclusion of the equalizer subgroup back into `V`; this goes in the opposite direction from `VTask.lift`.
- `NormedAddGroupHom.comp`: plain composition of two bounded group homomorphisms without any equalizer structure; `VTask.lift` factors `φ` specifically through a subgroup.
- `NormedAddGroupHom.equalizer`: the equalizer subgroup itself as an `AddSubgroup` object, not the induced morphism into it.