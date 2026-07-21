# Harvest Batch 1 Review

Human-readable review of the first mechanical harvest (`miner/output/harvest_manifest.jsonl`), generated read-only from that file. See `docs/design/` for the design docs this harvest feeds, and the miner-stage-1 task summary for the pipeline that produced it.

## 1. Summary

### Corpus counts

- **Scanned** (pre-filter `def` hits, all 5 target corners): 782
- **Verified** (elaborates in the live environment, regardless of rank): 767
- **Included** (top 100 by rank): 100
- **Excluded**: 682
  - verified but outranked (below top 100): 667
  - does not elaborate: 15

### Supply tier distribution (100 included)

| Tier | Casework | Membership | Global |
|---|---|---|---|
| Rich | 24 | 0 | 35 |
| Thin | 0 | 66 | 49 |
| None | 76 | 34 | 16 |

### Distribution across source modules (100 included)

| Module | Count |
|---|---|
| Data/Finset | 26 |
| Data/Nat | 24 |
| Data/List | 17 |
| Logic/Equiv | 11 |
| Logic/Function | 7 |
| Data/Int | 5 |
| Logic/Relator.lean | 4 |
| Logic/Pairwise.lean | 2 |
| Logic/Basic.lean | 1 |
| Logic/ExistsUnique.lean | 1 |
| Logic/Godel | 1 |
| Logic/Relation.lean | 1 |

### Executability-mechanism split (100 included)

- **eval** (concrete return type, `#eval` on canonical inputs succeeded): 24
- **decide** (`Prop`-valued, `#eval` succeeded via Lean's own decide-fallback for `Prop`, i.e. genuinely decidable in practice): 1
- **none** (neither confirmed executable): 75

> **Note on this split.** Only 1 of 19 included `Prop`-returning definitions landed in `decide` rather than `none`. Looking into why while writing this report surfaced two verifier limitations worth flagging for whoever builds on this manifest next, not fixed here (read-only task):
>
> 1. `output_decidable_eq` checks `DecidableEq (<return type>)` literally. For a `Prop`-returning definition that becomes `DecidableEq Prop`, which is not a real Mathlib instance -- so *every* `Prop`-valued definition gets `output_decidable_eq = False` regardless of whether the specific proposition it produces is individually decidable. `Nat.Prime` (rank 5) is a clear example: `executable = True` (Lean's `#eval` falls back to `Decidable.decide` for `Prop` targets when an instance exists) but `casework_tier = none` anyway, purely because of this check. The tier undercounts genuinely decidable predicates.
> 2. Several definitions (`Pairwise`, `Function.Bijective`, `Set.Pairwise`, `ExistsUnique`, and others in the top 25 below -- **not only `Prop`-valued ones**: `List.orderedInsert` and `List.kerase` further down the table show the identical pattern with ordinary `List`-returning signatures) were recorded with **zero explicit arguments**, when their source clearly takes one or more (e.g. `Pairwise (r : α → α → Prop)`). The verifier's `#check`-output parser evidently doesn't capture a trailing explicit argument as a named binder group for some signature shapes -- plausibly ones where the argument is threaded through a `variable` (section-scoped) declaration rather than written directly in the `def` header, which Lean's pretty-printer may render as a bare arrow chain instead of a named `(x : T)` group. This starves the executability check of any arguments to try, producing errors like "don't know how to synthesize implicit argument" that get recorded as `executable = False` -- not a real negative result about the definition, and worth a proper fix (not attempted here) before this arity data is trusted at scale.

> **Data-quality flag: a scanner name-truncation bug affects 8 rows in this batch.** The pre-filter's identifier regex doesn't include Lean's unicode subscript digits (e.g. `₂`), so `image₂`, `Semiconj₂`, `map₂Left'`, `map₂Right'`, `map₂Left`, and `map₂Right` were all scanned with their trailing subscript silently dropped. Where the truncated name collides with a real, different Mathlib definition (`Finset.image₂` → `Finset.image`, `Function.Semiconj₂` → `Function.Semiconj`, four different `List.map₂...` variants → `List.map`), **every verification field for the mis-scanned row (elaborates, arity, executable, axioms, mention count) was actually measured against the wrong, colliding definition**, not the one whose source/docstring is shown. Affected rows: **16–17, 64–67, 75–76** (marked ⚠ in the table and detail cards below). This is a pre-filter bug, not a verification bug -- flagging per this task's instructions, not fixing.

## 2. Full ranked table (all 100 included)

Description: docstring (truncated to fit) where present; the one row lacking a docstring is marked with a leading — and a source-derived summary instead. ⚠ marks a row affected by the name-truncation bug above -- see its note in the top-25 detail cards or the flag above.

| Rank | Name | Module | Description | Arity | Signature | CW | Mem | Glob | Mentions | Deps | Score (components) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Finset.range | Data/Finset/Range.lean | `range n` is the set of natural numbers less than `n`. | 1 | `(n : ℕ) : Finset ℕ` | Rich | Thin | Rich | 852 | 0 | 63.00 (q=5, b=3, deg=27, dep=0) |
| 2 | finRotate | Logic/Equiv/Fin/Rotate.lean | Rotate `Fin n` one step to the right. | 1 | `(n : ℕ) : Equiv.Perm (Fin n)` | Rich | None | Rich | 31 | 6 | 46.94 (q=4, b=2, deg=18, dep=6) |
| 3 | Nat.log | Data/Nat/Log.lean | `log b n`, is the logarithm of natural number `n` in base `b`. It returns the largest `k : ℕ` such… | 2 | `(b n : ℕ) : ℕ` | Rich | None | Rich | 56 | 1 | 46.45 (q=4, b=2, deg=6, dep=1) |
| 4 | Pairwise | Logic/Pairwise.lean | A relation `r` holds pairwise if `r i j` for all `i ≠ j`. | 0 | `: Prop` | None | Thin | Rich | 1451 | 3 | 43.59 (q=3, b=2, deg=119, dep=3) |
| 5 | Nat.Prime | Data/Nat/Prime/Defs.lean | `Nat.Prime p` means that `p` is a prime number, that is, a natural number at least 2 whose only div… | 1 | `(p : ℕ) : Prop` | None | Thin | Rich | 450 | 1 | 39.89 (q=3, b=2, deg=21, dep=1) |
| 6 | Xor | Logic/Basic.lean | `Xor a b` is the exclusive-or of propositions. | 2 | `(a b : Prop) : Prop` | None | Thin | Rich | 56 | 0 | 38.59 (q=3, b=2, deg=8, dep=0) |
| 7 | Multiset.toFinset | Data/Finset/Dedup.lean | `toFinset s` removes duplicates from the multiset `s` to produce a finset. | 0 | `: Finset α` | None | Thin | Rich | 85 | 0 | 37.84 (q=3, b=2, deg=6, dep=0) |
| 8 | Function.Bijective | Logic/Function/Defs.lean | A function is called bijective if it is both injective and surjective. | 0 | `: Prop` | None | Thin | Rich | 656 | 3 | 37.14 (q=3, b=2, deg=13, dep=3) |
| 9 | Set.Pairwise | Logic/Pairwise.lean | The relation `r` holds pairwise on the set `s` if `r x y` for all *distinct* `x y ∈ s`. | 0 | `: Prop` | None | Thin | Rich | 180 | 4 | 36.24 (q=3, b=2, deg=11, dep=4) |
| 10 | ExistsUnique | Logic/ExistsUnique.lean | For `p : α → Prop`, `ExistsUnique p` means that there exists a unique `x : α` with `p x`. | 0 | `: Prop` | None | Thin | Rich | 38 | 3 | 36.14 (q=3, b=2, deg=9, dep=3) |
| 11 | DependsOn | Logic/Function/DependsOn.lean | A function `f` depends on `s` if, whenever `x` and `y` coincide over `s`, `f x = f y`. It should be… | 0 | `: Prop` | None | Thin | Rich | 24 | 5 | 35.61 (q=3, b=2, deg=10, dep=5) |
| 12 | Nat.bit | Data/Nat/BinaryRec.lean | `bit b` appends the digit `b` to the little end of the binary representation of its natural number… | 2 | `(b : Bool) (n : ℕ) : ℕ` | Rich | None | Thin | 53 | 1 | 35.44 (q=3, b=2, deg=4, dep=1) |
| 13 | Nat.clog | Data/Nat/Log.lean | `clog b n`, is the upper logarithm of natural number `n` in base `b`. It returns the smallest `k :… | 2 | `(b n : ℕ) : ℕ` | Rich | None | Thin | 34 | 1 | 35.44 (q=3, b=2, deg=4, dep=1) |
| 14 | List.toFinset | Data/Finset/Dedup.lean | `toFinset l` removes duplicates from the list `l` to produce a finset. | 0 | `: Finset α` | None | Thin | Rich | 32 | 3 | 35.07 (q=3, b=2, deg=6, dep=3) |
| 15 | IsDvdSequence | Data/Nat/DvdSequence.lean | A function `f : α → β` is a divisibility sequence if `a ∣ b` implies `f a ∣ f b`. | 0 | `: Prop` | None | Thin | Rich | 2 | 4 | 35.02 (q=3, b=2, deg=7, dep=4) |
| 16 | Finset.image | Data/Finset/Image.lean | `image f s` is the forward image of `s` under `f`. | 0 | `: Finset β` | None | Thin | Rich | 158 | 6 | 35.02 (q=3, b=2, deg=9, dep=6) |
| 17 | Finset.image ⚠ | Data/Finset/NAry.lean | The image of a binary function `f : α → β → γ` as a function `Finset α → Finset β → Finset γ`. Math… | 0 | `: Finset β` | None | Thin | Rich | 154 | 6 | 35.02 (q=3, b=2, deg=9, dep=6) |
| 18 | Int.sqrt | Data/Int/Sqrt.lean | `sqrt z` is the square root of an integer `z`. If `z` is positive, it returns the largest integer `… | 1 | `(z : ℤ) : ℤ` | Rich | None | Thin | 6 | 1 | 33.91 (q=3, b=2, deg=2, dep=1) |
| 19 | Nat.gcdA | Data/Int/GCD.lean | The extended GCD `a` value in the equation `gcd x y = x * a + y * b`. | 2 | `(x y : ℕ) : ℤ` | Rich | None | Thin | 7 | 1 | 32.69 (q=3, b=2, deg=1, dep=1) |
| 20 | Nat.fib | Data/Nat/Fib/Basic.lean | Implementation of the Fibonacci sequence satisfying `fib 0 = 0, fib 1 = 1, fib (n + 2) = fib n + fi… | 1 | `(n : ℕ) : ℕ` | Rich | None | Thin | 36 | 3 | 32.52 (q=3, b=2, deg=2, dep=3) |
| 21 | Denumerable.raise'Finset | Logic/Equiv/Finset.lean | Makes `raise' l n` into a finset. Elements are distinct thanks to `raise'_sorted`. | 2 | `(l : List ℕ) (n : ℕ) : Finset ℕ` | Rich | Thin | None | 0 | 0 | 32.00 (q=3, b=2, deg=0, dep=0) |
| 22 | Nat.digitsAux1 | Data/Nat/Digits/Defs.lean | (Impl.) An auxiliary definition for `digits`, to help get the desired definitional unfolding. | 1 | `(n : ℕ) : List ℕ` | Rich | Thin | None | 0 | 1 | 30.61 (q=3, b=2, deg=0, dep=1) |
| 23 | Nat.primeFactors | Data/Nat/PrimeFin.lean | The prime factors of a natural number as a finset. | 1 | `(n : ℕ) : Finset ℕ` | Rich | Thin | None | 36 | 1 | 30.61 (q=3, b=2, deg=0, dep=1) |
| 24 | List.Ico | Data/List/Intervals.lean | `Ico n m` is the list of natural numbers `n ≤ x < m`. (Ico stands for "interval, closed-open".) See… | 2 | `(n m : ℕ) : List ℕ` | Rich | Thin | None | 2 | 1 | 30.61 (q=3, b=2, deg=0, dep=1) |
| 25 | Cycle | Data/List/Cycle.lean | `Cycle α` is the quotient of `List α` by cyclic permutation. Duplicates are allowed. | 0 | `: Type u_1` | None | None | Rich | 1664 | 2 | 30.02 (q=2, b=1, deg=41, dep=2) |
| 26 | finSuccEquiv | Logic/Equiv/Fin/Basic.lean | Equivalence between `Fin (n + 1)` and `Option (Fin n)`. This is a version of `Fin.pred` that produc… | 1 | `(n : ℕ) : Fin (n + 1) ≃ Option (Fin n)` | None | None | Rich | 168 | 1 | 29.50 (q=2, b=1, deg=26, dep=1) |
| 27 | finSuccEquiv' | Logic/Equiv/Fin/Basic.lean | An equivalence that removes `i` and maps it to `none`. This is a version of `Fin.predAbove` that pr… | 1 | `{n : ℕ} (i : Fin (n + 1)) : Fin (n + 1) ≃ Option (Fin n)` | None | None | Rich | 2 | 0 | 29.50 (q=2, b=1, deg=16, dep=0) |
| 28 | Nat.digitsAppend | Data/Nat/Digits/Lemmas.lean | The list of digits of `n` in base `b` with some `0`'s appended so that its length is equal to `l` i… | 3 | `(b l n : ℕ) : List ℕ` | Rich | Thin | None | 0 | 3 | 29.23 (q=3, b=2, deg=0, dep=3) |
| 29 | List.Nat.antidiagonal | Data/List/NatAntidiagonal.lean | The antidiagonal of a natural number `n` is the list of pairs `(i, j)` such that `i + j = n`. | 1 | `(n : ℕ) : List (ℕ × ℕ)` | Rich | Thin | None | 12 | 3 | 29.23 (q=3, b=2, deg=0, dep=3) |
| 30 | Equiv.swap | Logic/Equiv/Basic.lean | `swap a b` is the permutation that swaps `a` and `b` and leaves other values as is. | 0 | `: Equiv.Perm α` | None | None | Rich | 128 | 0 | 28.92 (q=2, b=1, deg=13, dep=0) |
| 31 | Int.range | Data/Int/Range.lean | List enumerating `[m, n)`. This is the ℤ variant of `List.Ico`. | 2 | `(m n : ℤ) : List ℤ` | Rich | Thin | None | 3 | 4 | 28.78 (q=3, b=2, deg=0, dep=4) |
| 32 | Nat.find | Data/Nat/Find.lean | If `p` is a (decidable) predicate on `ℕ` and `hp : ∃ (n : ℕ), p n` is a proof that there exists som… | 1 | `{p : ℕ → Prop} [DecidablePred p] (H : ∃ n, p n) : ℕ` | None | None | Rich | 378 | 2 | 28.58 (q=2, b=1, deg=25, dep=2) |
| 33 | Equiv.symm | Logic/Equiv/Defs.lean | Inverse of an equivalence `e : α ≃ β`. | 0 | `: β ≃ α` | None | None | Rich | 1816 | 0 | 28.19 (q=2, b=1, deg=10, dep=0) |
| 34 | Nat.bitIndices | Data/Nat/BitIndices.lean | The function which maps each natural number `∑ i ∈ s, 2 ^ i` to the list of elements of `s` in incr… | 1 | `(n : ℕ) : List ℕ` | Rich | Thin | None | 2 | 6 | 28.11 (q=3, b=2, deg=0, dep=6) |
| 35 | Nat.unbeta | Logic/Godel/GodelBetaFunction.lean | Inverse of Gödel's Beta Function. This is similar to `Encodable.encodeList`, but it is easier to pr… | 1 | `(l : List ℕ) : ℕ` | Rich | Thin | None | 0 | 7 | 27.84 (q=3, b=2, deg=0, dep=7) |
| 36 | finSumFinEquiv | Logic/Equiv/Fin/Basic.lean | Equivalence between `Fin m ⊕ Fin n` and `Fin (m + n)` | 0 | `{m n : ℕ} : Fin m ⊕ Fin n ≃ Fin (m + n)` | None | None | Rich | 42 | 0 | 26.84 (q=2, b=1, deg=6, dep=0) |
| 37 | Finset.disjUnion | Data/Finset/Disjoint.lean | `disjUnion s t h` is the set such that `a ∈ disjUnion s t h` iff `a ∈ s` or `a ∈ t`. It is the same… | 0 | `: Finset α` | None | Thin | Thin | 22 | 0 | 26.83 (q=2, b=2, deg=4, dep=0) |
| 38 | Finset.powerset | Data/Finset/Powerset.lean | When `s` is a finset, `s.powerset` is the finset of all subsets of `s` (seen as finsets). | 0 | `: Finset (Finset α)` | None | Thin | Thin | 16 | 0 | 26.83 (q=2, b=2, deg=4, dep=0) |
| 39 | Finset.sym2 | Data/Finset/Sym.lean | `s.sym2` is the finset of all unordered pairs of elements from `s`. It is the image of `s ×ˢ s` und… | 0 | `: Finset (Sym2 α)` | None | Thin | Thin | 5 | 0 | 26.83 (q=2, b=2, deg=4, dep=0) |
| 40 | PartialEquiv.refl | Logic/Equiv/PartialEquiv.lean | The identity partial equiv | 0 | `: PartialEquiv α α` | None | None | Rich | 15 | 2 | 26.72 (q=2, b=1, deg=13, dep=2) |
| 41 | Finset.filter | Data/Finset/Filter.lean | `Finset.filter p s` is the set of elements of `s` that satisfy `p`. For example, one can use `s.fil… | 0 | `: Finset α` | None | Thin | Thin | 136 | 0 | 26.16 (q=2, b=2, deg=3, dep=0) |
| 42 | Finset.map | Data/Finset/Image.lean | When `f` is an embedding of `α` in `β` and `s` is a finset in `α`, then `s.map f` is the image fins… | 0 | `: Finset β` | None | Thin | Thin | 90 | 0 | 26.16 (q=2, b=2, deg=3, dep=0) |
| 43 | Function.Embedding.toEquivRange | Logic/Equiv/Fintype.lean | Computably turn an embedding `f : α ↪ β` into an equiv `α ≃ Set.range f`, if `α` is a `Fintype`. Ha… | 0 | `: α ≃ ↑(Set.range ⇑f)` | None | Thin | Thin | 3 | 0 | 26.16 (q=2, b=2, deg=3, dep=0) |
| 44 | Nat.choose | Data/Nat/Choose/Basic.lean | `choose n k` is the number of `k`-element subsets in an `n`-element set. Also known as binomial coe… | 0 | `: ℕ → ℕ → ℕ` | None | None | Rich | 188 | 3 | 25.42 (q=2, b=1, deg=10, dep=3) |
| 45 | List.toAList | Data/List/AList.lean | Given `l : List (Sigma β)`, create a term of type `AList β` by removing entries with duplicate keys. | 0 | `: AList β` | None | Thin | Thin | 0 | 0 | 25.30 (q=2, b=2, deg=2, dep=0) |
| 46 | notMemRangeEquiv | Data/Finset/Range.lean | Equivalence between the set of natural numbers which are `≥ k` and `ℕ`, given by `n → n - k`. | 1 | `(k : ℕ) : { n // n ∉ Finset.range k } ≃ ℕ` | None | Thin | Thin | 2 | 0 | 25.30 (q=2, b=2, deg=2, dep=0) |
| 47 | Nat.findGreatest | Data/Nat/Find.lean | `Nat.findGreatest P n` is the largest `i ≤ n` such that `P i` holds, or `0` if no such `i` exists | 1 | `(P : ℕ → Prop) [DecidablePred P] : ℕ → ℕ` | None | None | Rich | 21 | 4 | 25.24 (q=2, b=1, deg=11, dep=4) |
| 48 | Finset.card | Data/Finset/Card.lean | `s.card` is the number of elements of `s`, aka its cardinality. The notation `#s` can be accessed i… | 0 | `: ℕ` | None | None | Rich | 719 | 2 | 25.04 (q=2, b=1, deg=7, dep=2) |
| 49 | Function.update | Logic/Function/Basic.lean | Replacing the value of a function at a given point by a given value. | 0 | `: β a` | None | None | Rich | 447 | 6 | 25.03 (q=2, b=1, deg=13, dep=6) |
| 50 | hyperoperation | Data/Nat/Hyperoperation.lean | Implementation of the hyperoperation sequence where `hyperoperation n m k` is the `n`th hyperoperat… | 0 | `: ℕ → ℕ → ℕ → ℕ` | None | None | Rich | 0 | 4 | 24.97 (q=2, b=1, deg=10, dep=4) |
| 51 | Pi.map | Logic/Function/Defs.lean | Sends a dependent function `a : ∀ i, α i` to a dependent function `Pi.map f a : ∀ i, β i` by applyi… | 0 | `: ((i : ι) → α i) → (i : ι) → β i` | None | None | Rich | 151 | 3 | 24.82 (q=2, b=1, deg=8, dep=3) |
| 52 | Relation.Map | Logic/Relation.lean | The map of a relation `r` through a pair of functions pushes the relation to the codomains of the f… | 0 | `: γ → δ → Prop` | None | None | Rich | 25 | 7 | 24.76 (q=2, b=1, deg=13, dep=7) |
| 53 | Nat.Primes | Data/Nat/Prime/Defs.lean | The type of prime numbers | 0 | `: Type` | None | None | Rich | 96 | 2 | 24.18 (q=2, b=1, deg=5, dep=2) |
| 54 | Finset.erase | Data/Finset/Erase.lean | `erase s a` is the set `s - {a}`, that is, the elements of `s` which are not equal to `a`. | 0 | `: Finset α` | None | Thin | Thin | 55 | 0 | 24.08 (q=2, b=2, deg=1, dep=0) |
| 55 | Finset.filterMap | Data/Finset/Image.lean | — def filterMap (f : α → Option β) (s : Finset α) (f_inj : ∀ a a' b, b ∈ f a → b ∈ f a' → a = a') :… | 0 | `: Finset β` | None | Thin | Thin | 0 | 0 | 24.08 (q=2, b=2, deg=1, dep=0) |
| 56 | Finset.cons | Data/Finset/Insert.lean | `cons a s h` is the set `{a} ∪ s` containing `a` and the elements of `s`. It is the same as `insert… | 0 | `: Finset α` | None | Thin | Thin | 125 | 0 | 24.08 (q=2, b=2, deg=1, dep=0) |
| 57 | Finset.product | Data/Finset/Prod.lean | `product s t` is the set of pairs `(a, b)` such that `a ∈ s` and `b ∈ t`. | 0 | `: Finset (α × β)` | None | Thin | Thin | 9 | 0 | 24.08 (q=2, b=2, deg=1, dep=0) |
| 58 | Finset.disjiUnion | Data/Finset/Union.lean | `disjiUnion s f h` is the set such that `a ∈ disjiUnion s f` iff `a ∈ f i` for some `i ∈ s`. It is… | 0 | `: Finset β` | None | Thin | Thin | 5 | 0 | 24.08 (q=2, b=2, deg=1, dep=0) |
| 59 | Equiv.Set.sumCompl | Logic/Equiv/Set.lean | If `s : Set α` is a set with decidable membership, then `s ⊕ sᶜ` is equivalent to `α`. See also `Eq… | 0 | `: ↑s ⊕ ↑sᶜ ≃ α` | None | None | Rich | 12 | 4 | 23.62 (q=2, b=1, deg=6, dep=4) |
| 60 | Finset.sym | Data/Finset/Sym.lean | Lifts a finset to `Sym α n`. `s.sym n` is the finset of all unordered tuples of cardinality `n` wit… | 0 | `: Finset (Sym α n)` | None | Thin | Thin | 22 | 5 | 23.24 (q=2, b=2, deg=4, dep=5) |
| 61 | Nat.multinomial | Data/Nat/Choose/Multinomial.lean | The multinomial coefficient. Gives the number of strings consisting of symbols from `s`, where `c ∈… | 0 | `: ℕ` | None | None | Rich | 4 | 4 | 23.16 (q=2, b=1, deg=5, dep=4) |
| 62 | Multiset.multinomial | Data/Nat/Choose/Multinomial.lean | The `multinomial` coefficients on `Multiset ℕ`. | 1 | `(m : Multiset ℕ) : ℕ` | None | Thin | Thin | 2 | 2 | 23.10 (q=2, b=2, deg=2, dep=2) |
| 63 | Finset.Nonempty | Data/Finset/Empty.lean | The property `s.Nonempty` expresses the fact that the finset `s` is not empty. It should be used in… | 0 | `: Prop` | None | Thin | Thin | 81 | 2 | 23.10 (q=2, b=2, deg=2, dep=2) |
| 64 | List.map ⚠ | Data/List/Defs.lean | Left-biased version of `List.map₂`. `map₂Left' f as bs` applies `f` to each pair of elements `aᵢ ∈… | 0 | `: List β` | None | Thin | Thin | 362 | 4 | 22.94 (q=2, b=2, deg=3, dep=4) |
| 65 | List.map ⚠ | Data/List/Defs.lean | Right-biased version of `List.map₂`. `map₂Right' f as bs` applies `f` to each pair of elements `aᵢ… | 0 | `: List β` | None | Thin | Thin | 362 | 4 | 22.94 (q=2, b=2, deg=3, dep=4) |
| 66 | List.map ⚠ | Data/List/Defs.lean | Left-biased version of `List.map₂`. `map₂Left f as bs` applies `f` to each pair `aᵢ ∈ as` and `bᵢ ∈… | 0 | `: List β` | None | Thin | Thin | 362 | 4 | 22.94 (q=2, b=2, deg=3, dep=4) |
| 67 | List.map ⚠ | Data/List/Defs.lean | Right-biased version of `List.map₂`. `map₂Right f as bs` applies `f` to each pair `aᵢ ∈ as` and `bᵢ… | 0 | `: List β` | None | Thin | Thin | 362 | 4 | 22.94 (q=2, b=2, deg=3, dep=4) |
| 68 | List.rdrop | Data/List/DropRight.lean | Drop `n` elements from the tail end of a list. | 0 | `: List α` | None | Thin | Thin | 0 | 4 | 22.94 (q=2, b=2, deg=3, dep=4) |
| 69 | List.SortedLE | Data/List/Sort.lean | `l.SortedLE` means that the list is monotonic. | 0 | `: Prop` | None | Thin | Thin | 3 | 4 | 22.94 (q=2, b=2, deg=3, dep=4) |
| 70 | List.SortedLT | Data/List/Sort.lean | `l.SortedLT` means that the list is strictly monotonic. | 0 | `: Prop` | None | Thin | Thin | 5 | 4 | 22.94 (q=2, b=2, deg=3, dep=4) |
| 71 | finAddFlip | Logic/Equiv/Fin/Basic.lean | The equivalence between `Fin (m + n)` and `Fin (n + m)` which rotates by `n`. | 0 | `{m n : ℕ} : Fin (m + n) ≃ Fin (n + m)` | None | None | Rich | 4 | 5 | 22.79 (q=2, b=1, deg=5, dep=5) |
| 72 | Function.Commute | Logic/Function/Conjugate.lean | Two maps `f g : α → α` commute if `f (g x) = g (f x)` for all `x : α`. Given `h : Function.commute… | 0 | `: Prop` | None | Thin | Thin | 31 | 3 | 22.52 (q=2, b=2, deg=2, dep=3) |
| 73 | Relator.BiUnique | Logic/Relator.lean | A relation is "bi-unique" if it is both left unique and right unique. | 0 | `: Prop` | None | Thin | Thin | 2 | 3 | 22.52 (q=2, b=2, deg=2, dep=3) |
| 74 | Finset.subtype | Data/Finset/Image.lean | Given a finset `s` and a predicate `p`, `s.subtype p` is the finset of `Subtype p` whose elements b… | 0 | `: Finset (Subtype p)` | None | Thin | Thin | 11 | 4 | 22.08 (q=2, b=2, deg=2, dep=4) |
| 75 | Function.Semiconj | Logic/Function/Conjugate.lean | We say that `f : α → β` semiconjugates `ga : α → α` to `gb : β → β` if `f ∘ ga = gb ∘ f`. We use `∀… | 0 | `: Prop` | None | Thin | Thin | 37 | 4 | 22.08 (q=2, b=2, deg=2, dep=4) |
| 76 | Function.Semiconj ⚠ | Logic/Function/Conjugate.lean | A map `f` semiconjugates a binary operation `ga` to a binary operation `gb` if for all `x`, `y` we… | 0 | `: Prop` | None | Thin | Thin | 37 | 4 | 22.08 (q=2, b=2, deg=2, dep=4) |
| 77 | Relator.RightUnique | Logic/Relator.lean | A relation is "right unique" if every element on the left is paired with at most one element on the… | 0 | `: Prop` | None | Thin | Thin | 3 | 4 | 22.08 (q=2, b=2, deg=2, dep=4) |
| 78 | Finset.fold | Data/Finset/Fold.lean | `fold op b f s` folds the commutative associative operation `op` over the `f`-image of `s`, i.e. `f… | 0 | `: β` | None | None | Rich | 11 | 9 | 21.77 (q=2, b=1, deg=5, dep=9) |
| 79 | Set.Sized | Data/Finset/Slice.lean | `Sized r A` means that every Finset in `A` has size `r`. | 0 | `: Prop` | None | Thin | Thin | 12 | 5 | 21.71 (q=2, b=2, deg=2, dep=5) |
| 80 | Finset.mapEmbedding | Data/Finset/Image.lean | Associate to an embedding `f` from `α` to `β` the order embedding that maps a finset to its image u… | 0 | `: Finset α ↪o Finset β` | None | Thin | Thin | 1 | 3 | 21.31 (q=2, b=2, deg=1, dep=3) |
| 81 | Option.toFinset | Data/Finset/Option.lean | Construct an empty or singleton finset from an `Option` | 0 | `: Finset α` | None | Thin | Thin | 2 | 3 | 21.31 (q=2, b=2, deg=1, dep=3) |
| 82 | Relator.BiTotal | Logic/Relator.lean | A relation is "bi-total" if it is both right total and left total. | 0 | `: Prop` | None | Thin | Thin | 0 | 3 | 21.31 (q=2, b=2, deg=1, dep=3) |
| 83 | Nat.digits | Data/Nat/Digits/Defs.lean | `digits b n` gives the digits, in little-endian order, of a natural number `n` in a specified base… | 0 | `: ℕ → ℕ → List ℕ` | None | Thin | Thin | 14 | 7 | 21.14 (q=2, b=2, deg=2, dep=7) |
| 84 | Finset.biUnion | Data/Finset/Union.lean | `Finset.biUnion s t` is the union of `t a` over `a ∈ s`. (This was formerly `bind` due to the monad… | 0 | `: Finset β` | None | Thin | Thin | 31 | 7 | 21.14 (q=2, b=2, deg=2, dep=7) |
| 85 | Nat.dist | Data/Nat/Dist.lean | Distance (absolute value of difference) between natural numbers. | 2 | `(n m : ℕ) : ℕ` | Rich | None | None | 31 | 0 | 21.00 (q=2, b=1, deg=0, dep=0) |
| 86 | Nat.factorization | Data/Nat/Factorization/Defs.lean | `n.factorization` is the finitely supported function `ℕ →₀ ℕ` mapping each prime factor of `n` to i… | 1 | `(n : ℕ) : ℕ →₀ ℕ` | Rich | None | None | 36 | 0 | 21.00 (q=2, b=1, deg=0, dep=0) |
| 87 | Nat.pair | Data/Nat/Pairing.lean | Pairing function for the natural numbers. | 2 | `(a b : ℕ) : ℕ` | Rich | None | None | 82 | 0 | 21.00 (q=2, b=1, deg=0, dep=0) |
| 88 | Int.succ | Data/Int/Init.lean | Immediate successor of an integer: `succ n = n + 1` | 1 | `(a : ℤ) : ℤ` | Rich | None | None | 1 | 0 | 21.00 (q=2, b=1, deg=0, dep=0) |
| 89 | Int.pred | Data/Int/Init.lean | Immediate predecessor of an integer: `pred n = n - 1` | 1 | `(a : ℤ) : ℤ` | Rich | None | None | 0 | 0 | 21.00 (q=2, b=1, deg=0, dep=0) |
| 90 | List.Forall | Data/List/Defs.lean | `l.Forall p` is equivalent to `∀ a ∈ l, p a`, but unfolds directly to a conjunction, i.e. `List.For… | 0 | `: List α → Prop` | None | Thin | Thin | 23 | 4 | 20.86 (q=2, b=2, deg=1, dep=4) |
| 91 | Relator.LeftUnique | Logic/Relator.lean | A relation is "left unique" if every element on the right is paired with at most one element on the… | 0 | `: Prop` | None | Thin | Thin | 4 | 4 | 20.86 (q=2, b=2, deg=1, dep=4) |
| 92 | Nat.bits | Data/Nat/Bits.lean | `bits n` returns a list of Bools which correspond to the binary representation of n, where the head… | 0 | `: ℕ → List Bool` | None | Thin | Thin | 1 | 5 | 20.50 (q=2, b=2, deg=1, dep=5) |
| 93 | List.destutter' | Data/List/Defs.lean | Greedily create a sublist of `a :: l` such that, for every two adjacent elements `a, b`, `R a b` ho… | 0 | `: α → List α → List α` | None | Thin | Thin | 9 | 5 | 20.50 (q=2, b=2, deg=1, dep=5) |
| 94 | List.iterate | Data/List/Defs.lean | `iterate f a n` is `[a, f a, ..., f^[n - 1] a]`. | 0 | `: List α` | None | Thin | Thin | 4 | 5 | 20.50 (q=2, b=2, deg=1, dep=5) |
| 95 | List.destutter | Data/List/Defs.lean | Greedily create a sublist of `l` such that, for every two adjacent elements `a, b ∈ l`, `R a b` hol… | 0 | `: List α → List α` | None | Thin | Thin | 18 | 6 | 20.19 (q=2, b=2, deg=1, dep=6) |
| 96 | List.kerase | Data/List/Sigma.lean | Remove the first pair with the key `a`. | 0 | `: List (Sigma β) → List (Sigma β)` | None | Thin | Thin | 2 | 6 | 20.19 (q=2, b=2, deg=1, dep=6) |
| 97 | List.orderedInsert | Data/List/Sort.lean | `orderedInsert a l` inserts `a` into `l` at such that `orderedInsert a l` is sorted if `l` is. | 0 | `: List α → List α` | None | Thin | Thin | 1 | 6 | 20.19 (q=2, b=2, deg=1, dep=6) |
| 98 | Finset.sort | Data/Finset/Sort.lean | `sort s` constructs a sorted list from the unordered set `s`. (Uses merge sort algorithm.) | 0 | `: List α` | None | Thin | Thin | 10 | 7 | 19.92 (q=2, b=2, deg=1, dep=7) |
| 99 | Nat.centralBinom | Data/Nat/Choose/Central.lean | The central binomial coefficient, `Nat.choose (2 * n) n`. | 1 | `(n : ℕ) : ℕ` | Rich | None | None | 12 | 1 | 19.61 (q=2, b=1, deg=0, dep=1) |
| 100 | Nat.ascFactorialBinary | Data/Nat/Factorial/Basic.lean | `ascFactorial` implemented using binary splitting. While this still performs the same number of mul… | 2 | `(n k : ℕ) : ℕ` | Rich | None | None | 0 | 1 | 19.61 (q=2, b=1, deg=0, dep=1) |
## 3. Detail cards: top 25

### 1. Finset.range
*Data/Finset/Range.lean*

**Docstring:**
> `range n` is the set of natural numbers less than `n`.

**Source:**
```lean
def range (n : ℕ) : Finset ℕ :=
  ⟨_, nodup_range n⟩
```

**Raw supply numbers:** mention_count=852, theorem_mention_count=27, enumerable_arg_count=1, is_predicate_shaped=False, classifies_structure=True, executable=True, output_decidable_eq=True, dependency_raw (referenced_constants count)=0
**Axiom set:** Classical.choice, Quot.sound, propext
**Score:** 63.00 (quality=5, breadth=3, in_degree=27, dependency=0)
**Notes:** Foundational, self-contained (subtype-wraps `nodup_range n`) — not a wrapper. A strong, uncontroversial top pick: cheap, canonical, extremely widely used.

### 2. finRotate
*Logic/Equiv/Fin/Rotate.lean*

**Docstring:**
> Rotate `Fin n` one step to the right.

**Source:**
```lean
def finRotate : ∀ n, Equiv.Perm (Fin n)
  | 0 => Equiv.refl _
  | n + 1 => finAddFlip.trans (finCongr (Nat.add_comm 1 n))
```

**Raw supply numbers:** mention_count=31, theorem_mention_count=18, enumerable_arg_count=1, is_predicate_shaped=False, classifies_structure=False, executable=True, output_decidable_eq=True, dependency_raw (referenced_constants count)=6
**Axiom set:** Quot.sound, propext
**Score:** 46.94 (quality=4, breadth=2, in_degree=18, dependency=6)
**Notes:** The `n + 1` case delegates to `finAddFlip.trans (finCongr ...)` (both defined elsewhere) — the real combinatorial content of the rotation lives there, not here.

### 3. Nat.log
*Data/Nat/Log.lean*

**Docstring:**
> `log b n`, is the logarithm of natural number `n` in base `b`. It returns the largest `k : ℕ`
> such that `b^k ≤ n`, so if `b^k = n`, it returns exactly `k`.

**Source:**
```lean
def log (b n : ℕ) : ℕ :=
  if b ≤ 1 then 0 else (go b n).2 where
  /-- An auxiliary definition for `Nat.log`.

  For `b > 1`, `n ≠ 0`, `n < b ^ fuel`, `Nat.log.go n b fuel = (n / b ^ b.log n, b.log n)`. -/
  go : ℕ → ℕ → ℕ × ℕ
  | _, 0 => (n, 0)
  | b, fuel + 1 =>
    if n < b then
      (n, 0)
    else
      let (q, e) := go (b * b) fuel
      if q < b then (q, 2 * e) else (q / b, 2 * e + 1)
```

**Raw supply numbers:** mention_count=56, theorem_mention_count=6, enumerable_arg_count=2, is_predicate_shaped=False, classifies_structure=False, executable=True, output_decidable_eq=True, dependency_raw (referenced_constants count)=1
**Axiom set:** (none)
**Score:** 46.45 (quality=4, breadth=2, in_degree=6, dependency=1)
**Notes:** Has a `where`-clause auxiliary `go` with fuel-based structural recursion (fuel roughly halves via `b * b` each step) — genuine recursion/well-foundedness machinery, not a one-liner. Worth a reviewer's eye on whether facts should target `log` itself or need to reach into `go`.

### 4. Pairwise
*Logic/Pairwise.lean*

**Docstring:**
> A relation `r` holds pairwise if `r i j` for all `i ≠ j`.

**Source:**
```lean
def Pairwise (r : α → α → Prop) :=
  ∀ ⦃i j⦄, i ≠ j → r i j
```

**Raw supply numbers:** mention_count=1451, theorem_mention_count=119, enumerable_arg_count=0, is_predicate_shaped=True, classifies_structure=False, executable=False, output_decidable_eq=False, dependency_raw (referenced_constants count)=3
**Axiom set:** (none)
**Score:** 43.59 (quality=3, breadth=2, in_degree=119, dependency=3)
**Notes:** Simple universal-quantifier wrapper around a caller-supplied relation `r`; nearly all its 'content' is whatever `r` turns out to be at a use site. **Recorded arity is 0**, but the source clearly takes one explicit argument `r : α → α → Prop` — see the summary's note on the `#check`-output parser under-capturing explicit arguments for some signatures.

### 5. Nat.Prime
*Data/Nat/Prime/Defs.lean*

**Docstring:**
> `Nat.Prime p` means that `p` is a prime number, that is, a natural number
>   at least 2 whose only divisors are `p` and `1`.
>   The theorem `Nat.prime_def` witnesses this description of a prime number.

**Source:**
```lean
def Prime (p : ℕ) :=
  Irreducible p
```

**Raw supply numbers:** mention_count=450, theorem_mention_count=21, enumerable_arg_count=1, is_predicate_shaped=True, classifies_structure=False, executable=True, output_decidable_eq=False, dependency_raw (referenced_constants count)=1
**Axiom set:** propext
**Score:** 39.89 (quality=3, breadth=2, in_degree=21, dependency=1)
**Notes:** Thin wrapper: `Prime p := Irreducible p`, a straight rename. All mathematical content lives in `Irreducible`, defined elsewhere and not itself in this batch. `casework_tier` is recorded `none` despite `executable = True` — an artifact of the `DecidableEq(Prop)` check, not a real negative; see the summary's executability-mechanism note.

### 6. Xor
*Logic/Basic.lean*

**Docstring:**
> `Xor a b` is the exclusive-or of propositions.

**Source:**
```lean
def Xor (a b : Prop) := (a ∧ ¬b) ∨ (b ∧ ¬a)
```

**Raw supply numbers:** mention_count=56, theorem_mention_count=8, enumerable_arg_count=0, is_predicate_shaped=True, classifies_structure=False, executable=None, output_decidable_eq=False, dependency_raw (referenced_constants count)=0
**Axiom set:** (none)
**Score:** 38.59 (quality=3, breadth=2, in_degree=8, dependency=0)
**Notes:** Self-contained propositional formula (`(a ∧ ¬b) ∨ (b ∧ ¬a)`), not a delegation to another named definition.

### 7. Multiset.toFinset
*Data/Finset/Dedup.lean*

**Docstring:**
> `toFinset s` removes duplicates from the multiset `s` to produce a finset.

**Source:**
```lean
def toFinset (s : Multiset α) : Finset α :=
  ⟨_, nodup_dedup s⟩
```

**Raw supply numbers:** mention_count=85, theorem_mention_count=6, enumerable_arg_count=0, is_predicate_shaped=False, classifies_structure=True, executable=False, output_decidable_eq=False, dependency_raw (referenced_constants count)=0
**Axiom set:** Classical.choice, Quot.sound, propext
**Score:** 37.84 (quality=3, breadth=2, in_degree=6, dependency=0)
**Notes:** Foundational constructor (subtype-wraps `nodup_dedup s`) — not a concerning delegation, this is the natural place for this content to live.

### 8. Function.Bijective
*Logic/Function/Defs.lean*

**Docstring:**
> A function is called bijective if it is both injective and surjective.

**Source:**
```lean
def Bijective (f : α → β) :=
  Injective f ∧ Surjective f
```

**Raw supply numbers:** mention_count=656, theorem_mention_count=13, enumerable_arg_count=0, is_predicate_shaped=True, classifies_structure=False, executable=False, output_decidable_eq=False, dependency_raw (referenced_constants count)=3
**Axiom set:** (none)
**Score:** 37.14 (quality=3, breadth=2, in_degree=13, dependency=3)
**Notes:** Thin wrapper: a conjunction of `Injective f` and `Surjective f`, both defined elsewhere. All the real content is in those two, not here.

### 9. Set.Pairwise
*Logic/Pairwise.lean*

**Docstring:**
> The relation `r` holds pairwise on the set `s` if `r x y` for all *distinct* `x y ∈ s`.

**Source:**
```lean
protected def Pairwise (s : Set α) (r : α → α → Prop) :=
  ∀ ⦃x⦄, x ∈ s → ∀ ⦃y⦄, y ∈ s → x ≠ y → r x y
```

**Raw supply numbers:** mention_count=180, theorem_mention_count=11, enumerable_arg_count=0, is_predicate_shaped=True, classifies_structure=False, executable=False, output_decidable_eq=False, dependency_raw (referenced_constants count)=4
**Axiom set:** (none)
**Score:** 36.24 (quality=3, breadth=2, in_degree=11, dependency=4)
**Notes:** Same shape and role as rank 4's `Pairwise`, with an added `∈ s` restriction — essentially a near-duplicate concept. Worth deciding whether both need to be separate mining targets, or whether one subsumes the other for task-authoring purposes. Same recorded-arity-0 artifact as rank 4 (source takes two explicit arguments, `s` and `r`).

### 10. ExistsUnique
*Logic/ExistsUnique.lean*

**Docstring:**
> For `p : α → Prop`, `ExistsUnique p` means that there exists a unique `x : α` with `p x`.

**Source:**
```lean
def ExistsUnique (p : α → Prop) := ∃ x, p x ∧ ∀ y, p y → y = x
```

**Raw supply numbers:** mention_count=38, theorem_mention_count=9, enumerable_arg_count=0, is_predicate_shaped=True, classifies_structure=False, executable=False, output_decidable_eq=False, dependency_raw (referenced_constants count)=3
**Axiom set:** (none)
**Score:** 36.14 (quality=3, breadth=2, in_degree=9, dependency=3)
**Notes:** Self-contained foundational logic primitive (`∃ x, p x ∧ ∀ y, p y → y = x`).

### 11. DependsOn
*Logic/Function/DependsOn.lean*

**Docstring:**
> A function `f` depends on `s` if, whenever `x` and `y` coincide over `s`, `f x = f y`.
> 
> It should be interpreted as "`f` _potentially_ depends only on variables in `s`".
> However it might be the case that `f` does not depend at all on variables in `s`,
> for example if `f` is constant. As a consequence, `DependsOn f univ` is always true,
> see `dependsOn_univ`.

**Source:**
```lean
def DependsOn (f : (Π i, α i) → β) (s : Set ι) : Prop :=
  ∀ ⦃x y⦄, (∀ i ∈ s, x i = y i) → f x = f y
```

**Raw supply numbers:** mention_count=24, theorem_mention_count=10, enumerable_arg_count=0, is_predicate_shaped=True, classifies_structure=False, executable=False, output_decidable_eq=False, dependency_raw (referenced_constants count)=5
**Axiom set:** (none)
**Score:** 35.61 (quality=3, breadth=2, in_degree=10, dependency=5)
**Notes:** Self-contained; has genuine content of its own, not a delegation to another named definition.

### 12. Nat.bit
*Data/Nat/BinaryRec.lean*

**Docstring:**
> `bit b` appends the digit `b` to the little end of the binary representation of
> its natural number input.

**Source:**
```lean
def bit (b : Bool) (n : Nat) : Nat :=
  cond b (2 * n + 1) (2 * n)
```

**Raw supply numbers:** mention_count=53, theorem_mention_count=4, enumerable_arg_count=2, is_predicate_shaped=False, classifies_structure=False, executable=True, output_decidable_eq=True, dependency_raw (referenced_constants count)=1
**Axiom set:** (none)
**Score:** 35.44 (quality=3, breadth=2, in_degree=4, dependency=1)
**Notes:** Self-contained one-liner using `cond`; not a delegation.

### 13. Nat.clog
*Data/Nat/Log.lean*

**Docstring:**
> `clog b n`, is the upper logarithm of natural number `n` in base `b`. It returns the smallest
> `k : ℕ` such that `n ≤ b^k`, so if `b^k = n`, it returns exactly `k`.

**Source:**
```lean
def clog (b n : ℕ) : ℕ :=
  if 1 < b ∧ 1 < n then (go b n).2 + 1 else 0 where
  /-- An auxiliary definition for `Nat.clog`.

  For `n > 1`, `b > 1`, `n ≤ b ^ fuel`, returns `(b ^ clog b n / n, clog b n - 1)`.
  -/
  go : ℕ → ℕ → ℕ × ℕ
  | b, 0 => (b / n, 0)
  | b, fuel + 1 =>
    if n ≤ b then (b / n, 0)
    else
      let (q, e) := go (b * b) fuel
      if q < b then (q, 2 * e + 1) else (q / b, 2 * e)
```

**Raw supply numbers:** mention_count=34, theorem_mention_count=4, enumerable_arg_count=2, is_predicate_shaped=False, classifies_structure=False, executable=True, output_decidable_eq=True, dependency_raw (referenced_constants count)=1
**Axiom set:** (none)
**Score:** 35.44 (quality=3, breadth=2, in_degree=4, dependency=1)
**Notes:** Same shape as rank 3's `Nat.log`: a `where`-clause fuel-recursive auxiliary `go`. `log` and `clog` are duals (floor vs. ceiling log) — both surfacing in the top 25 is expected, not a coincidence, and the same recursion caveat applies.

### 14. List.toFinset
*Data/Finset/Dedup.lean*

**Docstring:**
> `toFinset l` removes duplicates from the list `l` to produce a finset.

**Source:**
```lean
def toFinset (l : List α) : Finset α :=
  Multiset.toFinset l
```

**Raw supply numbers:** mention_count=32, theorem_mention_count=6, enumerable_arg_count=0, is_predicate_shaped=False, classifies_structure=True, executable=False, output_decidable_eq=False, dependency_raw (referenced_constants count)=3
**Axiom set:** Classical.choice, Quot.sound, propext
**Score:** 35.07 (quality=3, breadth=2, in_degree=6, dependency=3)
**Notes:** **Thin wrapper, textbook case**: the entire body is `Multiset.toFinset l`, a one-line delegation to rank 7's `Multiset.toFinset` in this very batch. Exactly the pattern this review was asked to flag.

### 15. IsDvdSequence
*Data/Nat/DvdSequence.lean*

**Docstring:**
> A function `f : α → β` is a divisibility sequence if `a ∣ b` implies `f a ∣ f b`.

**Source:**
```lean
def IsDvdSequence [Dvd α] [Dvd β] (f : α → β) : Prop :=
  ∀ a b, a ∣ b → f a ∣ f b
```

**Raw supply numbers:** mention_count=2, theorem_mention_count=7, enumerable_arg_count=0, is_predicate_shaped=True, classifies_structure=False, executable=False, output_decidable_eq=False, dependency_raw (referenced_constants count)=4
**Axiom set:** (none)
**Score:** 35.02 (quality=3, breadth=2, in_degree=7, dependency=4)
**Notes:** Self-contained `Prop`. The verifier couldn't resolve its instance arguments (`[Dvd α] [Dvd β]`) standalone ("typeclass instance problem is stuck"), so its casework/executability data should be read as inconclusive rather than a genuine negative.

### 16. Finset.image
*Data/Finset/Image.lean*

**Docstring:**
> `image f s` is the forward image of `s` under `f`.

**Source:**
```lean
def image (f : α → β) (s : Finset α) : Finset β :=
  (s.1.map f).toFinset
```

**Raw supply numbers:** mention_count=158, theorem_mention_count=9, enumerable_arg_count=0, is_predicate_shaped=False, classifies_structure=True, executable=False, output_decidable_eq=False, dependency_raw (referenced_constants count)=6
**Axiom set:** Classical.choice, Quot.sound, propext
**Score:** 35.02 (quality=3, breadth=2, in_degree=9, dependency=6)
**Notes:** ⚠ **Data-quality flag**: this row and rank 17 both recorded the name `Finset.image`, but rank 17's real source is `image₂` (binary image) — its trailing `₂` was dropped by the scanner's name regex, colliding with this genuinely different unary `image`. This row (16) is itself fine and correctly verified; it's rank 17's *verification data* that's actually about this definition, not about `image₂`. See the summary for the full list of affected rows.

### 17. Finset.image ⚠
*Data/Finset/NAry.lean*

**Docstring:**
> The image of a binary function `f : α → β → γ` as a function `Finset α → Finset β → Finset γ`.
> Mathematically this should be thought of as the image of the corresponding function `α × β → γ`.

**Source:**
```lean
def image₂ (f : α → β → γ) (s : Finset α) (t : Finset β) : Finset γ :=
  (s ×ˢ t).image <| uncurry f
```

**Raw supply numbers:** mention_count=154, theorem_mention_count=9, enumerable_arg_count=0, is_predicate_shaped=False, classifies_structure=True, executable=False, output_decidable_eq=False, dependency_raw (referenced_constants count)=6
**Axiom set:** Classical.choice, Quot.sound, propext
**Score:** 35.02 (quality=3, breadth=2, in_degree=9, dependency=6)
**Notes:** ⚠ **Data-quality flag**: the manifest's recorded name here, `Finset.image`, is wrong — the source/docstring shown (correctly captured by the pre-filter) are `Finset.image₂`'s own, but the trailing subscript `₂` was dropped when the verifier's `#check`/`#eval`/etc. commands were built, so every verification field (elaborates, arity, executable, axioms, mention count, tiers, score) was actually measured against the *other*, unary `Finset.image` (rank 16) — not against `image₂` itself. `image₂` has not actually been verified; treat this row's tiers/score as unreliable and re-run it under its correct name.

### 18. Int.sqrt
*Data/Int/Sqrt.lean*

**Docstring:**
> `sqrt z` is the square root of an integer `z`. If `z` is positive, it returns the largest
> integer `r` such that `r * r ≤ n`. If it is negative, it returns `0`. For example, `sqrt (-1) = 0`,
> `sqrt 1 = 1`, `sqrt 2 = 1`

**Source:**
```lean
def sqrt (z : ℤ) : ℤ :=
  Nat.sqrt <| Int.toNat z
```

**Raw supply numbers:** mention_count=6, theorem_mention_count=2, enumerable_arg_count=1, is_predicate_shaped=False, classifies_structure=False, executable=True, output_decidable_eq=True, dependency_raw (referenced_constants count)=1
**Axiom set:** (none)
**Score:** 33.91 (quality=3, breadth=2, in_degree=2, dependency=1)
**Notes:** Thin delegation to `Nat.sqrt` (defined elsewhere) after an `Int.toNat` coercion; the real algorithmic content is in `Nat.sqrt`.

### 19. Nat.gcdA
*Data/Int/GCD.lean*

**Docstring:**
> The extended GCD `a` value in the equation `gcd x y = x * a + y * b`.

**Source:**
```lean
def gcdA (x y : ℕ) : ℤ :=
  (xgcd x y).1
```

**Raw supply numbers:** mention_count=7, theorem_mention_count=1, enumerable_arg_count=2, is_predicate_shaped=False, classifies_structure=False, executable=True, output_decidable_eq=True, dependency_raw (referenced_constants count)=1
**Axiom set:** (none)
**Score:** 32.69 (quality=3, breadth=2, in_degree=1, dependency=1)
**Notes:** Thin projection: the `.1` component of `xgcd x y` (defined elsewhere, and itself excluded from this batch — see edge list (b) below, `Nat.xgcd` ranked 106). The real content is in `xgcd`.

### 20. Nat.fib
*Data/Nat/Fib/Basic.lean*

**Docstring:**
> Implementation of the Fibonacci sequence satisfying
> `fib 0 = 0, fib 1 = 1, fib (n + 2) = fib n + fib (n + 1)`.
> 
> *Note:* We use a stream iterator for better performance when compared to the naive recursive
> implementation.

**Source:**
```lean
def fib (n : ℕ) : ℕ :=
  ((fun p : ℕ × ℕ => (p.snd, p.fst + p.snd))^[n] (0, 1)).fst
```

**Raw supply numbers:** mention_count=36, theorem_mention_count=2, enumerable_arg_count=1, is_predicate_shaped=False, classifies_structure=False, executable=True, output_decidable_eq=True, dependency_raw (referenced_constants count)=3
**Axiom set:** (none)
**Score:** 32.52 (quality=3, breadth=2, in_degree=2, dependency=3)
**Notes:** Self-contained, and notably **not** the naive recursive Fibonacci definition — uses an iterated-function (`^[n]`) pair/stream trick for performance, per its own docstring. A good example of a definition whose *implementation strategy* is non-obvious from the mathematical statement alone; worth keeping the docstring's `fib 0 = 0, fib 1 = 1, fib (n+2) = fib n + fib (n+1)` characterization in mind as the actual spec, separate from the implementation.

### 21. Denumerable.raise'Finset
*Logic/Equiv/Finset.lean*

**Docstring:**
> Makes `raise' l n` into a finset. Elements are distinct thanks to `raise'_sorted`.

**Source:**
```lean
def raise'Finset (l : List ℕ) (n : ℕ) : Finset ℕ :=
  ⟨raise' l n, (raise'_sorted _ _).nodup⟩
```

**Raw supply numbers:** mention_count=0, theorem_mention_count=0, enumerable_arg_count=2, is_predicate_shaped=False, classifies_structure=True, executable=True, output_decidable_eq=True, dependency_raw (referenced_constants count)=0
**Axiom set:** Classical.choice, Quot.sound, propext
**Score:** 32.00 (quality=3, breadth=2, in_degree=0, dependency=0)
**Notes:** Thin wrapper: subtype-wraps `raise' l n` (defined elsewhere) with a `nodup` proof; the real content is in `raise'`.

### 22. Nat.digitsAux1
*Data/Nat/Digits/Defs.lean*

**Docstring:**
> (Impl.) An auxiliary definition for `digits`, to help get the desired definitional unfolding.

**Source:**
```lean
def digitsAux1 (n : ℕ) : List ℕ :=
  List.replicate n 1
```

**Raw supply numbers:** mention_count=0, theorem_mention_count=0, enumerable_arg_count=1, is_predicate_shaped=False, classifies_structure=True, executable=True, output_decidable_eq=True, dependency_raw (referenced_constants count)=1
**Axiom set:** (none)
**Score:** 30.61 (quality=3, breadth=2, in_degree=0, dependency=1)
**Notes:** Docstring explicitly says "(Impl.)" — an internal implementation-detail auxiliary ("to help get the desired definitional unfolding"), not a citizen definition in its own right. Worth reconsidering whether an explicitly-marked-internal helper belongs this high; its score comes from supply-proxy numbers, not from being a natural task target.

### 23. Nat.primeFactors
*Data/Nat/PrimeFin.lean*

**Docstring:**
> The prime factors of a natural number as a finset.

**Source:**
```lean
def primeFactors (n : ℕ) : Finset ℕ := n.primeFactorsList.toFinset
```

**Raw supply numbers:** mention_count=36, theorem_mention_count=0, enumerable_arg_count=1, is_predicate_shaped=False, classifies_structure=True, executable=True, output_decidable_eq=True, dependency_raw (referenced_constants count)=1
**Axiom set:** Classical.choice, Quot.sound, propext
**Score:** 30.61 (quality=3, breadth=2, in_degree=0, dependency=1)
**Notes:** Thin delegation to `n.primeFactorsList.toFinset` (both defined elsewhere).

### 24. List.Ico
*Data/List/Intervals.lean*

**Docstring:**
> `Ico n m` is the list of natural numbers `n ≤ x < m`.
> (Ico stands for "interval, closed-open".)
> 
> See also `Mathlib/Order/Interval/Basic.lean` for modelling intervals in general preorders, as well
> as sibling definitions alongside it such as `Set.Ico`, `Multiset.Ico` and `Finset.Ico`
> for sets, multisets and finite sets respectively.

**Source:**
```lean
def Ico (n m : ℕ) : List ℕ :=
  range' n (m - n)
```

**Raw supply numbers:** mention_count=2, theorem_mention_count=0, enumerable_arg_count=2, is_predicate_shaped=False, classifies_structure=True, executable=True, output_decidable_eq=True, dependency_raw (referenced_constants count)=1
**Axiom set:** (none)
**Score:** 30.61 (quality=3, breadth=2, in_degree=0, dependency=1)
**Notes:** Thin delegation to `range'` (defined elsewhere) with an argument transform (`m - n`).

### 25. Cycle
*Data/List/Cycle.lean*

**Docstring:**
> `Cycle α` is the quotient of `List α` by cyclic permutation.
> Duplicates are allowed.

**Source:**
```lean
def Cycle (α : Type*) : Type _ :=
  Quotient (IsRotated.setoid α)
```

**Raw supply numbers:** mention_count=1664, theorem_mention_count=41, enumerable_arg_count=0, is_predicate_shaped=False, classifies_structure=False, executable=False, output_decidable_eq=False, dependency_raw (referenced_constants count)=2
**Axiom set:** Quot.sound, propext
**Score:** 30.02 (quality=2, breadth=1, in_degree=41, dependency=2)
**Notes:** A **type-former** (returns `Type _`, not a value or `Prop`) — a `Quotient` of `List α` by rotation. Structurally different from every other entry in the top 25, all of which return a value or `Prop`; casework/membership tiers likely don't mean the same thing for a type-valued definition, and this is worth a second look before treating it like the others.

## 4. Edge lists

### (a) 10 lowest-ranked included -- the marginal cases

| Rank | Name | Module | Tiers (CW/Mem/Glob) | Score |
|---|---|---|---|---|
| 91 | Relator.LeftUnique | Logic/Relator.lean | none/thin/thin | 20.86 |
| 92 | Nat.bits | Data/Nat/Bits.lean | none/thin/thin | 20.50 |
| 93 | List.destutter' | Data/List/Defs.lean | none/thin/thin | 20.50 |
| 94 | List.iterate | Data/List/Defs.lean | none/thin/thin | 20.50 |
| 95 | List.destutter | Data/List/Defs.lean | none/thin/thin | 20.19 |
| 96 | List.kerase | Data/List/Sigma.lean | none/thin/thin | 20.19 |
| 97 | List.orderedInsert | Data/List/Sort.lean | none/thin/thin | 20.19 |
| 98 | Finset.sort | Data/Finset/Sort.lean | none/thin/thin | 19.92 |
| 99 | Nat.centralBinom | Data/Nat/Choose/Central.lean | rich/none/none | 19.61 |
| 100 | Nat.ascFactorialBinary | Data/Nat/Factorial/Basic.lean | rich/none/none | 19.61 |

### (b) 10 highest-ranked excluded (verified but outranked) -- what just missed

| Rank | Name | Module | Tiers (CW/Mem/Glob) | Score |
|---|---|---|---|---|
| 101 | Nat.factorialBinarySplitting | Data/Nat/Factorial/Basic.lean | rich/none/none | 19.61 |
| 102 | Nat.descFactorialBinary | Data/Nat/Factorial/Basic.lean | rich/none/none | 19.61 |
| 103 | Nat.fastFib | Data/Nat/Fib/Basic.lean | rich/none/none | 19.61 |
| 104 | Nat.divMaxPow | Data/Nat/MaxPowDiv.lean | rich/none/none | 19.61 |
| 105 | Nat.minFac | Data/Nat/Prime/Defs.lean | rich/none/none | 19.61 |
| 106 | Nat.xgcd | Data/Int/GCD.lean | rich/none/none | 19.61 |
| 107 | Nat.gcdB | Data/Int/GCD.lean | rich/none/none | 19.61 |
| 108 | Int.natMod | Data/Int/Init.lean | rich/none/none | 19.61 |
| 109 | Nat.beta | Logic/Godel/GodelBetaFunction.lean | rich/none/none | 19.61 |
| 110 | Nat.fast_choose | Data/Nat/Choose/Basic.lean | rich/none/none | 18.80 |

### (c) Lopsided-extreme included definitions -- rich in exactly one tier, none in both others

Per the design discussion, breadth is only a soft/tie-breaking preference, so a lopsided-but-excellent candidate is allowed to outrank a well-rounded-but-mediocre one. These are the ones that made it through on the strength of a single tier alone.

27 of the 100 included definitions qualify.

| Rank | Name | Module | Rich tier | Score |
|---|---|---|---|---|
| 25 | Cycle | Data/List/Cycle.lean | Global | 30.02 |
| 26 | finSuccEquiv | Logic/Equiv/Fin/Basic.lean | Global | 29.50 |
| 27 | finSuccEquiv' | Logic/Equiv/Fin/Basic.lean | Global | 29.50 |
| 30 | Equiv.swap | Logic/Equiv/Basic.lean | Global | 28.92 |
| 32 | Nat.find | Data/Nat/Find.lean | Global | 28.58 |
| 33 | Equiv.symm | Logic/Equiv/Defs.lean | Global | 28.19 |
| 36 | finSumFinEquiv | Logic/Equiv/Fin/Basic.lean | Global | 26.84 |
| 40 | PartialEquiv.refl | Logic/Equiv/PartialEquiv.lean | Global | 26.72 |
| 44 | Nat.choose | Data/Nat/Choose/Basic.lean | Global | 25.42 |
| 47 | Nat.findGreatest | Data/Nat/Find.lean | Global | 25.24 |
| 48 | Finset.card | Data/Finset/Card.lean | Global | 25.04 |
| 49 | Function.update | Logic/Function/Basic.lean | Global | 25.03 |
| 50 | hyperoperation | Data/Nat/Hyperoperation.lean | Global | 24.97 |
| 51 | Pi.map | Logic/Function/Defs.lean | Global | 24.82 |
| 52 | Relation.Map | Logic/Relation.lean | Global | 24.76 |
| 53 | Nat.Primes | Data/Nat/Prime/Defs.lean | Global | 24.18 |
| 59 | Equiv.Set.sumCompl | Logic/Equiv/Set.lean | Global | 23.62 |
| 61 | Nat.multinomial | Data/Nat/Choose/Multinomial.lean | Global | 23.16 |
| 71 | finAddFlip | Logic/Equiv/Fin/Basic.lean | Global | 22.79 |
| 78 | Finset.fold | Data/Finset/Fold.lean | Global | 21.77 |
| 85 | Nat.dist | Data/Nat/Dist.lean | Casework | 21.00 |
| 86 | Nat.factorization | Data/Nat/Factorization/Defs.lean | Casework | 21.00 |
| 87 | Nat.pair | Data/Nat/Pairing.lean | Casework | 21.00 |
| 88 | Int.succ | Data/Int/Init.lean | Casework | 21.00 |
| 89 | Int.pred | Data/Int/Init.lean | Casework | 21.00 |
| 99 | Nat.centralBinom | Data/Nat/Choose/Central.lean | Casework | 19.61 |
| 100 | Nat.ascFactorialBinary | Data/Nat/Factorial/Basic.lean | Casework | 19.61 |
