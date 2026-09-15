## VTask.stdPart

### Object

Given an ordered field `K` (typically a non-Archimedean or hyperreal-style extension of ℝ), `VTask.stdPart x` returns the **standard part** of `x`: the unique real number that differs from `x` by at most an infinitesimal amount. Intuitively, it is the "shadow" or "nearest real number" to a finite (i.e., bounded) element of `K`. If `x` is infinite (unbounded), the function returns the junk value `0 : ℝ`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.stdPart : {K : Type u_1} -> [LinearOrder K] -> [Field K] -> [IsOrderedRing K] -> (x : K) -> ℝ
<!-- PINNED-SIGNATURE:END -->


`VTask.stdPart : {K : Type u_1} -> [LinearOrder K] -> [Field K] -> [IsOrderedRing K] -> (x : K) -> ℝ`

The implicit type argument `K` is the ordered field whose elements are being measured. The three instance arguments supply a linear order, field structure, and ordered-ring compatibility on `K`. The explicit argument `x` is the element of `K` whose standard part is being computed. The return type `ℝ` is the real numbers.

### Conventions

For any infinite input `x` (one that is not a finite element, i.e., is unbounded with respect to the reals), the function returns the junk value `0 : ℝ`. This is a conventional choice to make the function total; no mathematical meaning is attached to `0` in this case.

### Worked examples

- Claim: For a finite element `x : K` that is exactly the image of a real number `r`, `VTask.stdPart x` equals `r`.

- Claim: For an infinite element `x : K` (one with no nearest real), `VTask.stdPart x = 0` by convention (junk value).

- Claim: If `x` and `y` are finite elements of `K` with `x - y` infinitesimal, then `VTask.stdPart x = VTask.stdPart y`.

- Claim: `VTask.stdPart` preserves addition on finite elements: for finite `x y : K`, `VTask.stdPart (x + y) = VTask.stdPart x + VTask.stdPart y`.

### Boundaries

- **Infinite inputs**: Any element of `K` that is infinite (larger in absolute value than every real number) receives the junk output `0 : ℝ`. This is a definitional convention and carries no mathematical significance.
- **Exactly real inputs**: If `x` is the image of an actual real number `r` under the canonical embedding of ℝ into `K`, then `VTask.stdPart x = r` exactly, with zero infinitesimal error.
- **Infinitesimal inputs**: An infinitesimal element (nonzero but smaller in absolute value than every positive real) is finite, and its standard part is `0 : ℝ`—not a junk value, but genuinely zero.
- **Negative finite elements**: The function handles negative finite elements correctly; the standard part of a negative finite element is the corresponding negative real number.

### Not to be confused with

- **The residue map / reduction mod the maximal ideal**: That map sends finite elements to the residue field, which need not be ℝ; `VTask.stdPart` specifically targets ℝ.
- **Round or floor functions**: Those send a real number to a nearby integer; `VTask.stdPart` sends a hyperreal/non-Archimedean element to a nearby *real* number.
- **Norm or absolute value**: Those measure the size of an element; `VTask.stdPart` produces the actual real shadow, including sign.
