## VTask.mmap

### Object

`VTask.mmap` is the monadic map operation for length-indexed vectors (`List.Vector`). Given a function `f` that maps a value of type `α` to a monadic value `m β`, it applies `f` to every component of a vector of length `n`, sequences the resulting monadic effects left-to-right (head first, then tail), and returns a vector of length `n` — with the same length guaranteed in the type — wrapped in the monad `m`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mmap : {m : Type u → Type u_6} -> [Monad m] -> {α : Type u_7} -> {β : Type u} -> (f : α → m β) -> {n : ℕ} -> List.Vector α n → m (List.Vector β n)
<!-- PINNED-SIGNATURE:END -->


`{m : Type u → Type u_6} -> [Monad m] -> {α : Type u_7} -> {β : Type u} -> (f : α → m β) -> {n : ℕ} -> List.Vector α n → m (List.Vector β n)`

The first (implicit) argument `m` is the monad in which effects live; it is supplied a `Monad` instance automatically. The implicit type arguments `α` and `β` are the element types of the input and output vectors, respectively. The explicit argument `f` is the monadic function to apply to each element. The implicit argument `n` is the shared length of the input and output vectors, inferred from the vector passed in. The final explicit argument is the input vector of `n` elements of type `α`.

### Conventions

No special junk-value or edge conventions are declared beyond the structural ones: on the empty vector (length 0) the result is `pure nil`, so no effects are executed; on a non-empty vector the head is processed first, then the tail recursively, following the standard left-to-right sequencing discipline of `do`-notation.

### Worked examples

- Claim: Mapping the identity monadic lift over the empty vector yields `pure nil`.
  For the monad `Option`, `VTask.mmap some (nil : List.Vector ℕ 0) = pure nil`.

- Claim: Mapping `some` over the single-element vector `⟨[1], rfl⟩ : List.Vector ℕ 1` returns `some ⟨[1], rfl⟩`.

- Claim: Mapping a function that always returns `none` over any non-empty vector returns `none`.

- Claim: For a vector `v : List.Vector ℕ 2` with components `[3, 5]`, applying `VTask.mmap (fun x => some (x + 1))` returns `some` of the vector `[4, 6]`.

### Boundaries

- **Empty vector (n = 0):** Regardless of `f`, the result is `pure nil`. No invocations of `f` occur and no effects are performed.
- **Single-element vector (n = 1):** Exactly one call to `f` is made; the result is `f x >>= fun h => pure (h ::ᵥ nil)`.
- **Effect failure propagates:** If `m` is a monad like `Option` or `Except` and `f` returns a failure for any element, the entire computation short-circuits at that point and returns the failure value; elements after the first failure are not visited.
- **Length is preserved in the type:** The output vector's length `n` is identical to the input's length `n`, enforced by the return type `m (List.Vector β n)`. This is stronger than the `List.mapM` analogue, which only preserves length as a runtime property.

### Not to be confused with

- `List.mapM`: The monadic map for ordinary (length-unindexed) lists; it returns `m (List β)`, providing no static length guarantee.
- `List.Vector.map`: The pure (non-monadic) map on vectors; it applies `f : α → β` without any monadic sequencing.
- `List.Vector.mapM` (if it exists as an alias): Could refer to the same operation under a different name; check the exact namespace and type signature.
