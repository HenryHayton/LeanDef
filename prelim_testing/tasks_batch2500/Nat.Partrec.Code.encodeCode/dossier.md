## Object

`VTask.encodeCode` is an injective encoding of the inductive type `Nat.Partrec.Code` — the type representing partial recursive (Turing-complete) programs built from a fixed set of primitive operations — into the natural numbers. It assigns to each code a unique natural number, enabling codes to be treated as data in number-theoretic arguments about computability.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.encodeCode : Nat.Partrec.Code → ℕ
<!-- PINNED-SIGNATURE:END -->


`VTask.encodeCode : Nat.Partrec.Code → ℕ`

The single argument is a `Nat.Partrec.Code` value, i.e., one of the eight forms of partial recursive program: a constant-zero function, a successor function, a left-projection, a right-projection, a pairing of two codes, a composition of two codes, a primitive recursion from two codes, or an unbounded search (`rfind'`) applied to one code. The function returns a natural number uniquely identifying that code.

## Conventions

The four base constructors (`zero`, `succ`, `left`, `right`) are mapped to the small values 0, 1, 2, 3 respectively. Compound constructors (`pair`, `comp`, `prec`, `rfind'`) are mapped to values ≥ 4, encoded via the Cantor pairing function `Nat.pair` of the encodings of their sub-codes, with arithmetic tags distinguishing among the four compound forms. This encoding agrees exactly with the canonical `Encodable` instance for `Nat.Partrec.Code`, i.e., it equals `encode` from that instance.

## Worked examples

- Claim: `VTask.encodeCode Nat.Partrec.Code.zero = 0`
  ```lean
  example : VTask.encodeCode Nat.Partrec.Code.zero = 0 := by decide
  ```

- Claim: `VTask.encodeCode Nat.Partrec.Code.succ = 1`
  ```lean
  example : VTask.encodeCode Nat.Partrec.Code.succ = 1 := by decide
  ```

- Claim: `VTask.encodeCode Nat.Partrec.Code.left = 2`
  ```lean
  example : VTask.encodeCode Nat.Partrec.Code.left = 2 := by decide
  ```

- Claim: `VTask.encodeCode Nat.Partrec.Code.right = 3`
  ```lean
  example : VTask.encodeCode Nat.Partrec.Code.right = 3 := by decide
  ```

- Claim: Every compound code encodes to a value ≥ 4; for instance, `VTask.encodeCode (Nat.Partrec.Code.pair Nat.Partrec.Code.zero Nat.Partrec.Code.zero) ≥ 4`
  ```lean
  example : VTask.encodeCode (Nat.Partrec.Code.pair Nat.Partrec.Code.zero Nat.Partrec.Code.zero) ≥ 4 := by decide
  ```

- Claim: The encoding is injective — distinct codes receive distinct natural numbers.

- Claim: The encoding is surjective onto ℕ (i.e., every natural number arises as the encoding of some code), making it a bijection.

## Boundaries

- The function is total; every constructor of `Nat.Partrec.Code` is handled, and the result is always a well-defined natural number.
- The four base constructors cover exactly the values {0, 1, 2, 3}; the compound constructors cover all values ≥ 4, partitioned by arithmetic residues into four disjoint families.
- The encoding is bijective with a computable inverse (`ofNatCode`/`decodeCode`): composing `VTask.encodeCode` with `ofNatCode` is the identity on ℕ, and composing in the other order is the identity on `Nat.Partrec.Code`.
- Because `Nat.pair` is injective and the arithmetic tags are distinct, `VTask.encodeCode` is injective.

## Not to be confused with

- `Nat.pair`: the Cantor pairing function on pairs of natural numbers; `VTask.encodeCode` *uses* `Nat.pair` internally but operates on `Nat.Partrec.Code`, not on pairs of naturals.
- `Nat.Partrec.Code.ofNatCode` (or `decodeCode`): the inverse function that reconstructs a code from its numeric encoding; the two are inverses but are distinct objects.
- `Encodable.encode` for `Nat.Partrec.Code`: the canonical encode function from the `Encodable` typeclass instance — it coincides with `VTask.encodeCode` by a theorem, but is accessed through a different interface.