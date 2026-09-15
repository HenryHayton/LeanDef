## VTask.Reduced

### Object

Given a family of groups $G_i$ (indexed by $\iota$), a group $H$, and a family of group homomorphisms $\phi_i : H \to G_i$, a **word** in the free product $\coprod_i G_i$ is called **reduced** (with respect to $\phi$) if none of the letters appearing in the word lie in the image of the corresponding $\phi_i$. Concretely, if the word is a sequence of pairs $(i_k, g_k)$ where each $g_k \in G_{i_k}$, then the word is reduced precisely when no $g_k$ belongs to $\phi_{i_k}(H) \subseteq G_{i_k}$.

This notion captures the idea that the word has been "fully reduced" relative to the base group $H$ embedded in each $G_i$ via $\phi$: no letter can be "absorbed" into the $H$-part.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Reduced : {ι : Type u_1} -> {G : ι → Type u_2} -> {H : Type u_3} -> [(i : ι) → Group (G i)] -> [Group H] -> (φ : (i : ι) → H →* G i) -> (w : Monoid.CoprodI.Word G) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Reduced : {ι : Type u_1} -> {G : ι → Type u_2} -> {H : Type u_3} -> [(i : ι) → Group (G i)] -> [Group H] -> (φ : (i : ι) → H →* G i) -> (w : Monoid.CoprodI.Word G) -> Prop`

The implicit type `ι` is the index type for the family of groups. The implicit family `G` assigns a group to each index. The implicit type `H` is the "base group" being mapped into each $G_i$. The instance `(i : ι) → Group (G i)` supplies the group structure on each $G_i$, and `Group H` supplies the group structure on $H$. The explicit argument `φ` is the family of group homomorphisms, one for each index $i$, sending $H$ into $G_i$; these determine which elements count as "coming from the base group." The explicit argument `w` is the word in the free product $\coprod_i G_i$ whose reducedness is being tested.

### Conventions

No junk-value or edge-case conventions are declared for this definition: it is a universally quantified predicate that is vacuously true on the empty word (since the empty word has no letters, the condition holds for all its letters trivially), and this is the standard mathematical convention rather than an arbitrary junk value.

### Worked examples

- Claim: The empty word `Monoid.CoprodI.Word.empty` is reduced with respect to any family of homomorphisms `φ`, since it has no letters.

- Claim: If `φ i` is the trivial homomorphism (sending every element of `H` to the identity in `G i`) and `w` contains a letter `(i, g)` where `g` is the identity element of `G i`, then `w` is NOT reduced, because the identity lies in the image of any group homomorphism.

- Claim: If each `φ i` is injective and `w` is a word all of whose letters lie strictly outside the image of the respective `φ i`, then `VTask.Reduced φ w` holds.

- Claim: If `H` is the trivial group, then every word `w` is reduced with respect to any `φ`, because the image of each `φ i` is just `{1}`, and a word in normal form in `CoprodI` has no trivial letters.

### Boundaries

- **Empty word**: The empty word is always reduced, by vacuous truth — the universal quantifier ranges over an empty set of letters.
- **Trivial homomorphisms**: If each $\phi_i$ is the trivial map, its image is $\{1\}$, and since the word is already in normal form in `CoprodI.Word` (which excludes identity letters), every word is reduced.
- **Surjective homomorphisms**: If some $\phi_i$ is surjective, then no word containing a letter at index $i$ can be reduced, since every element of $G_i$ is in the image of $\phi_i$.
- **The condition is per-letter**: Reducedness is a global property of the word, but it is checked letter by letter; a single letter in the image of $\phi$ suffices to make the word non-reduced.

### Not to be confused with

- **`Monoid.CoprodI.Word` (normal form)**: Being a `Word` already requires no trivial (identity) letters and no two consecutive letters at the same index; `VTask.Reduced` is an additional constraint relative to the maps $\phi_i$.
- **Reduced words in free groups**: In a free group, a reduced word has no letter adjacent to its inverse; here, the notion of reduction is with respect to a family of external homomorphisms, not adjacency cancellation.
- **`Monoid.CoprodI.NormalWord`**: A normal word in an amalgamated product or HNN extension carries richer structure about coset representatives; `VTask.Reduced` is a simpler predicate solely about images of $\phi_i$.