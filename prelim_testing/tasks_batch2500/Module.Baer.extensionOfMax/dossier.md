## Object

`VTask.extensionOfMax` is a **maximal extension** of a linear map `f : M →ₗ[R] Q` along an injective linear map `i : M →ₗ[R] N`. More precisely, it is an element of the type `ExtensionOf i f` — that is, a linear map `g : N' →ₗ[R] Q` defined on some submodule `N' ≤ N` containing the image of `i`, such that `g ∘ i = f` — and this element is **maximal** among all such extensions, in the sense that no strictly larger extension exists. Its existence is guaranteed by Zorn's lemma applied to the poset of all extensions of `f` along `i`, ordered by extension of domain.

This construction is a key step in proving the Baer criterion: a module `Q` is injective if and only if every such maximal extension is defined on all of `N`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.extensionOfMax : {R : Type u} -> [Ring R] -> {Q : Type v} -> [AddCommGroup Q] -> [Module R Q] -> {M : Type u_1} -> {N : Type u_2} -> [AddCommGroup M] -> [AddCommGroup N] -> [Module R M] -> [Module R N] -> (i : M →ₗ[R] N) -> (f : M →ₗ[R] Q) -> [Fact (Function.Injective ⇑i)] -> Module.Baer.ExtensionOf i f
<!-- PINNED-SIGNATURE:END -->


VTask.extensionOfMax : {R : Type u} -> [Ring R] -> {Q : Type v} -> [AddCommGroup Q] -> [Module R Q] -> {M : Type u_1} -> {N : Type u_2} -> [AddCommGroup M] -> [AddCommGroup N] -> [Module R M] -> [Module R N] -> (i : M →ₗ[R] N) -> (f : M →ₗ[R] Q) -> [Fact (Function.Injective ⇑i)] -> Module.Baer.ExtensionOf i f

`R` is the base ring; `Q` is the target module (a candidate injective module); `M` and `N` are the source and ambient modules. The argument `i` is the injective linear map embedding `M` into `N`. The argument `f` is the linear map from `M` to `Q` that one wishes to extend. The `Fact (Function.Injective ⇑i)` instance supplies the injectivity of `i` as a typeclass assumption. All additive group and module structures are provided as instances.

## Conventions

The construction is entirely non-constructive: the actual linear map returned is chosen by `Classical.choice` (wrapped inside Zorn's lemma), so no algorithm determines which maximal extension is returned. In particular, if multiple maximal extensions exist (which cannot happen when `Q` is injective, but can in degenerate settings), the choice among them is unspecified.

## Worked examples

- Claim: For any ring `R`, injective linear map `i : M →ₗ[R] N`, and linear map `f : M →ₗ[R] Q`, `VTask.extensionOfMax i f` is a term of type `Module.Baer.ExtensionOf i f`, hence in particular its domain is a submodule of `N` that contains the image of `i` and its underlying map restricts to `f` on the image of `i`.

- Claim: The element `VTask.extensionOfMax i f` is maximal in the poset `ExtensionOf i f` ordered by domain inclusion, meaning there is no element of `ExtensionOf i f` that strictly extends it.

- Claim: When `Q` is a Baer module (i.e., satisfies the Baer injectivity criterion), the domain of `VTask.extensionOfMax i f` equals all of `N`, so the extension is a full linear map `N →ₗ[R] Q`.

## Boundaries

- The construction requires `i` to be injective (supplied via `Fact (Function.Injective ⇑i)`); without this, the `ExtensionOf` type may not be well-behaved.
- The set of extensions is always nonempty (the trivial extension on the image of `i` itself is a default element), so Zorn's lemma is applicable and the result is well-defined.
- There is no computational content: the returned value cannot be evaluated to a concrete formula in general.
- If `M = 0` (the zero module), then `f` is the zero map and `VTask.extensionOfMax i f` is a maximal extension of the zero map, which in the Baer setting can always be taken to be all of `N`.

## Not to be confused with

- `Module.Baer.ExtensionOf i f` — this is the **type** of all extensions of `f` along `i`; `VTask.extensionOfMax` is a specific **term** (the maximal one) of that type.
- `Module.Baer` (the predicate) — this asserts that every linear map from a submodule can be extended to the whole module; `VTask.extensionOfMax` is a construction used in the proof of this characterization, not the predicate itself.
- A general Zorn's-lemma maximal element — `VTask.extensionOfMax` is specifically maximality in the poset of partial extensions of a fixed `f`, not maximality in an arbitrary poset.