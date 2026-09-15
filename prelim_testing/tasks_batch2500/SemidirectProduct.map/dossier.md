## VTask.map

### Object

Given two semidirect products $N_1 \rtimes_{\varphi_1} G_1$ and $N_2 \rtimes_{\varphi_2} G_2$, and group homomorphisms $f_n : N_1 \to N_2$ and $f_g : G_1 \to G_2$ that are compatible with the respective actions (in the sense that conjugating by $f_g(g)$ in the second action commutes with $f_n$ and conjugating by $g$ in the first action), `VTask.map` produces the induced group homomorphism $N_1 \rtimes_{\varphi_1} G_1 \to N_2 \rtimes_{\varphi_2} G_2$ that sends a pair $(n, g)$ to $(f_n(n), f_g(g))$.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.map : {N₁ : Type u_4} -> {G₁ : Type u_5} -> {N₂ : Type u_6} -> {G₂ : Type u_7} -> [Group N₁] -> [Group G₁] -> [Group N₂] -> [Group G₂] -> {φ₁ : G₁ →* MulAut N₁} -> {φ₂ : G₂ →* MulAut N₂} -> (fn : N₁ →* N₂) -> (fg : G₁ →* G₂) -> (h : ∀ (g : G₁), fn.comp (MulEquiv.toMonoidHom (φ₁ g)) = (MulEquiv.toMonoidHom (φ₂ (fg g))).comp fn) -> N₁ ⋊[φ₁] G₁ →* N₂ ⋊[φ₂] G₂
<!-- PINNED-SIGNATURE:END -->


`VTask.map : {N₁ : Type u_4} -> {G₁ : Type u_5} -> {N₂ : Type u_6} -> {G₂ : Type u_7} -> [Group N₁] -> [Group G₁] -> [Group N₂] -> [Group G₂] -> {φ₁ : G₁ →* MulAut N₁} -> {φ₂ : G₂ →* MulAut N₂} -> (fn : N₁ →* N₂) -> (fg : G₁ →* G₂) -> (h : ∀ (g : G₁), fn.comp (MulEquiv.toMonoidHom (φ₁ g)) = (MulEquiv.toMonoidHom (φ₂ (fg g))).comp fn) -> N₁ ⋊[φ₁] G₁ →* N₂ ⋊[φ₂] G₂`

The implicit type arguments `N₁`, `G₁`, `N₂`, `G₂` are the underlying types of the normal subgroup and quotient group in each semidirect product, equipped with their respective `Group` instances. The implicit arguments `φ₁` and `φ₂` are the action homomorphisms that encode how $G_1$ acts on $N_1$ and $G_2$ acts on $N_2$ by multiplication automorphisms, defining the respective semidirect product structures. The argument `fn` is the group homomorphism from $N_1$ to $N_2$ (the map on the normal-subgroup component). The argument `fg` is the group homomorphism from $G_1$ to $G_2$ (the map on the complement component). The argument `h` is the compatibility condition: for every element $g \in G_1$, applying $f_n$ after the automorphism $\varphi_1(g)$ equals applying the automorphism $\varphi_2(f_g(g))$ after $f_n$; this is precisely the condition ensuring that the pair $(f_n, f_g)$ defines a genuine group homomorphism between the semidirect products.

### Conventions

There are no declared junk-value or edge conventions for this definition: the map is total and is well-defined whenever the compatibility condition `h` holds; no convention is needed for out-of-domain inputs.

### Worked examples

- Claim: For the trivial action (giving a direct product), `VTask.map` with identity maps on both components yields the identity homomorphism on the direct product.

- Claim: For any element `x : N₁ ⋊[φ₁] G₁`, the left (normal) component of `VTask.map fn fg h x` equals `fn x.left`.

- Claim: For any element `x : N₁ ⋊[φ₁] G₁`, the right (complement) component of `VTask.map fn fg h x` equals `fg x.right`.

- Claim: Precomposing `VTask.map fn fg h` with the canonical inclusion `inl : N₁ →* N₁ ⋊[φ₁] G₁` gives `inl.comp fn`; that is, `(VTask.map fn fg h).comp inl = inl.comp fn`.

- Claim: Precomposing `VTask.map fn fg h` with the canonical inclusion `inr : G₁ →* N₁ ⋊[φ₁] G₁` gives `inr.comp fg`; that is, `(VTask.map fn fg h).comp inr = inr.comp fg`.

### Boundaries

- When `fn` or `fg` is the trivial (constant-identity) homomorphism, `VTask.map` still produces a valid group homomorphism (the trivial one on the semidirect product), as long as `h` is satisfied.
- When both semidirect products are actually direct products (trivial action `φ₁ = 1` and `φ₂ = 1`), the compatibility condition `h` reduces to a trivially satisfied equation, and `VTask.map` simply pairs the two component maps.
- When `fn` and `fg` are both isomorphisms and `h` holds, the resulting map is a group isomorphism; however, `VTask.map` only constructs the homomorphism, not its inverse.
- The identity map on $N_1 \rtimes_{\varphi_1} G_1$ is recovered by taking `fn = id` (the identity on $N_1$) and `fg = id` (the identity on $G_1$) with the evident compatibility proof.

### Not to be confused with

- `SemidirectProduct.inl` / `SemidirectProduct.inr`: These are the canonical inclusion homomorphisms of $N$ and $G$ into $N \rtimes_\varphi G$, not a map between two different semidirect products.
- `SemidirectProduct.lift`: This constructs a homomorphism *out of* a semidirect product given maps on $N$ and $G$ into a *single* target group, rather than mapping between two semidirect products preserving the product structure.
- `MulEquiv` between semidirect products: An isomorphism of semidirect products is a stronger object; `VTask.map` only produces a `MonoidHom` (group homomorphism), not necessarily an equivalence.
