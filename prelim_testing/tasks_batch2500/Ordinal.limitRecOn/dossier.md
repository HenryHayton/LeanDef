## VTask.limitRecOn

### Object

Limit induction (equivalently, transfinite recursion) on ordinals: a principle that allows one to define a value of type `motive o` for every ordinal `o` by specifying three cases — what the value is at zero, how to extend it from any ordinal `o` to its successor `o + 1`, and how to combine values at all smaller ordinals into a value at a limit ordinal. In proof terms it says: if a property holds at 0, is preserved by passing to successors, and holds at every limit ordinal whenever it holds at all smaller ordinals, then it holds at every ordinal.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.limitRecOn : {motive : Ordinal.{u_5} → Sort u_4} -> (o : Ordinal.{u_5}) -> (zero : motive 0) -> (add_one : (o : Ordinal.{u_5}) → motive o → motive (o + 1)) -> (limit : (o : Ordinal.{u_5}) → Order.IsSuccLimit o → ((o' : Ordinal.{u_5}) → o' < o → motive o') → motive o) -> motive o
<!-- PINNED-SIGNATURE:END -->


`{motive : Ordinal → Sort u_4}` is the property or type family being proved or defined, indexed by ordinals. `(o : Ordinal)` is the specific ordinal at which the result is computed. `(zero : motive 0)` is the base case: the value or proof at the ordinal 0. `(add_one : (o : Ordinal) → motive o → motive (o + 1))` is the successor step: given a value at any ordinal `o`, it produces a value at `o + 1`. `(limit : (o : Ordinal) → Order.IsSuccLimit o → ((o' : Ordinal) → o' < o → motive o') → motive o)` is the limit step: at any limit ordinal `o` (one that is not 0 and not a successor), given values at all strictly smaller ordinals, it produces a value at `o`.

### Conventions

Limit ordinals are those satisfying `Order.IsSuccLimit`, which means they are neither 0 nor a successor ordinal; note that 0 itself is treated as a separate base case and is NOT considered a limit ordinal in this scheme, even though it is not a successor. The recursion computes definitionally: at `o = 0` it returns `zero`; at `o = succ a` (equivalently `o = a + 1`) it returns `add_one a (VTask.limitRecOn a zero add_one limit)`; at a genuine limit ordinal `o` it returns `limit o h (fun o' _ => VTask.limitRecOn o' zero add_one limit)`.

### Worked examples

- Claim: VTask.limitRecOn 0 zero add_one limit = zero (the zero case reduces to the base case).
  This is the content of `limitRecOn_zero`: the function applied to ordinal 0 returns the `zero` argument unchanged.

- Claim: VTask.limitRecOn (o + 1) zero add_one limit = add_one o (VTask.limitRecOn o zero add_one limit) (the successor case reduces by one step).
  This is the content of `limitRecOn_add_one`: the function at `o + 1` calls `add_one` with `o` and the recursively computed value at `o`.

- Claim: For any limit ordinal `o` with witness `h : Order.IsSuccLimit o`, VTask.limitRecOn o zero add_one limit = limit o h (fun o' _ => VTask.limitRecOn o' zero add_one limit).
  This is the content of `limitRecOn_limit`: the function at a limit ordinal assembles all smaller values via the `limit` argument.

- Claim: One can define ordinal exponentiation `a ^ b` for `a ≠ 0` via VTask.limitRecOn on `b`, using `1` as the zero case, multiplication by `a` as the successor step, and a supremum over smaller values as the limit step.

### Boundaries

The ordinal 0 is treated exclusively as the zero case; it does not trigger the limit branch, even though it is vacuously a lower bound for all ordinals. Every nonzero ordinal is either a successor (triggering `add_one`) or a genuine limit ordinal (triggering `limit`). The `limit` argument receives a proof `Order.IsSuccLimit o` which rules out both 0 and successor ordinals, so the three cases are mutually exclusive and exhaustive. There are no restrictions on the universe `u_4` of the motive's values, so both proof-valued (`Prop`) and data-valued (any `Type`) uses are supported.

### Not to be confused with

- `WellFoundedLT.fix` (well-founded recursion on any well-founded relation): the fully general principle of which `VTask.limitRecOn` is a special but often more convenient case, handling all ordinals uniformly rather than splitting into the three ordinal-specific cases.
- Ordinary natural number induction / `Nat.rec`: handles only 0 and successor, with no limit case; not applicable to ordinals beyond ω.
- `Ordinal.isSuccLimit` or `Order.IsSuccLimit`: the predicate used to characterize limit ordinals in the third branch; it is an input to the `limit` argument of `VTask.limitRecOn`, not the recursion principle itself.