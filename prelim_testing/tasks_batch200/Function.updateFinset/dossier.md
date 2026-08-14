## 1. Object

`VTask.updateFinset x s y` is a dependent function on an index type `ι` that agrees with the "new values" `y` on every index that belongs to the finite set `s`, and agrees with the "base vector" `x` on every index outside `s`. Informally, it is the result of overwriting, in the dependent-function `x : (i : ι) → π i`, exactly the coordinates indexed by `s` with the values supplied by `y`.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.updateFinset : {ι : Type u_1} -> {π : ι → Sort u_2} -> [DecidableEq ι] -> (x : (i : ι) → π i) -> (s : Finset ι) -> (y : (i : ↥s) → π ↑i) -> (i : ι) -> π i
<!-- PINNED-SIGNATURE:END -->


`VTask.updateFinset : {ι : Type u_1} -> {π : ι → Sort u_2} -> [DecidableEq ι] -> (x : (i : ι) → π i) -> (s : Finset ι) -> (y : (i : ↥s) → π ↑i) -> (i : ι) -> π i`

- `ι` is the index type over which the dependent functions live.
- `π` is the type family assigning to each index its fiber (the type of value at that coordinate).
- The `DecidableEq ι` instance is needed so membership in `s` can be decided computationally.
- `x` is the base dependent function ("background vector") whose values are kept for indices outside `s`.
- `s` is the finite set of indices whose values are to be overwritten.
- `y` is the replacement dependent function defined on the subtype `↥s`, supplying a new value at each overwritten coordinate.
- The final argument `i : ι` is the index at which the resulting dependent function is evaluated.

## 3. Conventions

For an index `i` that belongs to `s`, `VTask.updateFinset x s y i` returns `y ⟨i, _⟩`, the replacement value at that coordinate. For an index `i` that does not belong to `s`, `VTask.updateFinset x s y i` returns `x i`, the original background value.

## 4. Worked examples

- Claim: For `ι = Fin 3`, `s = {0, 2}`, if `y` maps `0 ↦ 10` and `2 ↦ 30`, and `x` is the constant function mapping everything to `0`, then `VTask.updateFinset x s y 1 = 0` (index 1 is outside `s` so the background is used).
  ```lean
  example :
    let s : Finset (Fin 3) := {0, 2}
    let x : Fin 3 → ℕ := fun _ => 0
    let y : (i : ↥s) → ℕ := fun i =>
      if (i : Fin 3) = 0 then 10 else 30
    VTask.updateFinset x s y 1 = 0 := by decide
  ```

- Claim: For `ι = Fin 3`, `s = {0, 2}`, with `x` the constant `0` function and `y` mapping `0 ↦ 10` and `2 ↦ 30`, then `VTask.updateFinset x s y 0 = 10` (index 0 is inside `s` so the replacement is used).
  ```lean
  example :
    let s : Finset (Fin 3) := {0, 2}
    let x : Fin 3 → ℕ := fun _ => 0
    let y : (i : ↥s) → ℕ := fun i =>
      if (i : Fin 3) = 0 then 10 else 30
    VTask.updateFinset x s y 0 = 10 := by decide
  ```

- Claim: When `s` is the universal finset of a `Fintype`, `VTask.updateFinset x Finset.univ y i = y ⟨i, Finset.mem_univ i⟩` for every `i`, meaning the background `x` is entirely replaced.

- Claim: When `s` is empty, `VTask.updateFinset x ∅ y i = x i` for every `i`, since no index belongs to `∅`.
  ```lean
  example (ι : Type) [DecidableEq ι] (π : ι → Type) (x : ∀ i, π i)
      (y : ∀ i : (∅ : Finset ι), π i) (i : ι) :
      VTask.updateFinset x ∅ y i = x i := by simp [VTask.updateFinset]
  ```

## 5. Boundaries

- **Empty set (`s = ∅`):** No index satisfies membership, so the result equals `x` pointwise.
- **Universal set (`s = Finset.univ` with a `Fintype` instance):** Every index satisfies membership, so the result equals `y` (re-indexed to `ι`) pointwise; `x` is completely ignored.
- **Singleton set (`s = {j}`):** The result agrees with `Function.update x j (y ⟨j, _⟩)`, the usual single-coordinate update.
- **Index on the boundary (`i ∈ s`):** The replacement value `y ⟨i, _⟩` is returned, regardless of `x i`.
- **Index outside the set (`i ∉ s`):** The background value `x i` is returned, regardless of what `y` looks like elsewhere.
- **Overwriting `s` again with `s.restrict x`:** Produces `x` back, i.e., restoring the original is an identity.

## 6. Not to be confused with

- `Function.update` — updates exactly one coordinate at a single index `i`, not a whole finite set of coordinates at once.
- `Finset.restrict` — restricts a function `x : ∀ i, π i` to the subtype `↥s`, producing `∀ i : ↥s, π i`; this is a projection, not an update.
- `Pi.update` / `Set.update` — variant notions of coordinate update over a `Set` rather than a `Finset`, lacking the computational decidability structure used here.