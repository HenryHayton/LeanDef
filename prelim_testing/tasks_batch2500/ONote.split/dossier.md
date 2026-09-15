## VTask.split

### Object

`VTask.split` decomposes an ordinal notation `o` into a pair `(a, n)` where `a` is the "ω-divisible part" of `o` and `n` is the natural-number remainder. Concretely, it performs division with remainder modulo ω: the ordinal denoted by `o` equals the ordinal denoted by `a` plus the natural number `n`, and the ordinal denoted by `a` is divisible by ω (i.e., ω divides `repr a`). Think of it as stripping off the finite "tail" of an ordinal in Cantor normal form.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.split : ONote → ONote × ℕ
<!-- PINNED-SIGNATURE:END -->


```
VTask.split : ONote → ONote × ℕ
```

The single argument is an ordinal notation (a term of type `ONote`) representing an ordinal in Cantor normal form. The output is a pair whose first component is another ordinal notation representing the largest ω-multiple that does not exceed the input, and whose second component is a natural number giving the finite remainder.

### Conventions

For the zero notation, both components of the output are trivially zero: `VTask.split 0 = (0, 0)`. When the input is an `oadd` term whose leading exponent is zero (i.e., the term is of the form `oadd 0 n a`, representing a pure natural number coefficient), the ω-divisible part is 0 and the remainder is that coefficient `n`, discarding the sub-term `a` (which is 0 in any well-formed such notation). For an `oadd` term with nonzero leading exponent, the split recurses into the tail and keeps the leading monomial in the ω-divisible part.

### Worked examples

- Claim: `VTask.split 0 = (0, 0)` — the zero ordinal splits trivially.
  ```lean
  example : VTask.split 0 = (0, 0) := by decide
  ```

- Claim: For `e = 0`, the notation `oadd 0 3 0` (representing the natural number 3) splits as `(0, 3)`, since 3 = 0·ω + 3.
  ```lean
  example : VTask.split (ONote.oadd 0 3 0) = (0, 3) := by decide
  ```

- Claim: For a term like `oadd 1 2 0` (representing ω·2), which has nonzero leading exponent, the split yields `(oadd 1 2 0, 0)` because ω·2 is already divisible by ω with zero remainder.
  ```lean
  example : VTask.split (ONote.oadd 1 2 0) = (ONote.oadd 1 2 0, 0) := by decide
  ```

- Claim: For `oadd 1 1 (oadd 0 5 0)` (representing ω + 5), the split yields `(oadd 1 1 0, 5)`, peeling off the finite tail 5.
  ```lean
  example : VTask.split (ONote.oadd 1 1 (ONote.oadd 0 5 0)) = (ONote.oadd 1 1 0, 5) := by decide
  ```

### Boundaries

- Input `0`: returns `(0, 0)`. Both components are zero, which is correct since 0 = 0 + 0 and ω ∣ 0.
- Pure finite natural numbers (`oadd 0 n 0` in normal form): the ω-divisible part is 0, and the remainder equals the coefficient `n`. Any sub-term of an `oadd 0 n a` node is ignored in the output.
- Notations that are already divisible by ω (no constant term in Cantor normal form): remainder is 0 and the first component equals the input.
- The natural-number remainder `n` in the output pair is always strictly less than ω, so it faithfully represents the residue class modulo ω.
- For well-formed (normal-form, `NF`) inputs the output pair satisfies `repr o = repr a + n` and `ω ∣ repr a`; these properties are stated as separate theorems and do not hold trivially for ill-formed inputs.

### Not to be confused with

- `ONote.split'`: a closely related helper that instead writes `o = ω * a' + n`, producing a quotient `a'` such that `repr o = ω * repr a' + n` rather than a sum `repr a + n`; related to `VTask.split` by a `scale 1` transformation.
- `ONote.repr`: the function interpreting an `ONote` as an actual ordinal; `VTask.split` operates on the syntactic notation level, not directly on ordinals.
- Integer or natural-number `divmod`: standard remainder after division by a fixed integer; `VTask.split` is analogous but for ordinals modulo ω, returning a natural number remainder and an `ONote` quotient part.