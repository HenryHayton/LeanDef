# Harvest Batch 1 Review

Human-readable review of the first mechanical harvest (`miner/output/harvest_manifest.jsonl`), generated read-only from that file. See `docs/design/` for the design docs this harvest feeds, and the miner-stage-1 task summary for the pipeline that produced it.

**This is revision 2** (full re-harvest after four miner fixes). See §0 for what changed and why; §1 onward describe the current manifest exactly as revision 1 described its own, so the two are directly comparable.

## 0. Revision 2 changelog

Four fixes landed since revision 1, all confirmed by unit tests before this re-harvest ran, and all visible below:

1. **Identifier regex** (`miner/scan.py`): the pre-filter's name regex didn't include Lean's unicode subscript characters, so `image₂`, `Semiconj₂`, and four `map₂...` variants were scanned with their trailing subscript silently dropped, colliding with (and overwriting the verification data of) a real, different definition each. Fixed by switching to a `\w`-based identifier class matching Lean's actual `isIdFirst`/`isIdRest`/`isLetterLike`/`isSubScriptAlnum` grammar. **All six now resolve to their own identity** and have never been confused with another name's data:

   | Name | Rev 1 (wrong) rank | Rev 2 rank | Rev 2 included? |
   |---|---|---|---|
   | `Finset.image₂` | — (recorded as `Finset.image`, rank 17) | 102 | No (just outranked) |
   | `Function.Semiconj₂` | — (recorded as `Function.Semiconj`, rank 76) | 314 | No |
   | `List.map₂Left'` | — (recorded as `List.map`, rank 64) | 386 | No |
   | `List.map₂Right'` | — (recorded as `List.map`, rank 65) | 331 | No |
   | `List.map₂Left` | — (recorded as `List.map`, rank 66) | 387 | No |
   | `List.map₂Right` | — (recorded as `List.map`, rank 67) | 332 | No |

   None of the six are executable under this stage's canonical-input scheme (all take a generic function argument, not one of the enumerable types), so all six score in the `none/thin/thin`-to-`none/none/none` range on their own genuine data — correctly outranked now, rather than incorrectly ranked ~17–76 on borrowed data.

2. **Arity from types, not headers** (`miner/verify.py`): arity/argument types are now derived by parsing the pretty-printed type from `#check` (counting binders) instead of the `def` source header. Root cause of revision 1's "0 explicit arguments" rows turned out to be **two** distinct parser gaps, not the single "section variable" guess revision 1's own note speculated:
   - A **universe-parameter annotation** (`.{u_1}`, `.{u₁, u₂}`) that Lean's `#check` output attaches directly to a polymorphic name, before any binder groups. The old parser choked on the unexpected leading `.` and returned *zero* binder groups — not just missing the universe params, but silently discarding every named argument too. This affected essentially any universe-polymorphic definition, i.e. most of Mathlib, independent of whether its own header wrote its arguments out (e.g. `Finset.card`, `Nat.choose`).
   - **Trailing anonymous arrow-chain arguments**: a definition written header-less/pattern-matched-style (`def digits : ℕ → ℕ → List ℕ`) or relying on a section `variable` never repeated in its own header renders as a bare arrow chain in `#check`'s output, not a named `(x : T)` group. Now split out via `_split_top_level_arrows` and counted as trailing explicit arguments.

   The task's three named acceptance-criterion cases, confirmed fixed:

   | Name | Rev 1 arity | Rev 2 arity | Rev 2 signature |
   |---|---|---|---|
   | `Pairwise` | 0 | 1 | `{α : Type u_1} (r : α → α → Prop) : Prop` |
   | `Function.Bijective` | 0 | 1 | `{α : Sort u₁} {β : Sort u₂} (f : α → β) : Prop` |
   | `List.orderedInsert` | 0 | 3 | `(r : α → α → Prop) (a : α) (l : List α) : List α` |

   Also fixed, not previously named: `Set.Pairwise` (0→2), `List.kerase` (0→2), `Finset.card` (0→1), `Nat.choose` (0→2), `Nat.digits` (0→2), `Nat.bits` (0→1), `hyperoperation` (0→3), `Int.bodd` (0→1), and roughly a third of the manifest overall — this bug was pervasive, not an edge case. A dedicated regression-test file, `tests/test_miner_verify_parsing.py`, pins all three named cases plus `List.kerase`/`Nat.Prime` against their exact observed `#check` strings.

3. **Prop-valued supply semantics** (`miner/proxies.py`, `miner/verify.py`): the literal `DecidableEq (<return type>)` check — meaningless for `Prop`, since `DecidableEq Prop` is not a real Mathlib instance — is gone. Casework/membership supply for a `Prop`-valued definition is now determined by `exec_mechanism == "decide"` (Lean's own `#eval`-decide-fallback succeeding), via a new `_is_concretely_checkable` helper shared by both tiers. `Nat.Prime` is the direct acceptance-criterion case:

   | | Rev 1 | Rev 2 |
   |---|---|---|
   | `casework_tier` | None | **Rich** |
   | `membership_tier` | Thin | **Rich** |
   | Score | 39.89 | **70.89** |
   | Rank | 5 | **1** |

   `proxies.py`'s module docstring now documents why a decidable predicate coming out rich in *both* tiers is intentional (a stage-2 fact-authoring judgment call, not something stage-1 supply data should or can disambiguate), not a bug. `Nat.ModEq` and `Int.ModEq` are further, previously-unranked beneficiaries of the same fix (both entered the top 100 for the first time — see §2).

4. **Curation overrides** (new: `miner/curation.yaml`, `miner/rank.py`): a human-editable YAML file of `{name, action, reason}` entries, applied as a final pass after mechanical ranking (`exclude` / `demote` / `note`), with every application recorded on the manifest record's new `curation_applied` field for auditability. Seeded with exactly two logical entries this round:
   - **`Nat.digitsAux1`** (was rank 22 in revision 1) — `exclude`, "internal implementation-detail auxiliary, not a citizen definition" (its own docstring says "(Impl.)"). Now `included: false` with that reason, regardless of its mechanical score.
   - **`Pairwise`** and **`Set.Pairwise`** (ranks 8 and 16 in revision 2) — `note`, flagging their near-duplicate relationship for a human reviewer; ranking/inclusion untouched.

   Further curation entries are out of scope for this task — that file is meant to be hand-edited going forward, not regenerated by future harvest runs.

### Corpus-count deltas vs revision 1

| | Rev 1 | Rev 2 |
|---|---|---|
| Scanned | 782 | 782 |
| Verified (elaborates) | 767 | 768 |
| Included (top 100) | 100 | 100 |
| Does not elaborate | 15 | 14 |
| Curation-excluded | (mechanism didn't exist) | 1 |

Scanned count is identical (`TARGET_MODULES` untouched, per this task's explicit constraint). The elaborates count moved by one; not investigated further here since it's within the kind of run-to-run noise a live Mathlib environment can produce (timing-sensitive typeclass search, etc.), not something either fix targets.

## 1. Summary

### Corpus counts

- **Scanned** (pre-filter `def` hits, all 5 target corners): 782
- **Verified** (elaborates in the live environment, regardless of rank): 768
- **Included** (top 100 by rank): 100
- **Excluded**: 682
  - verified but outranked (below top 100): 667
  - curation-excluded: 1
  - does not elaborate: 14

### Supply tier distribution (100 included)

| Tier | Casework | Membership | Global |
|---|---|---|---|
| Rich | 36 | 4 | 34 |
| Thin | 0 | 70 | 48 |
| None | 64 | 26 | 18 |

Casework and membership both got materially richer than revision 1 (casework Rich 24→36, membership Rich 0→4) — the direct, expected effect of fixes 2 and 3 above.

### Distribution across source modules (100 included)

| Module | Count |
|---|---|
| Data/Finset | 29 |
| Data/Nat | 25 |
| Logic/Equiv | 16 |
| Data/List | 9 |
| Data/Int | 6 |
| Logic/Function | 6 |
| Logic/Relator.lean | 3 |
| Logic/Pairwise.lean | 2 |
| Logic/Basic.lean | 1 |
| Logic/ExistsUnique.lean | 1 |
| Logic/Relation.lean | 1 |
| Logic/Godel | 1 |

### Executability-mechanism split (100 included)

- **eval** (concrete return type, `#eval` on canonical inputs succeeded): 33
- **decide** (`Prop`-valued, genuinely decidable in practice): 3
- **none** (neither confirmed executable): 64

The `decide` count (1 → 3) is small in absolute terms because most `Prop`-valued candidates in this corpus genuinely aren't concretely decidable (abstract relations, quantifiers over an unbounded domain) — fix 3 stopped *miscounting* decidable ones as `none`, it didn't and couldn't manufacture decidability that isn't there. `Nat.Prime`, `Nat.ModEq`, `Int.ModEq` are the three.

## 2. Full ranked table (all 100 included)

Description: docstring (truncated to fit) where present. `Curation` column shows `note` for the two entries flagged in `miner/curation.yaml`; curation-excluded and demoted rows never reach this table's top 100 (see §0 item 4 and the edge lists in §4).

| Rank | Name | Module | Description | Arity | Signature | CW | Mem | Glob | Mentions | Deps | Score (components) | Curation |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Nat.Prime | Data/Nat/Prime/Defs.lean | `Nat.Prime p` means that `p` is a prime number, that is, a natural number at least 2 wh… | 1 | `(p : ℕ) : Prop` | Rich | Rich | Rich | 21 | 1 | 70.89 (q=6, b=3, deg=21, dep=1) | |
| 2 | Finset.range | Data/Finset/Range.lean | `range n` is the set of natural numbers less than `n`. | 1 | `(n : ℕ) : Finset ℕ` | Rich | Thin | Rich | 27 | 0 | 63.00 (q=5, b=3, deg=27, dep=0) | |
| 3 | Int.bodd | Data/Int/Bitwise.lean | `bodd n` returns `true` if `n` is odd | 1 | `: ℤ → Bool` | Rich | Rich | Thin | 1 | 5 | 51.50 (q=5, b=3, deg=1, dep=5) | |
| 4 | finRotate | Logic/Equiv/Fin/Rotate.lean | Rotate `Fin n` one step to the right. | 1 | `(n : ℕ) : Equiv.Perm (Fin n)` | Rich | None | Rich | 18 | 6 | 46.94 (q=4, b=2, deg=18, dep=6) | |
| 5 | Nat.log | Data/Nat/Log.lean | `log b n`, is the logarithm of natural number `n` in base `b`. It returns the largest `k … | 2 | `(b n : ℕ) : ℕ` | Rich | None | Rich | 6 | 1 | 46.45 (q=4, b=2, deg=6, dep=1) | |
| 6 | Nat.choose | Data/Nat/Choose/Basic.lean | `choose n k` is the number of `k`-element subsets in an `n`-element set. Also known as bi… | 2 | `: ℕ → ℕ → ℕ` | Rich | None | Rich | 10 | 3 | 46.42 (q=4, b=2, deg=10, dep=3) | |
| 7 | hyperoperation | Data/Nat/Hyperoperation.lean | Implementation of the hyperoperation sequence where `hyperoperation n m k` is the `n`th h… | 3 | `: ℕ → ℕ → ℕ → ℕ` | Rich | None | Rich | 10 | 4 | 45.97 (q=4, b=2, deg=10, dep=4) | |
| 8 | Pairwise | Logic/Pairwise.lean | A relation `r` holds pairwise if `r i j` for all `i ≠ j`. | 1 | `{α : Type u_1} (r : α → α → Prop) : Prop` | None | Thin | Rich | 119 | 2 | 44.17 (q=3, b=2, deg=119, dep=2) | note |
| 9 | Nat.digits | Data/Nat/Digits/Defs.lean | `digits b n` gives the digits, in little-endian order, of a natural number `n` in a speci… | 2 | `: ℕ → ℕ → List ℕ` | Rich | Thin | Thin | 2 | 7 | 42.14 (q=4, b=3, deg=2, dep=7) | |
| 10 | Nat.ModEq | Data/Nat/ModEq.lean | Modular equality. `n.ModEq a b`, or `a ≡ b [MOD n]`, means that `a % n = b % n`. | 3 | `(n a b : ℕ) : Prop` | Rich | Rich | None | 0 | 0 | 42.00 (q=4, b=2, deg=0, dep=0) | |
| 11 | Int.ModEq | Data/Int/ModEq.lean | `a ≡ b [ZMOD n]` when `a % n = b % n`. | 3 | `(n a b : ℤ) : Prop` | Rich | Rich | None | 0 | 0 | 42.00 (q=4, b=2, deg=0, dep=0) | |
| 12 | Nat.bits | Data/Nat/Bits.lean | `bits n` returns a list of Bools which correspond to the binary representation of n, wher… | 1 | `: ℕ → List Bool` | Rich | Thin | Thin | 1 | 5 | 41.50 (q=4, b=3, deg=1, dep=5) | |
| 13 | Xor | Logic/Basic.lean | `Xor a b` is the exclusive-or of propositions. | 2 | `(a b : Prop) : Prop` | None | Thin | Rich | 8 | 0 | 38.59 (q=3, b=2, deg=8, dep=0) | |
| 14 | Multiset.toFinset | Data/Finset/Dedup.lean | `toFinset s` removes duplicates from the multiset `s` to produce a finset. | 1 | `{α : Type u_1} [DecidableEq α] (s : Multiset α) : Finset α` | None | Thin | Rich | 6 | 0 | 37.84 (q=3, b=2, deg=6, dep=0) | |
| 15 | Function.Bijective | Logic/Function/Defs.lean | A function is called bijective if it is both injective and surjective. | 1 | `{α : Sort u₁} {β : Sort u₂} (f : α → β) : Prop` | None | Thin | Rich | 13 | 2 | 37.72 (q=3, b=2, deg=13, dep=2) | |
| 16 | Set.Pairwise | Logic/Pairwise.lean | The relation `r` holds pairwise on the set `s` if `r x y` for all *distinct* `x y ∈ s`. | 2 | `{α : Type u_1} (s : Set α) (r : α → α → Prop) : Prop` | None | Thin | Rich | 11 | 2 | 37.26 (q=3, b=2, deg=11, dep=2) | note |
| 17 | Finset.card | Data/Finset/Card.lean | `s.card` is the number of elements of `s`, aka its cardinality. The notation `#s` can be… | 1 | `{α : Type u_1} (s : Finset α) : ℕ` | None | Thin | Rich | 7 | 1 | 36.85 (q=3, b=2, deg=7, dep=1) | |
| 18 | ExistsUnique | Logic/ExistsUnique.lean | For `p : α → Prop`, `ExistsUnique p` means that there exists a unique `x : α` with `p x`. | 1 | `{α : Sort u_1} (p : α → Prop) : Prop` | None | Thin | Rich | 9 | 2 | 36.71 (q=3, b=2, deg=9, dep=2) | |
| 19 | Relation.Map | Logic/Relation.lean | The map of a relation `r` through a pair of functions pushes the relation to the codomain… | 5 | `{α : Type u_1} {β : Type u_2} {γ : Type u_3} {δ : Type u_4} (r : α → β → Prop) (f : α → γ) (g : β → δ) : γ → δ → Prop` | None | Thin | Rich | 13 | 4 | 36.70 (q=3, b=2, deg=13, dep=4) | |
| 20 | DependsOn | Logic/Function/DependsOn.lean | A function `f` depends on `s` if, whenever `x` and `y` coincide over `s`, `f x = f y`. I… | 2 | `{ι : Type u_1} {α : ι → Type u_2} {β : Type u_3} (f : ((i : ι) → α i) → β) (s : Set ι) : Prop` | None | Thin | Rich | 10 | 3 | 36.42 (q=3, b=2, deg=10, dep=3) | |
| 21 | Finset.image | Data/Finset/Image.lean | `image f s` is the forward image of `s` under `f`. | 2 | `{α : Type u_1} {β : Type u_2} [DecidableEq β] (f : α → β) (s : Finset α) : Finset β` | None | Thin | Rich | 9 | 4 | 35.69 (q=3, b=2, deg=9, dep=4) | |
| 22 | List.toFinset | Data/Finset/Dedup.lean | `toFinset l` removes duplicates from the list `l` to produce a finset. | 1 | `{α : Type u_1} [DecidableEq α] (l : List α) : Finset α` | None | Thin | Rich | 6 | 2 | 35.64 (q=3, b=2, deg=6, dep=2) | |
| 23 | IsDvdSequence | Data/Nat/DvdSequence.lean | A function `f : α → β` is a divisibility sequence if `a ∣ b` implies `f a ∣ f b`. | 1 | `{α : Type u_1} {β : Type u_2} [Dvd α] [Dvd β] (f : α → β) : Prop` | None | Thin | Rich | 7 | 3 | 35.47 (q=3, b=2, deg=7, dep=3) | |
| 24 | Nat.bit | Data/Nat/BinaryRec.lean | `bit b` appends the digit `b` to the little end of the binary representation of its natur… | 2 | `(b : Bool) (n : ℕ) : ℕ` | Rich | None | Thin | 4 | 1 | 35.44 (q=3, b=2, deg=4, dep=1) | |
| 25 | Nat.clog | Data/Nat/Log.lean | `clog b n`, is the upper logarithm of natural number `n` in base `b`. It returns the smal… | 2 | `(b n : ℕ) : ℕ` | Rich | None | Thin | 4 | 1 | 35.44 (q=3, b=2, deg=4, dep=1) | |
| 26 | Nat.multinomial | Data/Nat/Choose/Multinomial.lean | The multinomial coefficient. Gives the number of strings consisting of symbols from `s`, … | 2 | `{α : Type u_1} (s : Finset α) (f : α → ℕ) : ℕ` | None | Thin | Rich | 5 | 2 | 35.18 (q=3, b=2, deg=5, dep=2) | |
| 27 | Equiv.Set.sumCompl | Logic/Equiv/Set.lean | If `s : Set α` is a set with decidable membership, then `s ⊕ sᶜ` is equivalent to `α`. S… | 1 | `{α : Type u_3} (s : Set α) [DecidablePred fun x => x ∈ s] : ↑s ⊕ ↑sᶜ ≃ α` | None | Thin | Rich | 6 | 3 | 35.07 (q=3, b=2, deg=6, dep=3) | |
| 28 | Int.sqrt | Data/Int/Sqrt.lean | `sqrt z` is the square root of an integer `z`. If `z` is positive, it returns the largest… | 1 | `(z : ℤ) : ℤ` | Rich | None | Thin | 2 | 1 | 33.91 (q=3, b=2, deg=2, dep=1) | |
| 29 | Finset.fold | Data/Finset/Fold.lean | `fold op b f s` folds the commutative associative operation `op` over the `f`-image of … | 4 | `{α : Type u_1} {β : Type u_2} (op : β → β → β) [hc : Std.Commutative op] [ha : Std.Associative op] (b : β) (f : α → β) (s : Finset α) : β` | None | Thin | Rich | 5 | 5 | 33.79 (q=3, b=2, deg=5, dep=5) | |
| 30 | Nat.shiftLeft' | Data/Nat/Bits.lean | `shiftLeft' b m n` performs a left shift of `m` `n` times and adds the bit `b` as the lea… | 3 | `(b : Bool) (m : ℕ) : ℕ → ℕ` | Rich | None | Thin | 3 | 3 | 33.39 (q=3, b=2, deg=3, dep=3) | |
| 31 | Nat.gcdA | Data/Int/GCD.lean | The extended GCD `a` value in the equation `gcd x y = x * a + y * b`. | 2 | `(x y : ℕ) : ℤ` | Rich | None | Thin | 1 | 1 | 32.69 (q=3, b=2, deg=1, dep=1) | |
| 32 | Nat.fib | Data/Nat/Fib/Basic.lean | Implementation of the Fibonacci sequence satisfying `fib 0 = 0, fib 1 = 1, fib (n + 2) = … | 1 | `(n : ℕ) : ℕ` | Rich | None | Thin | 2 | 3 | 32.52 (q=3, b=2, deg=2, dep=3) | |
| 33 | Int.xor | Data/Int/Bitwise.lean | `xor` computes the bitwise `xor` of two natural numbers | 2 | `: ℤ → ℤ → ℤ` | Rich | None | Thin | 3 | 6 | 32.27 (q=3, b=2, deg=3, dep=6) | |
| 34 | Denumerable.raise'Finset | Logic/Equiv/Finset.lean | Makes `raise' l n` into a finset. Elements are distinct thanks to `raise'_sorted`. | 2 | `(l : List ℕ) (n : ℕ) : Finset ℕ` | Rich | Thin | None | 0 | 0 | 32.00 (q=3, b=2, deg=0, dep=0) | |
| 35 | Nat.multichoose | Data/Nat/Choose/Basic.lean | `multichoose n k` is the number of multisets of cardinality `k` from a type of cardinalit… | 2 | `: ℕ → ℕ → ℕ` | Rich | None | Thin | 1 | 3 | 31.31 (q=3, b=2, deg=1, dep=3) | |
| 36 | Nat.factorial | Data/Nat/Factorial/Basic.lean | `Nat.factorial n` is the factorial of `n`. | 1 | `: ℕ → ℕ` | Rich | None | Thin | 1 | 3 | 31.31 (q=3, b=2, deg=1, dep=3) | |
| 37 | Nat.primeFactors | Data/Nat/PrimeFin.lean | The prime factors of a natural number as a finset. | 1 | `(n : ℕ) : Finset ℕ` | Rich | Thin | None | 0 | 1 | 30.61 (q=3, b=2, deg=0, dep=1) | |
| 38 | List.Ico | Data/List/Intervals.lean | `Ico n m` is the list of natural numbers `n ≤ x < m`. (Ico stands for "interval, closed-o… | 2 | `(n m : ℕ) : List ℕ` | Rich | Thin | None | 0 | 1 | 30.61 (q=3, b=2, deg=0, dep=1) | |
| 39 | Cycle | Data/List/Cycle.lean | `Cycle α` is the quotient of `List α` by cyclic permutation. Duplicates are allowed. | 1 | `(α : Type u_1) : Type u_1` | None | None | Rich | 41 | 2 | 30.02 (q=2, b=1, deg=41, dep=2) | |
| 40 | finSuccEquiv | Logic/Equiv/Fin/Basic.lean | Equivalence between `Fin (n + 1)` and `Option (Fin n)`. This is a version of `Fin.pred` t… | 1 | `(n : ℕ) : Fin (n + 1) ≃ Option (Fin n)` | None | None | Rich | 26 | 1 | 29.50 (q=2, b=1, deg=26, dep=1) | |
| 41 | finSuccEquiv' | Logic/Equiv/Fin/Basic.lean | An equivalence that removes `i` and maps it to `none`. This is a version of `Fin.predAbov… | 1 | `{n : ℕ} (i : Fin (n + 1)) : Fin (n + 1) ≃ Option (Fin n)` | None | None | Rich | 16 | 0 | 29.50 (q=2, b=1, deg=16, dep=0) | |
| 42 | Nat.digitsAux0 | Data/Nat/Digits/Defs.lean | (Impl.) An auxiliary definition for `digits`, to help get the desired definitional unfold… | 1 | `: ℕ → List ℕ` | Rich | Thin | None | 0 | 3 | 29.23 (q=3, b=2, deg=0, dep=3) | |
| 43 | Nat.digitsAppend | Data/Nat/Digits/Lemmas.lean | The list of digits of `n` in base `b` with some `0`'s appended so that its length is equa… | 3 | `(b l n : ℕ) : List ℕ` | Rich | Thin | None | 0 | 3 | 29.23 (q=3, b=2, deg=0, dep=3) | |
| 44 | List.Nat.antidiagonal | Data/List/NatAntidiagonal.lean | The antidiagonal of a natural number `n` is the list of pairs `(i, j)` such that `i + j =… | 1 | `(n : ℕ) : List (ℕ × ℕ)` | Rich | Thin | None | 0 | 3 | 29.23 (q=3, b=2, deg=0, dep=3) | |
| 45 | List.ranges | Data/List/Range.lean | From `l : List ℕ`, construct `l.ranges : List (List ℕ)` such that `l.ranges.map List.leng… | 1 | `: List ℕ → List (List ℕ)` | Rich | Thin | None | 0 | 3 | 29.23 (q=3, b=2, deg=0, dep=3) | |
| 46 | Equiv.swap | Logic/Equiv/Basic.lean | `swap a b` is the permutation that swaps `a` and `b` and leaves other values as is. | 2 | `{α : Sort u_1} [DecidableEq α] (a b : α) : Equiv.Perm α` | None | None | Rich | 13 | 0 | 28.92 (q=2, b=1, deg=13, dep=0) | |
| 47 | Int.range | Data/Int/Range.lean | List enumerating `[m, n)`. This is the ℤ variant of `List.Ico`. | 2 | `(m n : ℤ) : List ℤ` | Rich | Thin | None | 0 | 4 | 28.78 (q=3, b=2, deg=0, dep=4) | |
| 48 | Denumerable.lower' | Logic/Equiv/Finset.lean | Outputs the list of differences minus one of the input list, that is `lower' [a₁, a₂, a₃,… | 2 | `: List ℕ → ℕ → List ℕ` | Rich | Thin | None | 0 | 4 | 28.78 (q=3, b=2, deg=0, dep=4) | |
| 49 | Denumerable.raise' | Logic/Equiv/Finset.lean | Outputs the list of partial sums plus one of the input list, that is `raise [a₁, a₂, a₃, … | 2 | `: List ℕ → ℕ → List ℕ` | Rich | Thin | None | 0 | 4 | 28.78 (q=3, b=2, deg=0, dep=4) | |
| 50 | Denumerable.lower | Logic/Equiv/Multiset.lean | Outputs the list of differences of the input list, that is `lower [a₁, a₂, ...] n = [a₁ -… | 2 | `: List ℕ → ℕ → List ℕ` | Rich | Thin | None | 0 | 4 | 28.78 (q=3, b=2, deg=0, dep=4) | |
| 51 | Denumerable.raise | Logic/Equiv/Multiset.lean | Outputs the list of partial sums of the input list, that is `raise [a₁, a₂, ...] n = [n +… | 2 | `: List ℕ → ℕ → List ℕ` | Rich | Thin | None | 0 | 4 | 28.78 (q=3, b=2, deg=0, dep=4) | |
| 52 | Nat.find | Data/Nat/Find.lean | If `p` is a (decidable) predicate on `ℕ` and `hp : ∃ (n : ℕ), p n` is a proof that there … | 1 | `{p : ℕ → Prop} [DecidablePred p] (H : ∃ n, p n) : ℕ` | None | None | Rich | 25 | 2 | 28.58 (q=2, b=1, deg=25, dep=2) | |
| 53 | Nat.primeFactorsList | Data/Nat/Factors.lean | `primeFactorsList n` is the prime factorization of `n`, listed in increasing order. | 1 | `: ℕ → List ℕ` | Rich | Thin | None | 0 | 5 | 28.42 (q=3, b=2, deg=0, dep=5) | |
| 54 | Equiv.symm | Logic/Equiv/Defs.lean | Inverse of an equivalence `e : α ≃ β`. | 1 | `{α : Sort u} {β : Sort v} (e : α ≃ β) : β ≃ α` | None | None | Rich | 10 | 0 | 28.19 (q=2, b=1, deg=10, dep=0) | |
| 55 | Nat.bitIndices | Data/Nat/BitIndices.lean | The function which maps each natural number `∑ i ∈ s, 2 ^ i` to the list of elements of `… | 1 | `(n : ℕ) : List ℕ` | Rich | Thin | None | 0 | 6 | 28.11 (q=3, b=2, deg=0, dep=6) | |
| 56 | Nat.unbeta | Logic/Godel/GodelBetaFunction.lean | Inverse of Gödel's Beta Function. This is similar to `Encodable.encodeList`, but it is ea… | 1 | `(l : List ℕ) : ℕ` | Rich | Thin | None | 0 | 7 | 27.84 (q=3, b=2, deg=0, dep=7) | |
| 57 | finSumFinEquiv | Logic/Equiv/Fin/Basic.lean | Equivalence between `Fin m ⊕ Fin n` and `Fin (m + n)` | 0 | `{m n : ℕ} : Fin m ⊕ Fin n ≃ Fin (m + n)` | None | None | Rich | 6 | 0 | 26.84 (q=2, b=1, deg=6, dep=0) | |
| 58 | Finset.disjUnion | Data/Finset/Disjoint.lean | `disjUnion s t h` is the set such that `a ∈ disjUnion s t h` iff `a ∈ s` or `a ∈ t`. It i… | 3 | `{α : Type u_2} (s t : Finset α) (h : Disjoint s t) : Finset α` | None | Thin | Thin | 4 | 0 | 26.83 (q=2, b=2, deg=4, dep=0) | |
| 59 | Finset.powerset | Data/Finset/Powerset.lean | When `s` is a finset, `s.powerset` is the finset of all subsets of `s` (seen as finsets). | 1 | `{α : Type u_1} (s : Finset α) : Finset (Finset α)` | None | Thin | Thin | 4 | 0 | 26.83 (q=2, b=2, deg=4, dep=0) | |
| 60 | Finset.sym2 | Data/Finset/Sym.lean | `s.sym2` is the finset of all unordered pairs of elements from `s`. It is the image of `s… | 1 | `{α : Type u_1} (s : Finset α) : Finset (Sym2 α)` | None | Thin | Thin | 4 | 0 | 26.83 (q=2, b=2, deg=4, dep=0) | |
| 61 | PartialEquiv.ofSet | Logic/Equiv/PartialEquiv.lean | The identity partial equivalence on a set `s` | 1 | `{α : Type u_1} (s : Set α) : PartialEquiv α α` | None | Thin | Thin | 4 | 0 | 26.83 (q=2, b=2, deg=4, dep=0) | |
| 62 | Nat.zeckendorf | Data/Nat/Fib/Zeckendorf.lean | The Zeckendorf representation of a natural number. Note: For unfolding, you should use t… | 1 | `: ℕ → List ℕ` | Rich | Thin | None | 0 | 13 | 26.72 (q=3, b=2, deg=0, dep=13) | |
| 63 | PartialEquiv.refl | Logic/Equiv/PartialEquiv.lean | The identity partial equiv | 1 | `(α : Type u_5) : PartialEquiv α α` | None | None | Rich | 13 | 2 | 26.72 (q=2, b=1, deg=13, dep=2) | |
| 64 | Function.update | Logic/Function/Basic.lean | Replacing the value of a function at a given point by a given value. | 4 | `{α : Sort u} {β : α → Sort v} [DecidableEq α] (f : (a : α) → β a) (a' : α) (v : β a') (a : α) : β a` | None | None | Rich | 13 | 2 | 26.72 (q=2, b=1, deg=13, dep=2) | |
| 65 | Finset.filter | Data/Finset/Filter.lean | `Finset.filter p s` is the set of elements of `s` that satisfy `p`. For example, one can… | 2 | `{α : Type u_1} (p : α → Prop) [DecidablePred p] (s : Finset α) : Finset α` | None | Thin | Thin | 3 | 0 | 26.16 (q=2, b=2, deg=3, dep=0) | |
| 66 | Finset.map | Data/Finset/Image.lean | When `f` is an embedding of `α` in `β` and `s` is a finset in `α`, then `s.map f` is the … | 2 | `{α : Type u_1} {β : Type u_2} (f : α ↪ β) (s : Finset α) : Finset β` | None | Thin | Thin | 3 | 0 | 26.16 (q=2, b=2, deg=3, dep=0) | |
| 67 | Function.Embedding.toEquivRange | Logic/Equiv/Fintype.lean | Computably turn an embedding `f : α ↪ β` into an equiv `α ≃ Set.range f`, if `α` is a `Fi… | 1 | `{α : Type u_1} {β : Type u_2} [Fintype α] [DecidableEq β] (f : α ↪ β) : α ≃ ↑(Set.range ⇑f)` | None | Thin | Thin | 3 | 0 | 26.16 (q=2, b=2, deg=3, dep=0) | |
| 68 | Pi.map | Logic/Function/Defs.lean | Sends a dependent function `a : ∀ i, α i` to a dependent function `Pi.map f a : ∀ i, β i`… | 3 | `{ι : Sort u_1} {α : ι → Sort u_2} {β : ι → Sort u_3} (f : (i : ι) → α i → β i) : ((i : ι) → α i) → (i : ι) → β i` | None | None | Rich | 8 | 2 | 25.39 (q=2, b=1, deg=8, dep=2) | |
| 69 | List.toAList | Data/List/AList.lean | Given `l : List (Sigma β)`, create a term of type `AList β` by removing entries with dupl… | 1 | `{α : Type u} [DecidableEq α] {β : α → Type v} (l : List (Sigma β)) : AList β` | None | Thin | Thin | 2 | 0 | 25.30 (q=2, b=2, deg=2, dep=0) | |
| 70 | notMemRangeEquiv | Data/Finset/Range.lean | Equivalence between the set of natural numbers which are `≥ k` and `ℕ`, given by `n → n -… | 1 | `(k : ℕ) : { n // n ∉ Finset.range k } ≃ ℕ` | None | Thin | Thin | 2 | 0 | 25.30 (q=2, b=2, deg=2, dep=0) | |
| 71 | Nat.findGreatest | Data/Nat/Find.lean | `Nat.findGreatest P n` is the largest `i ≤ n` such that `P i` holds, or `0` if no such `i… | 2 | `(P : ℕ → Prop) [DecidablePred P] : ℕ → ℕ` | None | None | Rich | 11 | 4 | 25.24 (q=2, b=1, deg=11, dep=4) | |
| 72 | Nat.Primes | Data/Nat/Prime/Defs.lean | The type of prime numbers | 0 | `: Type` | None | None | Rich | 5 | 2 | 24.18 (q=2, b=1, deg=5, dep=2) | |
| 73 | Finset.erase | Data/Finset/Erase.lean | `erase s a` is the set `s - {a}`, that is, the elements of `s` which are not equal to `… | 2 | `{α : Type u_1} [DecidableEq α] (s : Finset α) (a : α) : Finset α` | None | Thin | Thin | 1 | 0 | 24.08 (q=2, b=2, deg=1, dep=0) | |
| 74 | Finset.filterMap | Data/Finset/Image.lean | — (no docstring) | 3 | `{α : Type u_1} {β : Type u_2} (f : α → Option β) (s : Finset α) (f_inj : ∀ (a a' : α), ∀ b ∈ f a, b ∈ f a' → a = a') : Finset β` | None | Thin | Thin | 1 | 0 | 24.08 (q=2, b=2, deg=1, dep=0) | |
| 75 | Finset.cons | Data/Finset/Insert.lean | `cons a s h` is the set `{a} ∪ s` containing `a` and the elements of `s`. It is the same … | 3 | `{α : Type u_1} (a : α) (s : Finset α) (h : a ∉ s) : Finset α` | None | Thin | Thin | 1 | 0 | 24.08 (q=2, b=2, deg=1, dep=0) | |
| 76 | Finset.product | Data/Finset/Prod.lean | `product s t` is the set of pairs `(a, b)` such that `a ∈ s` and `b ∈ t`. | 2 | `{α : Type u_1} {β : Type u_2} (s : Finset α) (t : Finset β) : Finset (α × β)` | None | Thin | Thin | 1 | 0 | 24.08 (q=2, b=2, deg=1, dep=0) | |
| 77 | Finset.disjiUnion | Data/Finset/Union.lean | `disjiUnion s f h` is the set such that `a ∈ disjiUnion s f` iff `a ∈ f i` for some `i ∈ … | 3 | `{α : Type u_1} {β : Type u_2} (s : Finset α) (t : α → Finset β) (hf : (↑s).PairwiseDisjoint t) : Finset β` | None | Thin | Thin | 1 | 0 | 24.08 (q=2, b=2, deg=1, dep=0) | |
| 78 | List.rdrop | Data/List/DropRight.lean | Drop `n` elements from the tail end of a list. | 2 | `{α : Type u_1} (l : List α) (n : ℕ) : List α` | None | Thin | Thin | 3 | 2 | 23.96 (q=2, b=2, deg=3, dep=2) | |
| 79 | Finset.Nonempty | Data/Finset/Empty.lean | The property `s.Nonempty` expresses the fact that the finset `s` is not empty. It should … | 1 | `{α : Type u_1} (s : Finset α) : Prop` | None | Thin | Thin | 2 | 1 | 23.91 (q=2, b=2, deg=2, dep=1) | |
| 80 | Function.Semiconj | Logic/Function/Conjugate.lean | We say that `f : α → β` semiconjugates `ga : α → α` to `gb : β → β` if `f ∘ ga = gb ∘ f`.… | 3 | `{α : Type u_1} {β : Type u_2} (f : α → β) (ga : α → α) (gb : β → β) : Prop` | None | Thin | Thin | 2 | 1 | 23.91 (q=2, b=2, deg=2, dep=1) | |
| 81 | Function.Commute | Logic/Function/Conjugate.lean | Two maps `f g : α → α` commute if `f (g x) = g (f x)` for all `x : α`. Given `h : Functio… | 2 | `{α : Type u_1} (f g : α → α) : Prop` | None | Thin | Thin | 2 | 1 | 23.91 (q=2, b=2, deg=2, dep=1) | |
| 82 | Finset.sym | Data/Finset/Sym.lean | Lifts a finset to `Sym α n`. `s.sym n` is the finset of all unordered tuples of cardinali… | 2 | `{α : Type u_1} [DecidableEq α] (s : Finset α) (n : ℕ) : Finset (Sym α n)` | None | Thin | Thin | 4 | 4 | 23.61 (q=2, b=2, deg=4, dep=4) | |
| 83 | List.SortedLE | Data/List/Sort.lean | `l.SortedLE` means that the list is monotonic. | 1 | `{α : Type u_1} [Preorder α] (l : List α) : Prop` | None | Thin | Thin | 3 | 3 | 23.39 (q=2, b=2, deg=3, dep=3) | |
| 84 | List.SortedLT | Data/List/Sort.lean | `l.SortedLT` means that the list is strictly monotonic. | 1 | `{α : Type u_1} [Preorder α] (l : List α) : Prop` | None | Thin | Thin | 3 | 3 | 23.39 (q=2, b=2, deg=3, dep=3) | |
| 85 | Equiv.Finset.union | Data/Finset/Basic.lean | The disjoint union of finsets is a sum | 3 | `{α : Type u_1} [DecidableEq α] (s t : Finset α) (h : Disjoint s t) : ↥s ⊕ ↥t ≃ ↥(s ∪ t)` | None | Thin | Thin | 4 | 5 | 23.24 (q=2, b=2, deg=4, dep=5) | |
| 86 | Equiv.Finset.disjUnionEquiv | Data/Finset/Basic.lean | The disjoint union of finsets is a sum | 3 | `{α : Type u_1} [DecidableEq α] (s t : Finset α) (h : Disjoint s t) : ↥s ⊕ ↥t ≃ ↥(s.disjUnion t h)` | None | Thin | Thin | 4 | 5 | 23.24 (q=2, b=2, deg=4, dep=5) | |
| 87 | Multiset.multinomial | Data/Nat/Choose/Multinomial.lean | The `multinomial` coefficients on `Multiset ℕ`. | 1 | `(m : Multiset ℕ) : ℕ` | None | Thin | Thin | 2 | 2 | 23.10 (q=2, b=2, deg=2, dep=2) | |
| 88 | Finset.subtype | Data/Finset/Image.lean | Given a finset `s` and a predicate `p`, `s.subtype p` is the finset of `Subtype p` whose … | 2 | `{α : Type u_4} (p : α → Prop) [DecidablePred p] (s : Finset α) : Finset (Subtype p)` | None | Thin | Thin | 2 | 2 | 23.10 (q=2, b=2, deg=2, dep=2) | |
| 89 | Relator.BiUnique | Logic/Relator.lean | A relation is "bi-unique" if it is both left unique and right unique. | 1 | `{α : Sort u₁} {β : Sort u₂} (R : α → β → Prop) : Prop` | None | Thin | Thin | 2 | 2 | 23.10 (q=2, b=2, deg=2, dep=2) | |
| 90 | finAddFlip | Logic/Equiv/Fin/Basic.lean | The equivalence between `Fin (m + n)` and `Fin (n + m)` which rotates by `n`. | 0 | `{m n : ℕ} : Fin (m + n) ≃ Fin (n + m)` | None | None | Rich | 5 | 5 | 22.79 (q=2, b=1, deg=5, dep=5) | |
| 91 | Finset.restrict | Data/Finset/Pi.lean | Restrict domain of a function `f` to a finite set `s`. | 3 | `{ι : Type u_2} {π : ι → Type u_3} (s : Finset ι) (f : (i : ι) → π i) (i : ↥s) : π ↑i` | None | Thin | Thin | 1 | 1 | 22.69 (q=2, b=2, deg=1, dep=1) | |
| 92 | Finset.max | Data/Finset/Max.lean | Let `s` be a finset in a linear order. Then `s.max` is the maximum of `s` if `s` is not e… | 1 | `{α : Type u_2} [LinearOrder α] (s : Finset α) : WithBot α` | None | Thin | Thin | 2 | 3 | 22.52 (q=2, b=2, deg=2, dep=3) | |
| 93 | Finset.min | Data/Finset/Max.lean | Let `s` be a finset in a linear order. Then `s.min` is the minimum of `s` if `s` is not e… | 1 | `{α : Type u_2} [LinearOrder α] (s : Finset α) : WithTop α` | None | Thin | Thin | 2 | 3 | 22.52 (q=2, b=2, deg=2, dep=3) | |
| 94 | Set.Sized | Data/Finset/Slice.lean | `Sized r A` means that every Finset in `A` has size `r`. | 2 | `{α : Type u_1} (r : ℕ) (A : Set (Finset α)) : Prop` | None | Thin | Thin | 2 | 3 | 22.52 (q=2, b=2, deg=2, dep=3) | |
| 95 | Relator.RightUnique | Logic/Relator.lean | A relation is "right unique" if every element on the left is paired with at most one elem… | 1 | `{α : Sort u₁} {β : Sort u₂} (R : α → β → Prop) : Prop` | None | Thin | Thin | 2 | 3 | 22.52 (q=2, b=2, deg=2, dep=3) | |
| 96 | Finset.mapEmbedding | Data/Finset/Image.lean | Associate to an embedding `f` from `α` to `β` the order embedding that maps a finset to i… | 1 | `{α : Type u_1} {β : Type u_2} (f : α ↪ β) : Finset α ↪o Finset β` | None | Thin | Thin | 1 | 2 | 21.88 (q=2, b=2, deg=1, dep=2) | |
| 97 | Option.toFinset | Data/Finset/Option.lean | Construct an empty or singleton finset from an `Option` | 1 | `{α : Type u_1} (o : Option α) : Finset α` | None | Thin | Thin | 1 | 2 | 21.88 (q=2, b=2, deg=1, dep=2) | |
| 98 | Relator.BiTotal | Logic/Relator.lean | A relation is "bi-total" if it is both right total and left total. | 1 | `{α : Sort u₁} {β : Sort u₂} (R : α → β → Prop) : Prop` | None | Thin | Thin | 1 | 2 | 21.88 (q=2, b=2, deg=1, dep=2) | |
| 99 | Finset.biUnion | Data/Finset/Union.lean | `Finset.biUnion s t` is the union of `t a` over `a ∈ s`. (This was formerly `bind` due t… | 2 | `{α : Type u_1} {β : Type u_2} [DecidableEq β] (s : Finset α) (t : α → Finset β) : Finset β` | None | Thin | Thin | 2 | 5 | 21.71 (q=2, b=2, deg=2, dep=5) | |
| 100 | List.Forall | Data/List/Defs.lean | `l.Forall p` is equivalent to `∀ a ∈ l, p a`, but unfolds directly to a conjunction, i.e.… | 2 | `{α : Type u_1} (p : α → Prop) : List α → Prop` | None | Thin | Thin | 1 | 3 | 21.31 (q=2, b=2, deg=1, dep=3) | |

## 3. Detail cards: top 25

### 1. Nat.Prime
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

**Raw supply numbers:** mention_count=450, theorem_mention_count=21, enumerable_arg_count=1, is_predicate_shaped=True, classifies_structure=False, executable=True, exec_mechanism=decide, output_decidable_eq=None, dependency_raw=1
**Axiom set:** propext
**Score:** 70.89 (quality=6, breadth=3, in_degree=21, dependency=1)
**Notes:** **The headline case for this round's item-3 fix.** `casework_tier` and `membership_tier` are now both Rich — revision 1 recorded `none`/`thin` here purely because of the literal, meaningless `DecidableEq Prop` check, not because anything about `Nat.Prime` itself changed. New rank 1 (was rank 5), the single largest score jump in the batch (39.89 → 70.89). Still a thin rename underneath (`Prime p := Irreducible p`) — all mathematical content lives in `Irreducible`, defined elsewhere and not itself in this batch.

### 2. Finset.range
*Data/Finset/Range.lean*

**Docstring:**
> `range n` is the set of natural numbers less than `n`.

**Source:**
```lean
def range (n : ℕ) : Finset ℕ :=
  ⟨_, nodup_range n⟩
```

**Raw supply numbers:** mention_count=852, theorem_mention_count=27, enumerable_arg_count=1, is_predicate_shaped=False, classifies_structure=True, executable=True, exec_mechanism=eval, output_decidable_eq=True, dependency_raw=0
**Axiom set:** Classical.choice, Quot.sound, propext
**Score:** 63.00 (quality=5, breadth=3, in_degree=27, dependency=0)
**Notes:** Untouched by any of this round's fixes — identical score to revision 1. Dropped one rank purely because `Nat.Prime` (above) now correctly outscores it, not because anything about this row changed.

### 3. Int.bodd
*Data/Int/Bitwise.lean*

**Docstring:**
> `bodd n` returns `true` if `n` is odd

**Source:**
```lean
def bodd : ℤ → Bool
  | (n : ℕ) => n.bodd
  | -[n+1] => not (n.bodd)
```

**Raw supply numbers:** mention_count=0, theorem_mention_count=1, enumerable_arg_count=1, is_predicate_shaped=True, classifies_structure=False, executable=True, exec_mechanism=eval, output_decidable_eq=True, dependency_raw=5
**Axiom set:** propext
**Score:** 51.50 (quality=5, breadth=3, in_degree=1, dependency=5)
**Notes:** Did not appear anywhere in revision 1's ranked table. Beneficiary of item 2's arity fix: `def bodd : ℤ → Bool` is a header-less pattern match, so the old source-header parser recorded 0 explicit arguments and it never reached casework/membership tiers at all. The type-derived arity now correctly finds its one `ℤ` argument via the trailing-anonymous-arrow-chain fix, making it casework- and (since `Bool` is predicate-shaped and it's genuinely executable) membership-rich.

### 4. finRotate
*Logic/Equiv/Fin/Rotate.lean*

**Docstring:**
> Rotate `Fin n` one step to the right.

**Source:**
```lean
def finRotate : ∀ n, Equiv.Perm (Fin n)
  | 0 => Equiv.refl _
  | n + 1 => finAddFlip.trans (finCongr (Nat.add_comm 1 n))
```

**Raw supply numbers:** mention_count=31, theorem_mention_count=18, enumerable_arg_count=1, is_predicate_shaped=False, classifies_structure=False, executable=True, exec_mechanism=eval, output_decidable_eq=True, dependency_raw=6
**Axiom set:** Quot.sound, propext
**Score:** 46.94 (quality=4, breadth=2, in_degree=18, dependency=6)
**Notes:** Untouched by any of this round's fixes — identical score and tiers to revision 1. The `n + 1` case delegates to `finAddFlip.trans (finCongr ...)` (both defined elsewhere) — the real combinatorial content of the rotation lives there, not here.

### 5. Nat.log
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

**Raw supply numbers:** mention_count=56, theorem_mention_count=6, enumerable_arg_count=2, is_predicate_shaped=False, classifies_structure=False, executable=True, exec_mechanism=eval, output_decidable_eq=True, dependency_raw=1
**Axiom set:** (none)
**Score:** 46.45 (quality=4, breadth=2, in_degree=6, dependency=1)
**Notes:** Untouched by any of this round's fixes. Has a `where`-clause auxiliary `go` with fuel-based structural recursion — genuine recursion/well-foundedness machinery, not a one-liner. Worth a reviewer's eye on whether facts should target `log` itself or need to reach into `go`.

### 6. Nat.choose
*Data/Nat/Choose/Basic.lean*

**Docstring:**
> `choose n k` is the number of `k`-element subsets in an `n`-element set. Also known as binomial
> coefficients. For the fact that this is the number of `k`-element-subsets of an `n`-element
> set, see `Finset.card_powersetCard`.

**Source:**
```lean
def choose : ℕ → ℕ → ℕ
  | _, 0 => 1
  | 0, _ + 1 => 0
  | n + 1, k + 1 => choose n k + choose n (k + 1)
```

**Raw supply numbers:** mention_count=188, theorem_mention_count=10, enumerable_arg_count=2, is_predicate_shaped=False, classifies_structure=False, executable=True, exec_mechanism=eval, output_decidable_eq=True, dependency_raw=3
**Axiom set:** (none)
**Score:** 46.42 (quality=4, breadth=2, in_degree=10, dependency=3)
**Notes:** Only appeared in revision 1's edge-list (c) at rank 44, lopsided on Global alone (`: ℕ → ℕ → ℕ`, 0 recorded arguments). Same header-less pattern-match shape as `Int.bodd` above — the arity fix now finds both `ℕ` arguments, making it casework-rich and lifting it from rank 44 to rank 6.

### 7. hyperoperation
*Data/Nat/Hyperoperation.lean*

**Docstring:**
> Implementation of the hyperoperation sequence
> where `hyperoperation n m k` is the `n`th hyperoperation between `m` and `k`.

**Source:**
```lean
def hyperoperation : ℕ → ℕ → ℕ → ℕ
  | 0, _, k => k + 1
  | 1, m, 0 => m
  | 2, _, 0 => 0
  | _ + 3, _, 0 => 1
  | n + 1, m, k + 1 => hyperoperation n m (hyperoperation (n + 1) m k)
```

**Raw supply numbers:** mention_count=0, theorem_mention_count=10, enumerable_arg_count=3, is_predicate_shaped=False, classifies_structure=False, executable=True, exec_mechanism=eval, output_decidable_eq=True, dependency_raw=4
**Axiom set:** Quot.sound, propext
**Score:** 45.97 (quality=4, breadth=2, in_degree=10, dependency=4)
**Notes:** Same story as `Nat.choose` above — header-less pattern match, all three `ℕ` arguments were invisible to the old arity parser. Rank 50 (edge-list (c), lopsided-Global) in revision 1 → rank 7.

### 8. Pairwise
*Logic/Pairwise.lean*

**Docstring:**
> A relation `r` holds pairwise if `r i j` for all `i ≠ j`.

**Source:**
```lean
def Pairwise (r : α → α → Prop) :=
  ∀ ⦃i j⦄, i ≠ j → r i j
```

**Raw supply numbers:** mention_count=1451, theorem_mention_count=119, enumerable_arg_count=0, is_predicate_shaped=True, classifies_structure=False, executable=None, exec_mechanism=none, output_decidable_eq=None, dependency_raw=2
**Axiom set:** (none)
**Score:** 44.17 (quality=3, breadth=2, in_degree=119, dependency=2)
**Notes:** **One of this task's three named arity-fix acceptance cases** (with `Function.Bijective` and `List.orderedInsert`, §0). Recorded arity is now correctly **1** (`r : α → α → Prop`), not 0 as in revision 1 — the universe-annotation parsing bug (`Pairwise.{u_1}`) previously discarded this binder group entirely. `casework_tier` stays `none` regardless: `α → α → Prop` isn't one of the cheap enumerable types this stage can construct canonical inputs for. `membership_tier` stays `thin`: predicate-shaped, but Lean can't synthesize a `Decidable` instance for an abstract `r`, so it isn't concretely checkable. Dropped four ranks purely because previously arity-starved definitions above it (`Nat.choose`, `hyperoperation`, `Nat.digits`, `Int.bodd`) now correctly outscore it. Same near-duplicate relationship with `Set.Pairwise` (rank 16) noted in `miner/curation.yaml`.

### 9. Nat.digits
*Data/Nat/Digits/Defs.lean*

**Docstring:**
> `digits b n` gives the digits, in little-endian order,
> of a natural number `n` in a specified base `b`.
>
> In any base, we have `ofDigits b L = L.foldr (fun x y ↦ x + b * y) 0`.
> * For any `2 ≤ b`, we have `l < b` for any `l ∈ digits b n`,
>   and the last digit is not zero.
>   This uniquely specifies the behaviour of `digits b`.
> * For `b = 1`, we define `digits 1 n = List.replicate n 1`.
> * For `b = 0`, we define `digits 0 n = [n]`, except `digits 0 0 = []`.
>
> Note this differs from the existing `Nat.toDigits` in core, which is used for printing numerals.
> In particular, `Nat.toDigits b 0 = ['0']`, while `digits b 0 = []`.

**Source:**
```lean
def digits : ℕ → ℕ → List ℕ
  | 0 => digitsAux0
  | 1 => digitsAux1
  | b + 2 => digitsAux (b + 2) (by simp)
```

**Raw supply numbers:** mention_count=14, theorem_mention_count=2, enumerable_arg_count=2, is_predicate_shaped=False, classifies_structure=True, executable=True, exec_mechanism=eval, output_decidable_eq=True, dependency_raw=7
**Axiom set:** Classical.choice, Quot.sound, propext
**Score:** 42.14 (quality=4, breadth=3, in_degree=2, dependency=7)
**Notes:** **The single biggest mover in this batch**: rank 83 (revision 1) → rank 9. Same header-less pattern-match arity gap as `Nat.choose`/`hyperoperation` — recording 0 arguments capped casework at `none`; both `ℕ` arguments are now correctly found, roughly doubling its score (21.14 → 42.14). Delegates to `digitsAux0`/`digitsAux1`/`digitsAux` (all defined elsewhere; `digitsAux1` is this batch's curation-`exclude` case, see §0 item 4 and card 22 in revision 1).

### 10. Nat.ModEq
*Data/Nat/ModEq.lean*

**Docstring:**
> Modular equality. `n.ModEq a b`, or `a ≡ b [MOD n]`, means that `a % n = b % n`.

**Source:**
```lean
def Nat.ModEq (n a b : ℕ) :=
  a % n = b % n
```

**Raw supply numbers:** mention_count=48, theorem_mention_count=0, enumerable_arg_count=3, is_predicate_shaped=True, classifies_structure=False, executable=True, exec_mechanism=decide, output_decidable_eq=None, dependency_raw=0
**Axiom set:** (none)
**Score:** 42.00 (quality=4, breadth=2, in_degree=0, dependency=0)
**Notes:** Did not appear in revision 1's top 100 at all — a pure item-3 (Prop-semantics) beneficiary, not an arity case: its header (`n a b : ℕ`) was always parsed correctly. Under the old literal `DecidableEq Prop` check this decidable equality-mod-`n` predicate scored `none`/`none`; now correctly `decide`-mechanism and casework-/membership-rich.

### 11. Int.ModEq
*Data/Int/ModEq.lean*

**Docstring:**
> `a ≡ b [ZMOD n]` when `a % n = b % n`.

**Source:**
```lean
def Int.ModEq (n a b : ℤ) :=
  a % n = b % n
```

**Raw supply numbers:** mention_count=32, theorem_mention_count=0, enumerable_arg_count=3, is_predicate_shaped=True, classifies_structure=False, executable=True, exec_mechanism=decide, output_decidable_eq=None, dependency_raw=0
**Axiom set:** (none)
**Score:** 42.00 (quality=4, breadth=2, in_degree=0, dependency=0)
**Notes:** `ℤ`-valued sibling of rank 10's `Nat.ModEq`, same story: a genuine `decide`-mechanism predicate the old `DecidableEq Prop` bug always scored `none`/`none`. Both entering the ranked table for the first time together is expected, not a coincidence.

### 12. Nat.bits
*Data/Nat/Bits.lean*

**Docstring:**
> `bits n` returns a list of Bools which correspond to the binary representation of n, where
> the head of the list represents the least significant bit

**Source:**
```lean
def bits : ℕ → List Bool :=
  binaryRec [] fun b _ IH => b :: IH
```

**Raw supply numbers:** mention_count=1, theorem_mention_count=1, enumerable_arg_count=1, is_predicate_shaped=False, classifies_structure=True, executable=True, exec_mechanism=eval, output_decidable_eq=True, dependency_raw=5
**Axiom set:** Quot.sound, propext
**Score:** 41.50 (quality=4, breadth=3, in_degree=1, dependency=5)
**Notes:** Same header-less arity-fix pattern as `Int.bodd`/`Nat.choose` above: `def bits : ℕ → List Bool` has no named binder at all. Rank 92 (revision 1, `none/thin/thin`) → rank 12 (`rich/thin/thin`).

### 13. Xor
*Logic/Basic.lean*

**Docstring:**
> `Xor a b` is the exclusive-or of propositions.

**Source:**
```lean
def Xor (a b : Prop) := (a ∧ ¬b) ∨ (b ∧ ¬a)
```

**Raw supply numbers:** mention_count=56, theorem_mention_count=8, enumerable_arg_count=0, is_predicate_shaped=True, classifies_structure=False, executable=None, exec_mechanism=none, output_decidable_eq=None, dependency_raw=0
**Axiom set:** (none)
**Score:** 38.59 (quality=3, breadth=2, in_degree=8, dependency=0)
**Notes:** Untouched by any of this round's fixes — identical score to revision 1. Self-contained propositional formula (`(a ∧ ¬b) ∨ (b ∧ ¬a)`), not a delegation. Not `decide`-mechanism (its two arguments are themselves abstract `Prop`s, not concrete data), so item 3's fix doesn't apply here despite the `Prop` return type.

### 14. Multiset.toFinset
*Data/Finset/Dedup.lean*

**Docstring:**
> `toFinset s` removes duplicates from the multiset `s` to produce a finset.

**Source:**
```lean
def toFinset (s : Multiset α) : Finset α :=
  ⟨_, nodup_dedup s⟩
```

**Raw supply numbers:** mention_count=85, theorem_mention_count=6, enumerable_arg_count=0, is_predicate_shaped=False, classifies_structure=True, executable=None, exec_mechanism=none, output_decidable_eq=False, dependency_raw=0
**Axiom set:** Classical.choice, Quot.sound, propext
**Score:** 37.84 (quality=3, breadth=2, in_degree=6, dependency=0)
**Notes:** Untouched by any of this round's fixes — identical score to revision 1. Foundational constructor (subtype-wraps `nodup_dedup s`), not a concerning delegation.

### 15. Function.Bijective
*Logic/Function/Defs.lean*

**Docstring:**
> A function is called bijective if it is both injective and surjective.

**Source:**
```lean
def Bijective (f : α → β) :=
  Injective f ∧ Surjective f
```

**Raw supply numbers:** mention_count=656, theorem_mention_count=13, enumerable_arg_count=0, is_predicate_shaped=True, classifies_structure=False, executable=None, exec_mechanism=none, output_decidable_eq=None, dependency_raw=2
**Axiom set:** (none)
**Score:** 37.72 (quality=3, breadth=2, in_degree=13, dependency=2)
**Notes:** **One of this task's three named arity-fix acceptance cases** (§0). Arity now correctly 1 (`f : α → β`), not 0. Tiers otherwise unaffected by item 3's fix: `Injective f ∧ Surjective f` isn't itself `decide`-checkable (a conjunction of two definitions elaborated elsewhere), so it doesn't get the `Nat.Prime`-style boost. Still a thin wrapper: all real content lives in `Injective`/`Surjective`, neither in this batch.

### 16. Set.Pairwise
*Logic/Pairwise.lean*

**Docstring:**
> The relation `r` holds pairwise on the set `s` if `r x y` for all *distinct* `x y ∈ s`.

**Source:**
```lean
protected def Pairwise (s : Set α) (r : α → α → Prop) :=
  ∀ ⦃x⦄, x ∈ s → ∀ ⦃y⦄, y ∈ s → x ≠ y → r x y
```

**Raw supply numbers:** mention_count=180, theorem_mention_count=11, enumerable_arg_count=0, is_predicate_shaped=True, classifies_structure=True, executable=None, exec_mechanism=none, output_decidable_eq=None, dependency_raw=2
**Axiom set:** (none)
**Score:** 37.26 (quality=3, breadth=2, in_degree=11, dependency=2)
**Notes:** Same fix as `Pairwise` (rank 8): arity now correctly 2 (`s`, `r`); tiers unaffected (not concretely decidable for an abstract `r`). Same curation note as revision 1 — near-duplicate of `Pairwise`, see `miner/curation.yaml`.

### 17. Finset.card
*Data/Finset/Card.lean*

**Docstring:**
> `s.card` is the number of elements of `s`, aka its cardinality.
>
> The notation `#s` can be accessed in the `Finset` locale.

**Source:**
```lean
def card (s : Finset α) : ℕ :=
  Multiset.card s.1
```

**Raw supply numbers:** mention_count=719, theorem_mention_count=7, enumerable_arg_count=0, is_predicate_shaped=False, classifies_structure=True, executable=None, exec_mechanism=none, output_decidable_eq=True, dependency_raw=1
**Axiom set:** Quot.sound, propext
**Score:** 36.85 (quality=3, breadth=2, in_degree=7, dependency=1)
**Notes:** Arity now correctly 1 (`s : Finset α`) — was recorded 0 in revision 1, despite `Finset.card`'s own header writing `(s : Finset α)` out explicitly. This is the universe-annotation bug specifically (its implicit `{α : Type u_1}` triggered the `.{u_1}`-prefixed `#check` output that discarded every binder group, named ones included) — not the header-less pattern-match gap that affects `Nat.choose`/`hyperoperation`/etc. above. Rank 48 (edge-list (c), lopsided-Global) in revision 1 → rank 17. Thin delegation to `Multiset.card s.1`.

### 18. ExistsUnique
*Logic/ExistsUnique.lean*

**Docstring:**
> For `p : α → Prop`, `ExistsUnique p` means that there exists a unique `x : α` with `p x`.

**Source:**
```lean
def ExistsUnique (p : α → Prop) := ∃ x, p x ∧ ∀ y, p y → y = x
```

**Raw supply numbers:** mention_count=38, theorem_mention_count=9, enumerable_arg_count=0, is_predicate_shaped=True, classifies_structure=False, executable=None, exec_mechanism=none, output_decidable_eq=None, dependency_raw=2
**Axiom set:** (none)
**Score:** 36.71 (quality=3, breadth=2, in_degree=9, dependency=2)
**Notes:** Arity now correctly 1 (`p : α → Prop`), was 0 (universe-annotation bug). Tiers unaffected — not concretely decidable for an abstract `p`. Self-contained foundational logic primitive otherwise unchanged from revision 1.

### 19. Relation.Map
*Logic/Relation.lean*

**Docstring:**
> The map of a relation `r` through a pair of functions pushes the
> relation to the codomains of the functions. The resulting relation is
> defined by having pairs of terms related if they have preimages
> related by `r`.

**Source:**
```lean
protected def Map (r : α → β → Prop) (f : α → γ) (g : β → δ) : γ → δ → Prop := fun c d ↦
  ∃ a b, r a b ∧ f a = c ∧ g b = d
```

**Raw supply numbers:** mention_count=25, theorem_mention_count=13, enumerable_arg_count=0, is_predicate_shaped=True, classifies_structure=False, executable=None, exec_mechanism=none, output_decidable_eq=None, dependency_raw=4
**Axiom set:** (none)
**Score:** 36.70 (quality=3, breadth=2, in_degree=13, dependency=4)
**Notes:** Rank 52 (revision 1, arity recorded 0) → rank 19. Arity now correctly **5**: the named `r`, `f`, `g` plus the two arguments its curried `γ → δ → Prop` result itself takes (`c`, `d` in the body) — a genuine type-theoretic arity of 5, correctly reconstructed by the trailing-arrow-chain fix rather than stopping at the three named binders.

### 20. DependsOn
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

**Raw supply numbers:** mention_count=24, theorem_mention_count=10, enumerable_arg_count=0, is_predicate_shaped=True, classifies_structure=True, executable=None, exec_mechanism=none, output_decidable_eq=None, dependency_raw=3
**Axiom set:** (none)
**Score:** 36.42 (quality=3, breadth=2, in_degree=10, dependency=3)
**Notes:** Arity now correctly 2 (`f`, `s`), was 0. Tiers unaffected — self-contained, has genuine content of its own, not a delegation.

### 21. Finset.image
*Data/Finset/Image.lean*

**Docstring:**
> `image f s` is the forward image of `s` under `f`.

**Source:**
```lean
def image (f : α → β) (s : Finset α) : Finset β :=
  (s.1.map f).toFinset
```

**Raw supply numbers:** mention_count=158, theorem_mention_count=9, enumerable_arg_count=0, is_predicate_shaped=False, classifies_structure=True, executable=None, exec_mechanism=none, output_decidable_eq=False, dependency_raw=4
**Axiom set:** Classical.choice, Quot.sound, propext
**Score:** 35.69 (quality=3, breadth=2, in_degree=9, dependency=4)
**Notes:** Arity now correctly 2 (`f`, `s`), was 0. **This is the genuine, correctly-scanned `Finset.image` (unary)** — never confused with `Finset.image₂` (binary), which now correctly appears under its own name at rank 102 (§0 item 1, §4 edge-list (b)). Thin delegation to `(s.1.map f).toFinset`.

### 22. List.toFinset
*Data/Finset/Dedup.lean*

**Docstring:**
> `toFinset l` removes duplicates from the list `l` to produce a finset.

**Source:**
```lean
def toFinset (l : List α) : Finset α :=
  Multiset.toFinset l
```

**Raw supply numbers:** mention_count=32, theorem_mention_count=6, enumerable_arg_count=0, is_predicate_shaped=False, classifies_structure=True, executable=None, exec_mechanism=none, output_decidable_eq=False, dependency_raw=2
**Axiom set:** Classical.choice, Quot.sound, propext
**Score:** 35.64 (quality=3, breadth=2, in_degree=6, dependency=2)
**Notes:** Arity now correctly 1 (`l : List α`), was 0. **Thin wrapper, textbook case, unchanged from revision 1**: the entire body is `Multiset.toFinset l`, a one-line delegation to rank 14's `Multiset.toFinset` in this very batch.

### 23. IsDvdSequence
*Data/Nat/DvdSequence.lean*

**Docstring:**
> A function `f : α → β` is a divisibility sequence if `a ∣ b` implies `f a ∣ f b`.

**Source:**
```lean
def IsDvdSequence [Dvd α] [Dvd β] (f : α → β) : Prop :=
  ∀ a b, a ∣ b → f a ∣ f b
```

**Raw supply numbers:** mention_count=2, theorem_mention_count=7, enumerable_arg_count=0, is_predicate_shaped=True, classifies_structure=False, executable=None, exec_mechanism=none, output_decidable_eq=None, dependency_raw=3
**Axiom set:** (none)
**Score:** 35.47 (quality=3, breadth=2, in_degree=7, dependency=3)
**Notes:** Arity now correctly 1 (`f : α → β`), was 0. Still unresolved standalone ("typeclass instance problem is stuck" on `[Dvd α] [Dvd β]"), same as revision 1 — its casework/executability data should still be read as inconclusive rather than a genuine negative.

### 24. Nat.bit
*Data/Nat/BinaryRec.lean*

**Docstring:**
> `bit b` appends the digit `b` to the little end of the binary representation of
> its natural number input.

**Source:**
```lean
def bit (b : Bool) (n : Nat) : Nat :=
  cond b (2 * n + 1) (2 * n)
```

**Raw supply numbers:** mention_count=53, theorem_mention_count=4, enumerable_arg_count=2, is_predicate_shaped=False, classifies_structure=False, executable=True, exec_mechanism=eval, output_decidable_eq=True, dependency_raw=1
**Axiom set:** (none)
**Score:** 35.44 (quality=3, breadth=2, in_degree=4, dependency=1)
**Notes:** Untouched by any of this round's fixes — identical score to revision 1 (its named header `(b : Bool) (n : Nat)` was always parsed correctly). Self-contained one-liner using `cond`; not a delegation.

### 25. Nat.clog
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

**Raw supply numbers:** mention_count=34, theorem_mention_count=4, enumerable_arg_count=2, is_predicate_shaped=False, classifies_structure=False, executable=True, exec_mechanism=eval, output_decidable_eq=True, dependency_raw=1
**Axiom set:** (none)
**Score:** 35.44 (quality=3, breadth=2, in_degree=4, dependency=1)
**Notes:** Untouched by any of this round's fixes — identical score to revision 1. Same `where`-clause fuel-recursive-auxiliary shape as rank 5's `Nat.log` (its dual, floor vs. ceiling log); same recursion caveat applies.

## 4. Edge lists

### (a) 10 lowest-ranked included -- the marginal cases

| Rank | Name | Module | Tiers (CW/Mem/Glob) | Score |
|---|---|---|---|---|
| 91 | Finset.restrict | Data/Finset/Pi.lean | none/thin/thin | 22.69 |
| 92 | Finset.max | Data/Finset/Max.lean | none/thin/thin | 22.52 |
| 93 | Finset.min | Data/Finset/Max.lean | none/thin/thin | 22.52 |
| 94 | Set.Sized | Data/Finset/Slice.lean | none/thin/thin | 22.52 |
| 95 | Relator.RightUnique | Logic/Relator.lean | none/thin/thin | 22.52 |
| 96 | Finset.mapEmbedding | Data/Finset/Image.lean | none/thin/thin | 21.88 |
| 97 | Option.toFinset | Data/Finset/Option.lean | none/thin/thin | 21.88 |
| 98 | Relator.BiTotal | Logic/Relator.lean | none/thin/thin | 21.88 |
| 99 | Finset.biUnion | Data/Finset/Union.lean | none/thin/thin | 21.71 |
| 100 | List.Forall | Data/List/Defs.lean | none/thin/thin | 21.31 |

### (b) 10 highest-ranked excluded (verified but outranked, non-curated) -- what just missed

Includes `Finset.image₂` at rank 102 — the real, correctly-named binary image function, verified on its own genuine (not borrowed) data for the first time; see §0 item 1.

| Rank | Name | Module | Tiers (CW/Mem/Glob) | Score |
|---|---|---|---|---|
| 101 | List.iterate | Data/List/Defs.lean | none/thin/thin | 21.31 |
| 102 | Finset.image₂ | Data/Finset/NAry.lean | none/thin/thin | 21.31 |
| 103 | Relator.LeftUnique | Logic/Relator.lean | none/thin/thin | 21.31 |
| 104 | Nat.dist | Data/Nat/Dist.lean | rich/none/none | 21.00 |
| 105 | Nat.pair | Data/Nat/Pairing.lean | rich/none/none | 21.00 |
| 106 | Int.succ | Data/Int/Init.lean | rich/none/none | 21.00 |
| 107 | Int.pred | Data/Int/Init.lean | rich/none/none | 21.00 |
| 108 | List.destutter' | Data/List/Defs.lean | none/thin/thin | 20.86 |
| 109 | List.orderedInsert | Data/List/Sort.lean | none/thin/thin | 20.86 |
| 110 | List.destutter | Data/List/Defs.lean | none/thin/thin | 20.50 |

Note `List.orderedInsert` (rank 109) — the third of this task's three named arity-fix acceptance cases (§0 item 2). Its arity is now correctly 3 (`r`, `a`, `l`), confirmed via `tests/test_miner_verify_parsing.py`; it remains casework-`none` (its `r : α → α → Prop` argument still isn't an enumerable type) and so stays outranked, which is the expected, correct outcome — the fix corrects the *data*, not necessarily the *rank*.

### (c) Lopsided-extreme included definitions -- rich in exactly one tier, none in both others

Per the design discussion, breadth is only a soft/tie-breaking preference, so a lopsided-but-excellent candidate is allowed to outrank a well-rounded-but-mediocre one. These are the ones that made it through on the strength of a single tier alone.

13 of the 100 included definitions qualify (down from 27 in revision 1 — expected, since fixes 2 and 3 moved several former lopsided-Global entries, e.g. `Nat.choose` and `hyperoperation`, into multi-tier territory once their true casework arity was recovered).

| Rank | Name | Module | Rich tier | Score |
|---|---|---|---|---|
| 39 | Cycle | Data/List/Cycle.lean | Global | 30.02 |
| 40 | finSuccEquiv | Logic/Equiv/Fin/Basic.lean | Global | 29.50 |
| 41 | finSuccEquiv' | Logic/Equiv/Fin/Basic.lean | Global | 29.50 |
| 46 | Equiv.swap | Logic/Equiv/Basic.lean | Global | 28.92 |
| 52 | Nat.find | Data/Nat/Find.lean | Global | 28.58 |
| 54 | Equiv.symm | Logic/Equiv/Defs.lean | Global | 28.19 |
| 57 | finSumFinEquiv | Logic/Equiv/Fin/Basic.lean | Global | 26.84 |
| 63 | PartialEquiv.refl | Logic/Equiv/PartialEquiv.lean | Global | 26.72 |
| 64 | Function.update | Logic/Function/Basic.lean | Global | 26.72 |
| 68 | Pi.map | Logic/Function/Defs.lean | Global | 25.39 |
| 71 | Nat.findGreatest | Data/Nat/Find.lean | Global | 25.24 |
| 72 | Nat.Primes | Data/Nat/Prime/Defs.lean | Global | 24.18 |
| 90 | finAddFlip | Logic/Equiv/Fin/Basic.lean | Global | 22.79 |
