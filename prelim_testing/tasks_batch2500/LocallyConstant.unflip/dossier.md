## Object

`VTask.unflip f` takes a family of locally constant functions `f : α → LocallyConstant X β` — one locally constant map from `X` to `β` for each element of `α` — and assembles them into a single locally constant function `X → (α → β)`, where a point `x : X` is sent to the function `a ↦ f a x`. In other words, it "transposes" or "uncurries" the indexing: instead of varying over `α` to pick a function of `x`, you vary over `x` to get a function of `α`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.unflip : {X : Type u_5} -> {α : Type u_6} -> {β : Type u_7} -> [Finite α] -> [TopologicalSpace X] -> (f : α → LocallyConstant X β) -> LocallyConstant X (α → β)
<!-- PINNED-SIGNATURE:END -->


`VTask.unflip : {X : Type u_5} -> {α : Type u_6} -> {β : Type u_7} -> [Finite α] -> [TopologicalSpace X] -> (f : α → LocallyConstant X β) -> LocallyConstant X (α → β)`

- `X` is the topological space serving as the common domain of all locally constant functions in the family.
- `α` is the finite index type that parametrises the family; its finiteness is essential so that the intersection of finitely many open sets used internally remains open.
- `β` is the codomain (value type) shared by every function in the family.
- The `[Finite α]` instance witnesses that `α` has only finitely many elements.
- The `[TopologicalSpace X]` instance provides the topology on `X` needed to state and verify local constancy.
- `f` is the family itself: for each `a : α`, `f a` is a locally constant function from `X` to `β`.

## Conventions

No junk-value or edge conventions have been declared: every input satisfying the stated type constraints produces a well-formed `LocallyConstant X (α → β)`, and no output is considered "garbage" for any admissible input.

## Worked examples

- Claim: When `α = Fin 2`, `X = Bool` (with the discrete topology), `f 0 = (fun _ => true)` and `f 1 = (fun _ => false)`, then `(VTask.unflip f).toFun tt 0 = true` and `(VTask.unflip f).toFun tt 1 = false`.

- Claim: When `α` is the empty type (e.g. `α = Fin 0`), the result of `VTask.unflip f` evaluated at any point `x : X` is the unique function `Fin 0 → β`, since there are no indices to satisfy.

- Claim: `VTask.unflip f` satisfies `(VTask.unflip f).toFun x a = (f a).toFun x` for every `x : X` and `a : α` — that is, evaluation of the assembled function at `(x, a)` agrees with evaluation of the `a`-th member of the family at `x`.

- Claim: If each `f a` is the constant function with value `b : β`, then `VTask.unflip f` is the constant function with value `(fun _ => b) : α → β`.

## Boundaries

- **Empty index type (`α` has no elements):** The construction still works. With `Finite (Fin 0)` or any empty `α`, the intersection over `α` of preimages is empty (vacuously `⊤`, i.e. the whole space), so the resulting `LocallyConstant X (α → β)` is perfectly valid and sends every point `x` to the unique function from the empty type.
- **Singleton `α`:** The result is essentially a rearranged version of the single function `f ⟨default, ...⟩`.
- **`X` empty:** If `X` is an empty type, the locally constant function's `toFun` is a function from the empty set, still well-typed and locally constant vacuously.
- **`β` a one-element type:** All functions in the family are constant, and `VTask.unflip f` is the constant locally constant function to the unique element of `α → β`.

## Not to be confused with

- `LocallyConstant.flip`: the inverse operation, which takes a `LocallyConstant X (α → β)` and produces a family `α → LocallyConstant X β`; `VTask.unflip` goes the other direction.
- `LocallyConstant.comap`: pulls back a locally constant function along a continuous map, which is a different transformation on the domain `X`, not on the value type.
- `Pi.LocallyConstant` constructions that require a topology on `α` or on `β`: `VTask.unflip` requires only finiteness of `α`, not any topological structure on `α` or `β`.