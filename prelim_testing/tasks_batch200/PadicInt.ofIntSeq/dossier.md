## Object

`VTask.ofIntSeq` constructs a *p*-adic integer from a sequence of ordinary integers that is Cauchy with respect to the *p*-adic norm. Concretely, whenever a sequence `seq : ℕ → ℤ` satisfies the Cauchy condition — meaning that for any required precision the terms of the sequence eventually differ by a *p*-adic amount smaller than that precision — it converges in ℤ_[p], and this function returns the limit as an element of the *p*-adic integers.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofIntSeq : {p : ℕ} -> [hp : Fact (Nat.Prime p)] -> (seq : ℕ → ℤ) -> (h : IsCauSeq (padicNorm p) fun n => ↑(seq n)) -> ℤ_[p]
<!-- PINNED-SIGNATURE:END -->


`VTask.ofIntSeq : {p : ℕ} -> [hp : Fact (Nat.Prime p)] -> (seq : ℕ → ℤ) -> (h : IsCauSeq (padicNorm p) fun n => ↑(seq n)) -> ℤ_[p]`

The implicit argument `p` is the prime modulus fixing which *p*-adic integer ring is being used. The instance argument `hp` is the proof that `p` is prime, required to give ℤ_[p] its ring structure and norm. The argument `seq` is the integer-valued sequence; each term is an ordinary integer, viewed inside the *p*-adic rationals via the canonical embedding. The argument `h` is the proof that this sequence satisfies the Cauchy condition with respect to the *p*-adic absolute value `padicNorm p`, i.e., that consecutive (and eventually distant) terms are *p*-adically close.

## Conventions

The constructed element has *p*-adic norm at most 1, since every integer already lies in ℤ_[p] and the *p*-adic norm of any integer is at most 1; the construction automatically respects this membership condition without any additional hypothesis.

## Worked examples

- Claim: For `p = 5`, the constant sequence `seq n = 3` is Cauchy with respect to `padicNorm 5`, and `VTask.ofIntSeq seq h` lies in ℤ_[5] with the expected reduction modulo powers of 5 given by `3`.

- Claim: For `p = 2`, if `f : ℕ → ℤ` satisfies `(2 : ℤ)^i ∣ f(i+1) - f(i)` for all `i`, then the element `VTask.ofIntSeq f h` reduces modulo `2^n` to `f n` for every `n : ℕ`. (This is the content of `toZModPow_ofIntSeq_of_pow_dvd_sub`.)

- Claim: For any prime `p` and any integer `k : ℤ`, the constant sequence `fun _ => k` is Cauchy with respect to `padicNorm p`, so `VTask.ofIntSeq (fun _ => k) h` is a well-defined element of ℤ_[p].

## Boundaries

- The sequence must take values in ℤ (not merely ℚ or ℚ_[p]); the Cauchy condition is stated after embedding each integer into ℚ_[p].
- Any constant integer sequence is automatically Cauchy (differences are eventually zero, hence *p*-adically zero), so the construction never fails for constant sequences.
- The norm of the result is guaranteed to be at most 1, reflecting that every integer has *p*-adic absolute value ≤ 1; no further norm hypothesis is needed.
- The Cauchy hypothesis `h` is essential: without it, a general sequence of integers need not converge in ℤ_[p].

## Not to be confused with

- `PadicInt.ofNat` or similar coercions: those embed a single integer directly, not a sequence.
- `PadicSeq` / sequences in ℚ_[p]: `VTask.ofIntSeq` specifically requires the sequence to be integer-valued, not merely rational-valued; the Cauchy condition for integer sequences is more restrictive in type but gives the same kind of limit.
- `IsCauSeq.lim`: that produces a limit in any complete metric space, whereas `VTask.ofIntSeq` specifically packages the limit as a *p*-adic integer (with the norm ≤ 1 certificate bundled in).