## Object

Given a Dyck word `p`, a natural number `i`, and a proof that the first `i` symbols of `p` contain equal numbers of up-steps (`U`) and down-steps (`D`), `VTask.take p i hi` is the Dyck word whose underlying list is exactly the length-`i` prefix of `p`'s symbol list. In other words, it extracts a balanced prefix of a Dyck path and certifies that prefix as a valid Dyck word in its own right.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.take : (p : DyckWord) -> (i : ℕ) -> (hi : List.count DyckStep.U (List.take i ↑p) = List.count DyckStep.D (List.take i ↑p)) -> DyckWord
<!-- PINNED-SIGNATURE:END -->


VTask.take : (p : DyckWord) -> (i : ℕ) -> (hi : List.count DyckStep.U (List.take i ↑p) = List.count DyckStep.D (List.take i ↑p)) -> DyckWord

The first argument `p` is the Dyck word from which a prefix is to be extracted. The second argument `i` is the length of the prefix to take (as a natural number indexing into `p`'s underlying symbol list). The third argument `hi` is a proof obligation that the prefix of length `i` is balanced: the number of `U` steps in that prefix equals the number of `D` steps.

## Conventions

The function is total: for any `p`, `i`, and valid proof `hi`, a well-formed `DyckWord` is always returned. No special junk values are introduced; the only precondition is the explicit balancedness hypothesis `hi`.

## Worked examples

- Claim: Taking a prefix of length 0 from any Dyck word `p`, with the trivial balance proof, yields the empty Dyck word (the one with an empty underlying list).

- Claim: For the Dyck word `UUDD` (which has `toList = [U, U, D, D]`), taking a prefix of length 4 with the proof that `count U [U,U,D,D] = count D [U,U,D,D]` (both equal 2) recovers the original word.

- Claim: For the Dyck word `UDUD` (which has `toList = [U, D, U, D]`), taking a prefix of length 2 with the proof that `count U [U,D] = count D [U,D]` (both equal 1) yields the Dyck word `UD`.

- Claim: The underlying list (`toList`) of `VTask.take p i hi` equals `List.take i p.toList` for all valid inputs.

## Boundaries

- When `i = 0`, the prefix is empty. The balance condition `count U [] = count D []` holds trivially (both sides are 0), and the result is the empty Dyck word.
- When `i ≥ p.toList.length`, `List.take i p.toList` equals `p.toList` itself, so the result is `p` (provided `hi` is the balance proof for the full word, which holds since every Dyck word satisfies `count U = count D`).
- The hypothesis `hi` is strictly required: not every prefix of a Dyck word is itself a Dyck word, since intermediate prefixes may have more `U`s than `D`s. The function is only callable at lengths `i` where the prefix happens to be balanced.
- The `count_D_le_count_U` condition for the new Dyck word (every intermediate prefix has no more `D`s than `U`s) is automatically inherited from the corresponding property of the original word `p`, ensuring validity at all sub-prefixes.
- The `firstReturn` of a non-empty Dyck word `p` is the smallest positive index where the prefix is balanced; `count_take_firstReturn_add_one` confirms this is a valid `i` to use.

## Not to be confused with

- `DyckWord.firstReturn`: a natural number (the index of the first return to balance), not a Dyck word; `VTask.take` uses that index as its `i` argument.
- `List.take`: operates on arbitrary lists without any Dyck-word structure or balance constraint; `VTask.take` wraps the prefix in the `DyckWord` type.
- `DyckWord.append` (concatenation of two Dyck words): combines two whole Dyck words rather than splitting one.
