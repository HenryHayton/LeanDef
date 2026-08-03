## VTask.map

### Object

Given a matroid `M` on a type `α` and a function `f : α → β` that is injective on the ground set of `M`, `VTask.map M f hf` is the matroid on `β` whose ground set is the image `f(M.E)` and whose independent sets are exactly the images under `f` of the independent sets of `M`. Informally, it is the *image* or *push-forward* of `M` along `f`; because `f` is injective on `M.E`, the matroid structure is transferred faithfully. If `β` is a nonempty type, a matroid `N` on `β` equals such a map if and only if `N` is isomorphic to `M`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.map : {α : Type u_1} -> {β : Type u_2} -> (M : Matroid α) -> (f : α → β) -> (hf : Set.InjOn f M.E) -> Matroid β
<!-- PINNED-SIGNATURE:END -->


`VTask.map : {α : Type u_1} -> {β : Type u_2} -> (M : Matroid α) -> (f : α → β) -> (hf : Set.InjOn f M.E) -> Matroid β`

The first argument `M` is the source matroid whose structure is to be transported. The second argument `f` is the function used to relabel elements from `α` to `β`. The third argument `hf` is the proof that `f` is injective when restricted to the ground set `M.E`; this injectivity is what makes the image matroid well-defined and isomorphic to `M`.

### Conventions

There are no junk-value or edge conventions declared for this definition: the construction is well-defined for every matroid `M`, every function `f`, and every proof `hf` that `f` is injective on `M.E`; no special output is stipulated for degenerate inputs.

### Worked examples

- Claim: The ground set of `VTask.map M f hf` is `f '' M.E` for any matroid `M`, function `f`, and injectivity proof `hf`.

- Claim: If `I` is an independent set of `M` and `I ⊆ M.E`, then `f '' I` is independent in `VTask.map M f hf`. (Formally: `M.Indep I → (VTask.map M f hf).Indep (f '' I)`.)

- Claim: If `B` is a base of `M`, then `f '' B` is a base of `VTask.map M f hf`. (Formally: `M.IsBase B → (VTask.map M f hf).IsBase (f '' B)`.)

- Claim: For any `X ⊆ M.E`, the extended rank of `f '' X` in `VTask.map M f hf` equals the extended rank of `X` in `M`. (Formally: `(VTask.map M f hf).eRk (f '' X) = M.eRk X`.)

- Claim: An element `f e` (with `e ∈ M.E`) is a loop in `VTask.map M f hf` if and only if `e` is a loop in `M`.

### Boundaries

- If `M` has an empty ground set (the empty matroid), then `VTask.map M f hf` also has empty ground set and is the empty matroid on `β`, regardless of `f`.
- The injectivity hypothesis `hf` only constrains `f` on `M.E`; the behaviour of `f` on elements outside `M.E` is irrelevant to the resulting matroid.
- If `f` is a bijection from `M.E` to some subset of `β`, the resulting matroid is isomorphic to `M`.
- Elements of `β` that are not in the image `f '' M.E` are outside the ground set of `VTask.map M f hf` entirely; they are neither independent nor dependent in the resulting matroid.

### Not to be confused with

- `Matroid.mapEmbedding`: the special case where `f` is given as an actual embedding `α ↪ β` (automatically injective everywhere, not only on `M.E`); `VTask.map` is strictly more general.
- `Matroid.comap` / `Matroid.comapOn`: these pull a matroid *back* along a function from `α` to `β` (going in the opposite direction), rather than pushing it forward.
- `Matroid.mapSetEmbedding`: a related construction that maps via an embedding of the subtype `M.E` rather than a plain function on the ambient type; `VTask.map` is the ambient-type version.