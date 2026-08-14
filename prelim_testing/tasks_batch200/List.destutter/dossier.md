## Object

`VTask.destutter R l` produces the **greedy destuttering** of the list `l` with respect to the binary relation `R`: it scans `l` from left to right, keeping each element that satisfies `R` with respect to the immediately preceding kept element, and discarding elements that do not. The result is a sublist of `l` in which every pair of adjacent elements satisfies `R`. In the canonical use case `R = (≠)`, this removes consecutive duplicate elements while preserving non-consecutive ones.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.destutter : {α : Type u_1} -> (R : α → α → Prop) -> [DecidableRel R] -> List α → List α
<!-- PINNED-SIGNATURE:END -->


`VTask.destutter : {α : Type u_1} -> (R : α → α → Prop) -> [DecidableRel R] -> List α → List α`

`α` is the element type of the list. `R` is the binary relation that adjacent elements of the result are required to satisfy — adjacent kept elements `a, b` will have `R a b`. The `DecidableRel R` instance is needed to decide at each step whether the current element should be retained. The final argument is the input list to be destuttered.

## Conventions

There are no special junk-value or out-of-domain conventions: the function is total over all lists and all decidable relations, with the empty list simply returning the empty list as a natural base case.

## Worked examples

- Claim: `VTask.destutter (· ≠ ·) [1, 2, 2, 1, 1] = [1, 2, 1]` — consecutive duplicate runs are collapsed to a single representative.
  ```lean
  example : VTask.destutter (· ≠ ·) [1, 2, 2, 1, 1] = [1, 2, 1] := by decide
  ```

- Claim: `VTask.destutter (· < ·) [1, 2, 5, 2, 3, 4, 9] = [1, 2, 5, 9]` — with the strict-less-than relation, each kept element must exceed the one before it; the greedy pass retains `1, 2, 5`, skips `2, 3, 4` (each ≤ 5), then keeps `9`.
  ```lean
  example : VTask.destutter (· < ·) [1, 2, 5, 2, 3, 4, 9] = [1, 2, 5, 9] := by decide
  ```

- Claim: `VTask.destutter (· ≠ ·) [3, 3, 3] = [3]` — an all-equal list collapses to one element.
  ```lean
  example : VTask.destutter (· ≠ ·) [3, 3, 3] = [3] := by decide
  ```

- Claim: `VTask.destutter (· ≠ ·) [1, 2, 3] = [1, 2, 3]` — a list with no consecutive duplicates is unchanged.
  ```lean
  example : VTask.destutter (· ≠ ·) [1, 2, 3] = [1, 2, 3] := by decide
  ```

- Claim: Applying `VTask.destutter R` twice gives the same result as applying it once (idempotence): `(l.destutter R).destutter R = l.destutter R`.

## Boundaries

- **Empty list**: `VTask.destutter R [] = []`. The empty list is a fixed point.
- **Singleton list**: `VTask.destutter R [a] = [a]`. A single element is always kept regardless of `R`.
- **Result is a sublist**: The output is always a sublist (in the order-preserving sublist sense) of the input; no elements are reordered or invented.
- **Result is never empty unless input is empty**: `VTask.destutter R l = [] ↔ l = []`.
- **Idempotence**: Applying destutter a second time does not change the result, because the output already satisfies `R` at every adjacent pair.
- **All-equal list**: For `R = (≠)`, a list of identical elements yields a singleton list containing just that element.
- **Greedy, not global**: The algorithm is greedy — it always keeps the first element of any run, which means a later element that could have enabled a longer chain may be lost.

## Not to be confused with

- **`List.dedup`**: Removes *all* duplicate elements (not just adjacent ones), producing a list of distinct elements; `destutter (≠)` only collapses consecutive duplicates and may leave non-adjacent repeated values.
- **`List.Nodup` / `List.Pairwise (≠)`**: These are *predicates* asserting a list has no adjacent (or no any) repetitions, while `VTask.destutter` is a *function* that constructs such a list.
- **`List.rdestutter` or reverse variants**: A right-to-left or last-element-biased version would keep different elements in runs; `VTask.destutter` is strictly left-to-right and first-element-greedy.