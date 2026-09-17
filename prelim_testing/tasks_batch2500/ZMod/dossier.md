## VTask.ZMod

### Object

`VTask.ZMod n` is the type of integers modulo `n`, for a natural number `n`. When `n = 0` it is (by convention) the type of all integers, and when `n ≥ 1` it is the type of residue classes `{0, 1, …, n−1}`, i.e., a finite type with exactly `n` elements. This construction underlies modular arithmetic in Mathlib.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ZMod : ℕ → Type
<!-- PINNED-SIGNATURE:END -->


The single argument is the modulus: the natural number `n` that determines which residue system is being described. Passing `n = 0` yields the integers themselves (since modular arithmetic modulo 0 is identified with ℤ by convention), while passing any positive `n` yields the finite residue ring with `n` elements.

### Conventions

When the modulus is `0`, the type `VTask.ZMod 0` is definitionally equal to `ℤ` (the integers), rather than the trivial type or the empty type. This is a junk-value convention for the degenerate modulus: "modulo 0" does not describe a finite residue system, so the definition falls back to the full integers to keep the construction total and algebraically coherent.

### Worked examples

- Claim: `VTask.ZMod 0` is the type of integers.
  ```lean
  example : VTask.ZMod 0 = ℤ := rfl
  ```

- Claim: `VTask.ZMod 1` is the type `Fin 1`, which has exactly one element.
  ```lean
  example : VTask.ZMod 1 = Fin 1 := rfl
  ```

- Claim: `VTask.ZMod 5` is the type `Fin 5`, whose inhabitants represent the residue classes 0, 1, 2, 3, 4 modulo 5.
  ```lean
  example : VTask.ZMod 5 = Fin 5 := rfl
  ```

- Claim: `VTask.ZMod 7` has exactly 7 elements, representing the residue classes modulo 7.

### Boundaries

- **Modulus 0**: `VTask.ZMod 0 = ℤ`. This is the only case where the result is an infinite type.
- **Modulus 1**: `VTask.ZMod 1 = Fin 1`, a one-element type; every element is equal to every other.
- **Modulus n+1 (positive)**: `VTask.ZMod (n+1) = Fin (n+1)`, a finite type with exactly `n+1` elements.
- The function is total: every natural number produces a well-defined type.

### Not to be confused with

- **`Fin n`**: The type `Fin n` is always the type `{0, …, n−1}` regardless of context, whereas `VTask.ZMod 0` is ℤ, not `Fin 0` (which is the empty type).
- **`Int`** (ℤ): While `VTask.ZMod 0` equals ℤ by convention, `Int` refers to the integers as an independent type rather than as a modular ring.
- **The quotient `ℤ ⧸ nℤ`**: Conceptually identical to `VTask.ZMod n` for positive `n`, but constructed as an explicit quotient rather than via `Fin`; the two are isomorphic but not definitionally the same object.