## Object

`VTask.single` is the canonical "inclusion into a product" continuous linear map. Given an index `i` in a (possibly infinite) family of topological `R`-modules `φ`, it sends an element `x : φ i` to the function `j ↦ x` if `j = i`, and `0` otherwise. In other words, it bundles the pointwise-single-support function `Pi.single` into a genuine `R`-linear continuous map from the `i`-th component into the full product `∀ i, φ i`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.single : (R : Type u_1) -> [Semiring R] -> {ι : Type u_4} -> (φ : ι → Type u_5) -> [(i : ι) → TopologicalSpace (φ i)] -> [(i : ι) → AddCommMonoid (φ i)] -> [(i : ι) → Module R (φ i)] -> [DecidableEq ι] -> (i : ι) -> φ i →L[R] (i : ι) → φ i
<!-- PINNED-SIGNATURE:END -->


VTask.single : (R : Type u_1) -> [Semiring R] -> {ι : Type u_4} -> (φ : ι → Type u_5) -> [(i : ι) → TopologicalSpace (φ i)] -> [(i : ι) → AddCommMonoid (φ i)] -> [(i : ι) → Module R (φ i)] -> [DecidableEq ι] -> (i : ι) -> φ i →L[R] (i : ι) → φ i

`R` is the scalar semiring. `φ` is the family of types, one for each index in `ι`, each equipped with a topology, an additive commutative monoid structure, and an `R`-module structure. The `DecidableEq ι` instance is needed to decide whether two indices are equal when forming the single-support function. `i` is the chosen index: the map produced goes from the single component `φ i` into the full product `∀ i, φ i`.

## Conventions

When two indices coincide (i.e., the evaluation index equals the insertion index), the output is exactly the inserted element; when they differ, the output is `0`. This is the standard `Pi.single` convention and holds everywhere, including at the boundary where the index type is a singleton.

## Worked examples

- Claim: Evaluating `VTask.single R φ i x` at index `i` returns `x`.
  ```lean
  example (R : Type*) [Semiring R] {ι : Type*} [DecidableEq ι]
      (φ : ι → Type*) [(i : ι) → TopologicalSpace (φ i)]
      [(i : ι) → AddCommMonoid (φ i)] [(i : ι) → Module R (φ i)]
      (i : ι) (x : φ i) :
      VTask.single R φ i x i = x := by
    simp [VTask.single, Pi.single_eq_same]
  ```

- Claim: Evaluating `VTask.single R φ i x` at an index `j ≠ i` returns `0`.
  ```lean
  example (R : Type*) [Semiring R] {ι : Type*} [DecidableEq ι]
      (φ : ι → Type*) [(i : ι) → TopologicalSpace (φ i)]
      [(i : ι) → AddCommMonoid (φ i)] [(i : ι) → Module R (φ i)]
      (i j : ι) (h : j ≠ i) (x : φ i) :
      VTask.single R φ i x j = 0 := by
    simp [VTask.single, Pi.single_eq_of_ne h]
  ```

- Claim: `VTask.single R φ i` is a continuous linear map from `φ i` to `∀ i, φ i`, so composing with the `i`-th projection recovers the identity map.

- Claim: The range of `VTask.single R φ i` is contained in the set of functions supported only at `i`.

## Boundaries

- When `ι` is a singleton type (e.g., `Unit`), the map is an isomorphism: every element of the product is supported exactly at the unique index, so `single` is essentially the identity (up to isomorphism).
- When `ι` is empty, the map cannot be instantiated (there is no `i : ι`), so no boundary behaviour arises.
- The map sends `0 : φ i` to the zero function `∀ i, φ i`, consistent with linearity.
- The `DecidableEq ι` instance is required for the definition to compile; without it, the `if i = j then ... else 0` branch cannot be evaluated.

## Not to be confused with

- `LinearMap.single` (or `Pi.LinearMap.single`): the unbundled or purely algebraic single-support linear map, which does not carry continuity.
- `ContinuousLinearMap.proj`: the *projection* from the product onto a single component, which is dual to `VTask.single`.
- `Pi.single` (the bare function): the underlying function `φ i → ∀ i, φ i` without any linear or topological structure bundled.