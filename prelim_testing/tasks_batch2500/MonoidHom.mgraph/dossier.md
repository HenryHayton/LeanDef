## VTask.mgraph

### Object

Given monoids $G$ and $H$ and a monoid homomorphism $f : G \to H$, the **graph of $f$** is the submonoid of the product monoid $G \times H$ consisting of all pairs $(g, h)$ such that $f(g) = h$. Equivalently, it is the set $\{(g, f(g)) \mid g \in G\}$, assembled as a submonoid of $G \times H$.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mgraph : {G : Type u_1} -> {H : Type u_2} -> [Monoid G] -> [Monoid H] -> (f : G →* H) -> Submonoid (G × H)
<!-- PINNED-SIGNATURE:END -->


`VTask.mgraph : {G : Type u_1} -> {H : Type u_2} -> [Monoid G] -> [Monoid H] -> (f : G →* H) -> Submonoid (G × H)`

The universe-polymorphic type parameters `G` and `H` are the source and target types, inferred implicitly. The two monoid instances supply the monoid structures on `G` and `H`. The explicit argument `f` is the monoid homomorphism whose graph is being constructed.

### Conventions

There are no junk-value conventions to declare: the definition is total and every monoid homomorphism has a well-defined graph as a submonoid of the product.

### Worked examples

- Claim: For the identity homomorphism `MonoidHom.id ℕ`, the pair `(3, 3)` belongs to its graph, while `(3, 5)` does not.

- Claim: For any monoid homomorphism `f : G →* H`, a pair `(g, h) : G × H` belongs to `VTask.mgraph f` if and only if `f g = h`.

- Claim: The graph of the trivial (constant-one) homomorphism from any monoid `G` to any monoid `H` contains exactly the pairs `(g, 1)` for every `g : G`.

- Claim: `VTask.mgraph f` is isomorphic (as a monoid) to `G` itself for any homomorphism `f`, via the projection to the first coordinate.

### Boundaries

- **Identity homomorphism**: The graph of the identity on $G$ is the diagonal submonoid $\{(g, g) \mid g \in G\}$ of $G \times G$.
- **Trivial homomorphism**: The graph of the trivial homomorphism $f : G \to H$ (sending every element to $1_H$) is $\{(g, 1_H) \mid g \in G\}$, which is isomorphic to $G$.
- **Injective $f$**: The graph is still all of $\{(g, f(g))\}$ but the induced projection to the second coordinate is injective, giving an isomorphism with $\mathrm{mrange}(f)$.
- **Surjective $f$**: Every element of $H$ appears as a second coordinate of some element of the graph.
- The graph always contains the identity element $(1_G, 1_H)$, since homomorphisms preserve the identity.
- The graph is always closed under multiplication: if $(g_1, f(g_1))$ and $(g_2, f(g_2))$ are in the graph, then so is $(g_1 g_2, f(g_1 g_2))$.

### Not to be confused with

- **`AddMonoidHom.graph`**: The analogous construction for additive monoid homomorphisms; structurally identical but lives in the additive world.
- **`MonoidHom.mrange`**: The image (range) of $f$ as a submonoid of $H$ alone, not the graph in $G \times H$; the graph maps surjectively onto the range via the second projection.
- **`Submonoid.prod`**: The product of two submonoids $S \leq G$ and $T \leq H$ as a submonoid of $G \times H$; this is generally larger than the graph and does not encode the functional relation $f(g) = h$.
