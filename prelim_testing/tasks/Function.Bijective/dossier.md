## 1. Object

A function `f : α → β` between two types (or sorts) is **bijective** if it is simultaneously injective (no two distinct inputs are mapped to the same output) and surjective (every element of the codomain is hit by at least one input). Bijectivity captures the idea that `f` establishes a perfect one-to-one correspondence between `α` and `β`.

## 2. Signature

```
VTask.Bijective : {α : Sort u₁} -> {β : Sort u₂} -> (f : α → β) -> Prop
```

- `α : Sort u₁` — the domain type (implicit); may be a type or a proposition-universe sort.
- `β : Sort u₂` — the codomain type (implicit); similarly universe-polymorphic.
- `f : α → β` — the function whose bijectivity is being asserted.
- Returns a `Prop` stating that `f` is both injective and surjective.

## 3. Conventions

No special junk-value or edge-case conventions are declared for this predicate: it is a straightforward logical conjunction of injectivity and surjectivity, fully meaningful for every function in every universe, with no boundary inputs that require special treatment.

## 4. Worked Examples

- Claim: The identity function `id : α → α` is bijective for any type `α`.

- Claim: The function `f : Fin 2 → Fin 2` swapping `0` and `1` (i.e., `fun i => if i = 0 then 1 else 0`) is bijective.

- Claim: If `f : α → β` and `g : β → γ` are both bijective, then their composition `g ∘ f : α → γ` is also bijective.

- Claim: A bijective function `f : α → β` has a two-sided inverse; that is, there exists `g : β → α` such that `g ∘ f = id` and `f ∘ g = id`.

## 5. Boundaries

- **Empty domain:** If `α` is an empty type, the only function `f : α → β` is vacuously injective. It is bijective precisely when `β` is also empty (so surjectivity holds vacuously). If `β` is non-empty, the function is not surjective and hence not bijective.
- **Empty codomain:** If `β` is empty and `α` is non-empty, no function `f : α → β` can exist at all; the predicate is vacuously inapplicable. If both are empty, the unique function is bijective.
- **Singleton types:** Any function between two singleton types is bijective.
- **Universe generality:** The predicate is fully universe-polymorphic and applies to functions between propositions (`Prop`) as well as types.

## 6. Not to be confused with

- **`VTask.Injective`** — asserts only that `f` maps distinct inputs to distinct outputs; bijectivity additionally requires surjectivity.
- **`VTask.Surjective`** — asserts only that every element of the codomain is in the image of `f`; bijectivity additionally requires injectivity.
- **`Equiv α β`** — a bundled equivalence that packages a bijection together with its inverse and the proofs that they are mutual inverses; `VTask.Bijective f` is an unbundled `Prop` about a given function `f`, not a structure carrying the inverse.