## VTask.normalizer

### Object

Given a group $G$ and a subset $S \subseteq G$, the **normalizer** of $S$ in $G$ is the subgroup of all elements $g \in G$ with the property that conjugation by $g$ preserves $S$ set-wise — that is, $g S g^{-1} = S$. Equivalently, an element $g$ belongs to the normalizer if and only if for every $n \in G$, we have $n \in S \iff g n g^{-1} \in S$. When $S$ is itself a subgroup $H$, the normalizer is the largest subgroup of $G$ in which $H$ sits as a normal subgroup.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.normalizer : {G : Type u_1} -> [Group G] -> (S : Set G) -> Subgroup G
<!-- PINNED-SIGNATURE:END -->


`VTask.normalizer : {G : Type u_1} -> [Group G] -> (S : Set G) -> Subgroup G`

The implicit argument `G` is the ambient group. The instance argument supplies the group structure on `G`. The explicit argument `S` is any subset of `G` whose normalizer is to be formed; it need not be a subgroup.

### Conventions

The definition is completely general: `S` is allowed to be any subset of `G`, not merely a subgroup. When `S` is not a subgroup, the normalizer is still a well-defined subgroup, although the "largest subgroup in which $S$ is normal" characterization does not directly apply in the same way. No junk values arise because the construction is total over all subsets.

### Worked examples

- Claim: Every element of $G$ normalizes the whole group $G$ itself; i.e., `VTask.normalizer (Set.univ : Set G) = ⊤`.

- Claim: Every element of $G$ normalizes the trivial subgroup $\{1\}$; i.e., `VTask.normalizer ({1} : Set G) = ⊤`.

- Claim: If $H$ is a normal subgroup of $G$, then `VTask.normalizer (H : Set G) = ⊤` — the normalizer is all of $G$.

- Claim: A subgroup $H$ is itself always contained in its own normalizer: `H ≤ VTask.normalizer (H : Set G)`.

- Claim: For an abelian group $G$ and any subset $S$, every element of $G$ normalizes $S$, so `VTask.normalizer S = ⊤`.

### Boundaries

- **Empty set:** The empty set $\emptyset \subseteq G$ satisfies $g \emptyset g^{-1} = \emptyset$ for all $g$, so the normalizer of the empty set is all of $G$ (the top subgroup).
- **Singleton $\{1\}$:** Since $g \cdot 1 \cdot g^{-1} = 1$ for all $g$, the normalizer of the trivial singleton is the whole group.
- **Whole group:** $G$ is invariant under any conjugation, so the normalizer of the whole set is the whole group.
- **Normal subgroup:** If $H \unlhd G$, then every element of $G$ conjugates $H$ to itself, so `normalizer H = ⊤`. Conversely, `normalizer H = ⊤` implies $H$ is normal.
- **Self-normalization:** Every subgroup is contained in its own normalizer. In general, a subgroup $H$ is self-normalizing when $\mathrm{N}_G(H) = H$.

### Not to be confused with

- **Centralizer** (`Subgroup.centralizer S`): the subgroup of elements that commute point-wise with every element of $S$ (i.e., $g s = s g$ for all $s \in S$), which is in general a smaller subgroup than the normalizer.
- **Center** (`Subgroup.center G`): the subgroup of elements commuting with *all* elements of $G$; a special case of the centralizer, not the normalizer.
- **Normal closure** (`Subgroup.normalClosure S`): the smallest normal subgroup of $G$ containing $S$, which is a different construction going in the opposite direction.
