## Object

`VTask.withTopWithBot` takes a lattice homomorphism `f : α → β` and produces a **bounded** lattice homomorphism between the doubly-extended types `WithTop (WithBot α)` and `WithTop (WithBot β)`. The type `WithTop (WithBot α)` is the lattice obtained by freely adjoining both a greatest element `⊤` (via `WithTop`) and a least element `⊥` (via `WithBot`) to `α`; the resulting type is a bounded lattice regardless of whether `α` itself had top or bottom elements. The constructed map preserves all lattice operations and also strictly preserves the adjoin top `⊤` and the adjoin bottom `⊥`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.withTopWithBot : {α : Type u_1} -> {β : Type u_2} -> [Lattice α] -> [Lattice β] -> (f : LatticeHom α β) -> BoundedLatticeHom (WithTop (WithBot α)) (WithTop (WithBot β))
<!-- PINNED-SIGNATURE:END -->


`VTask.withTopWithBot : {α : Type u_1} -> {β : Type u_2} -> [Lattice α] -> [Lattice β] -> (f : LatticeHom α β) -> BoundedLatticeHom (WithTop (WithBot α)) (WithTop (WithBot β))`

The type parameters `α` and `β` are the source and target lattices, inferred implicitly. The two typeclass arguments supply the lattice structures on `α` and `β`. The explicit argument `f` is the lattice homomorphism being extended: it maps `α` to `β` preserving `⊓` and `⊔`, and the construction lifts it to the doubly-completed types while additionally preserving the freely adjoined `⊤` and `⊥`.

## Conventions

No junk-value or edge conventions are declared: the function is total and every case of the `WithTop (WithBot α)` type (the adjoined `⊤`, the adjoined `⊥`, and ordinary elements) is handled canonically by mapping `⊤ ↦ ⊤`, `⊥ ↦ ⊥`, and an ordinary element `a ↦ f a` (embedded in `WithTop (WithBot β)`).

## Worked examples

- Claim: Applying `VTask.withTopWithBot` to the identity lattice homomorphism on `α` yields the identity bounded lattice homomorphism on `WithTop (WithBot α)`.

- Claim: For lattices `α`, `β`, `γ` and lattice homomorphisms `g : α → β` and `f : β → γ`, composing their extensions equals the extension of their composition, i.e., `(f.comp g).withTopWithBot = f.withTopWithBot.comp g.withTopWithBot`.

- Claim: For any `a : WithTop (WithBot α)`, `(VTask.withTopWithBot f) a = a.map (WithBot.map f)` — meaning the action on the `WithTop` layer is given by mapping the `WithBot`-layer extension of `f` across the outer `WithTop`.

- Claim: The underlying function of `VTask.withTopWithBot f` equals `WithTop.map (WithBot.map f)` as a bare set-function.

## Boundaries

- At the adjoined top: `(VTask.withTopWithBot f) ⊤ = ⊤`. The map strictly preserves the freely adjoined greatest element.
- At the adjoined bottom: `(VTask.withTopWithBot f) ⊥ = ⊥`. The map strictly preserves the freely adjoined least element. Here `⊥` lives inside `WithBot α` (embedded in `WithTop (WithBot α)`).
- For an ordinary element `a : α` embedded into `WithTop (WithBot α)`, the map sends it to `f a` embedded in `WithTop (WithBot β)` — the original lattice homomorphism `f` acts on interior elements unchanged.
- The construction is functorial: identity maps to identity and composition is preserved, so it defines a functor on the category of lattices.

## Not to be confused with

- `LatticeHom.withBot`: extends a lattice homomorphism only to `WithBot α → WithBot β`, without also adjoining a top; the result is not a bounded lattice hom.
- `LatticeHom.withTop`: extends only to `WithTop α → WithTop β`, without also adjoining a bottom.
- `BoundedLatticeHom.withTopWithBot`: a version for bounded lattice homomorphisms (where `α` and `β` already carry `⊤` and `⊥`), as opposed to this construction which freely adjoins new top and bottom elements to bare lattices.
