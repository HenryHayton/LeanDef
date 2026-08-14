## VTask.StrongLT

### Object

`VTask.StrongLT a b` is the proposition that a dependent-function `a` is *strongly less than* a dependent-function `b`, meaning that `a` is strictly less than `b` at every index simultaneously. Concretely, it holds if and only if `a i < b i` for every element `i` of the index type.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.StrongLT : {ι : Type u_1} -> {π : ι → Type u_4} -> [(i : ι) → LT (π i)] -> (a b : (i : ι) → π i) -> Prop
<!-- PINNED-SIGNATURE:END -->


The implicit type `ι` is the index type over which both functions are defined. The family `π` assigns to each index `i` an ordered type (the fiber over `i`); the instance argument supplies a strict-order `LT` on each fiber. The explicit arguments `a` and `b` are the two dependent functions being compared: `a` is the putative lower function and `b` is the putative upper function.

### Conventions

No junk-value or edge-value conventions are declared for this definition: it is a universally-quantified `Prop` that is well-formed for any index type, any fiber family with `LT` instances, and any pair of functions, including when `ι` is empty (in which case the proposition holds vacuously).

### Worked examples

- Claim: For functions `a b : Fin 3 → ℕ` defined by `a i = i` and `b i = i + 1`, `VTask.StrongLT a b` holds, since `i < i + 1` for every `i : Fin 3`.

- Claim: `VTask.StrongLT (fun _ : Empty => (0 : ℕ)) (fun _ => 0)` holds vacuously because there are no indices to check.

- Claim: If `VTask.StrongLT a b` and `VTask.StrongLT b c` hold for functions into a type with a transitive strict order, then `VTask.StrongLT a c` holds, since `a i < b i < c i` for all `i` implies `a i < c i` for all `i`.

- Claim: `VTask.StrongLT (0 : Fin 2 → ℝ) (fun _ => 1)` holds because `(0 : ℝ) < 1`.

### Boundaries

- When the index type `ι` is empty (e.g., `Empty` or `Fin 0`), `VTask.StrongLT a b` is vacuously true for any `a` and `b`, regardless of the fiber orders.
- When `ι` is a singleton, `VTask.StrongLT a b` reduces to a single strict inequality `a default < b default`.
- The relation is irreflexive at every index (since `<` is irreflexive), so `VTask.StrongLT a a` is always false whenever `ι` is nonempty.
- The relation is strictly stronger than the pointwise `≤` relation: `VTask.StrongLT a b` implies `∀ i, a i ≤ b i`, but not conversely.
- There is no requirement that the index type be finite; the universal quantifier ranges over all of `ι`.

### Not to be confused with

- **Pointwise `≤` (Pi.instLE)**: the standard `a ≤ b` on pi-types requires `a i ≤ b i` for all `i`, using weak inequality rather than strict inequality at each fiber.
- **Lexicographic strict order on pi-types (`Pi.Lex`)**: compares functions lexicographically using a chosen well-order on the index type, not simultaneously at every index.
- **`Monovary f g`**: asserts a covariance condition between two functions on a *common* domain, not a pointwise strict ordering between two functions with the same type signature.
