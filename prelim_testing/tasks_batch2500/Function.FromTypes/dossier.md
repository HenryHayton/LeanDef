## Object

`VTask.FromTypes` constructs the type of an `n`-ary curried function whose arguments have heterogeneous types given by a finite family, and whose return type is fixed. Concretely, given a family `p : Fin n → Type u` and a return type `τ : Type u`, `VTask.FromTypes p τ` is the type `p 0 → p 1 → … → p (n-1) → τ` — an `n`-fold iterated function space.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.FromTypes : {n : ℕ} -> (Fin n → Type u) → Type u → Type u
<!-- PINNED-SIGNATURE:END -->


`VTask.FromTypes : {n : ℕ} -> (Fin n → Type u) → Type u → Type u`

The implicit natural number `n` is the arity of the function type being described. The first explicit argument is the type family `p : Fin n → Type u`, which assigns a type to each argument position. The second explicit argument is the result type `τ : Type u`.

## Conventions

When `n = 0` the function space degenerates to the return type itself, so `VTask.FromTypes p τ = τ` regardless of `p`. There is no junk or undefined behaviour at any input; the definition is total for all natural numbers and all type families.

## Worked examples

- Claim: `VTask.FromTypes ![] Nat = Nat` (arity zero collapses to the return type).

- Claim: `VTask.FromTypes ![Bool] Nat = (Bool → Nat)` (arity one is a single-argument function type).

- Claim: `VTask.FromTypes ![Bool, Int] Nat = (Bool → Int → Nat)` (arity two is a curried two-argument function type).

- Claim: For the constant family `fun _ => α`, `VTask.FromTypes (fun _ : Fin 3 => α) τ = (α → α → α → τ)` (all argument types coincide when the family is constant).

## Boundaries

- **Arity 0:** `VTask.FromTypes p τ = τ` for any `p : Fin 0 → Type u`. The argument family is vacuous but the return type is exactly `τ`.
- **Arity 1:** `VTask.FromTypes p τ = (p 0 → τ)`, a plain single-argument function.
- **Successor step:** `VTask.FromTypes p τ = (p 0 → VTask.FromTypes (fun i => p i.succ) τ)`, so the type unfolds one argument at a time from the front.
- **Empty vector notation:** `VTask.FromTypes ![] τ = τ` is a special instance of the arity-0 case.
- **`vecCons` notation:** `VTask.FromTypes (vecCons α p) τ = (α → VTask.FromTypes p τ)`, prepending one argument type to the family.

## Not to be confused with

- `Function.uncurry` / `VTask.FromTypes.uncurry`: the *function* that converts a value of type `VTask.FromTypes p τ` into its uncurried form `((i : Fin n) → p i) → τ`; `VTask.FromTypes` itself is only the *type*.
- `Pi` / dependent function types `(i : Fin n) → p i`: this is the uncurried argument tuple type, not the curried function type that `VTask.FromTypes` describes.
- `Function.OfArity α τ n`: a special case of iterated function spaces where every argument has the *same* type `α`; `VTask.FromTypes` generalises this to heterogeneous argument types.