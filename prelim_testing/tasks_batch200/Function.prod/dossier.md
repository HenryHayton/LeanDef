## Object

`VTask.prod f g` is the pointwise pairing of two dependent functions: given an index `i`, it returns the pair `(f i, g i)`. Both component types may depend on the index, so `f` takes `i` to a value in `α i` and `g` takes `i` to a value in `β i`, and the result lives in the dependent product type `α i × β i`. This is the canonical way to combine two functions sharing the same domain into a single function landing in a product type.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prod : {ι : Sort u_3} -> {α : ι → Type u_1} -> {β : ι → Type u_2} -> (f : (i : ι) → α i) -> (g : (i : ι) → β i) -> (i : ι) -> α i × β i
<!-- PINNED-SIGNATURE:END -->


`VTask.prod : {ι : Sort u_3} -> {α : ι → Type u_1} -> {β : ι → Type u_2} -> (f : (i : ι) → α i) -> (g : (i : ι) → β i) -> (i : ι) -> α i × β i`

The index type `ι` is the shared domain of all functions involved. The type families `α` and `β` assign a type to each index, allowing the component types to vary with `i`. The argument `f` is the first component function, mapping each index `i` to a value in `α i`. The argument `g` is the second component function, mapping each index `i` to a value in `β i`. The final argument `i` is the particular index at which to evaluate the paired function.

## Conventions

No special junk-value or edge conventions are declared for this definition: it is a total function that behaves uniformly for every input, including when `ι` is an empty type (in which case no evaluation is possible, but the function is still well-formed) or a unit type.

## Worked examples

- Claim: `VTask.prod (fun n : Fin 3 => n.val) (fun n : Fin 3 => n.val + 1) ⟨0, by omega⟩ = (0, 1)`
  ```lean
  example : VTask.prod (fun n : Fin 3 => n.val) (fun n : Fin 3 => n.val + 1) ⟨0, by omega⟩ = (0, 1) := by decide
  ```

- Claim: `VTask.prod (fun b : Bool => b) (fun b : Bool => !b) true = (true, false)`
  ```lean
  example : VTask.prod (fun b : Bool => b) (fun b : Bool => !b) true = (true, false) := by decide
  ```

- Claim: For any functions `f : ι → α` and `g : ι → β` and index `i`, `(VTask.prod f g i).1 = f i` and `(VTask.prod f g i).2 = g i`. (The first and second projections recover the original function values pointwise.)

- Claim: Composing `VTask.prod f g` with a function `h : κ → ι` on the right equals `VTask.prod (f ∘ h) (g ∘ h)`. (Post-composition distributes into the pairing.)

## Boundaries

- When `ι` is an empty type (e.g., `Empty` or `Fin 0`), `VTask.prod f g` is a function from an empty type; it is vacuously defined and cannot be applied to any concrete index.
- When `ι` is a singleton (e.g., `Unit`), the result is a single pair, and the function is determined entirely by `f ()` and `g ()`.
- The non-dependent special case (where `α` and `β` are constant type families) recovers the ordinary pointwise pairing `fun i => (f i, g i)` on non-dependent function types.
- The definition is symmetric in the sense that swapping `f` and `g` gives the pointwise-swapped pairing; there is no canonical preference for which function is first.

## Not to be confused with

- `Prod.map`: takes a single pair and applies separate functions to each component, rather than building a pair from two functions with the same domain.
- `Pi.prod` / `fun i => (f i, g i)` written inline: these are definitionally equal but `VTask.prod` is the named, protected version intended for systematic use and rewriting.
- `MonoidHom.prod` / `LinearMap.prod` and similar algebraic `prod` combinators: these are structure-preserving variants for specific algebraic categories; their underlying function is `VTask.prod`, but they carry additional algebraic data.
