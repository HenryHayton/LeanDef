## VTask.lift

### Object

Given a directed system of abelian groups — a family of abelian groups indexed by a preordered set, together with additive group homomorphisms between them that are compatible with the ordering — the direct limit is the universal abelian group that the system maps into. `VTask.lift` embodies the **universal property** of that direct limit: if one has a compatible family of homomorphisms from each component group into some target abelian group `P` (meaning the maps respect the transition homomorphisms of the directed system), then there is a unique additive group homomorphism from the direct limit into `P` through which all the component maps factor. `VTask.lift` constructs that canonical map.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lift : {ι : Type u_2} -> [Preorder ι] -> (G : ι → Type u_3) -> [(i : ι) → AddCommMonoid (G i)] -> (f : (i j : ι) → i ≤ j → G i →+ G j) -> [DecidableEq ι] -> (P : Type u_4) -> [AddCommMonoid P] -> (g : (i : ι) → G i →+ P) -> (Hg : ∀ (i j : ι) (hij : i ≤ j) (x : G i), (g j) ((f i j hij) x) = (g i) x) -> AddCommGroup.DirectLimit G f →+ P
<!-- PINNED-SIGNATURE:END -->


```
VTask.lift : {ι : Type u_2} -> [Preorder ι] -> (G : ι → Type u_3) -> [(i : ι) → AddCommMonoid (G i)] -> (f : (i j : ι) → i ≤ j → G i →+ G j) -> [DecidableEq ι] -> (P : Type u_4) -> [AddCommMonoid P] -> (g : (i : ι) → G i →+ P) -> (Hg : ∀ (i j : ι) (hij : i ≤ j) (x : G i), (g j) ((f i j hij) x) = (g i) x) -> AddCommGroup.DirectLimit G f →+ P
```

The implicit type `ι` is the indexing type for the directed system, equipped with a preorder. `G` is the family of abelian groups indexed by `ι`, one for each index `i`. The family `f` provides the **transition maps**: for indices `i ≤ j`, `f i j hij` is the additive homomorphism from `G i` to `G j`, forming the directed system. `P` is the **target** abelian group into which we wish to map. The family `g` supplies a homomorphism `g i : G i →+ P` for each index `i`; these are the component maps from each piece of the system into `P`. The proof `Hg` is the **compatibility condition**: for all `i ≤ j` and `x : G i`, applying the transition map `f i j hij` to `x` and then mapping by `g j` yields the same result as mapping `x` directly by `g i`. The output is an additive group homomorphism from the direct limit of `G` under `f` into `P`.

### Conventions

The direct limit `AddCommGroup.DirectLimit G f` is the target of the component maps `of G f i : G i →+ DirectLimit G f`, and `VTask.lift` is characterized by the property that composing it with any `of G f i` recovers `g i`. No junk-value conventions are declared: the function is well-defined and total whenever the given compatibility condition `Hg` holds, and the universal map is uniquely determined by the component data.

### Worked examples

- Claim: For any compatible family `g` and compatible element `x` in component `G i`, the lift evaluated at the image of `x` under the canonical map `of G f i` equals `g i x`. That is, `VTask.lift G f P g Hg (of G f i x) = g i x` holds universally — this is the defining factoring property.

- Claim: If each component map `g i` is injective and the index type is directed, then `VTask.lift G f P g Hg` is injective as a homomorphism from the direct limit into `P`.

- Claim: The lift is the **unique** such homomorphism: if `F : DirectLimit G f →+ P` is any homomorphism with the property that for all `i` and `x`, `F (of G f i x) = g i x`, then `F` equals `VTask.lift G f P g Hg`. In particular, `VTask.lift G f _ (fun i => F.comp (of G f i)) _ = F` for any `F`.

### Boundaries

- If the compatibility condition `Hg` fails for some `i ≤ j` and some `x`, the data would not define a well-posed map out of the direct limit (elements in the direct limit are equivalence classes that conflate `x` in `G i` with `f i j hij x` in `G j`); however, the term `VTask.lift` still type-checks since `Hg` is a proof argument the user must supply.
- When `ι` has a single element (trivial directed system), the direct limit is isomorphic to the single group `G *`, and `VTask.lift` specializes to the unique homomorphism `g *`.
- When the family `g` consists entirely of zero maps and `Hg` holds trivially, `VTask.lift` produces the zero homomorphism.
- The output is an `AddMonoidHom` (additive group homomorphism), not merely a function; it preserves the group structure by construction.

### Not to be confused with

- `AddCommGroup.DirectLimit.of`: the canonical inclusions `G i →+ DirectLimit G f` going *into* the direct limit, rather than out of it.
- `Module.DirectLimit.lift`: the analogous construction for modules over a ring; `VTask.lift` is the abelian-group specialisation and is implemented by reducing to it with natural-number scalars.
- The **colimit comparison map** between two different direct limits built from the same underlying data, which is a different universal construction even though it also factors through `VTask.lift`.
