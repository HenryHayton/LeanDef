## VTask.maximalRealSubfield

### Object

Given a field `K` (typically a number field), the **maximal real subfield** is the subfield of `K` consisting precisely of those elements that are fixed by complex conjugation under every ring homomorphism from `K` into the complex numbers ℂ. Equivalently, an element `x ∈ K` belongs to this subfield if and only if, for every embedding `φ : K →+* ℂ`, the image `φ(x)` is a real number (i.e., equals its own complex conjugate). This subfield is totally real, and it contains every other totally real subfield of `K`; it is, in a precise sense, the largest totally real subfield.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.maximalRealSubfield : (K : Type u_2) -> [Field K] -> Subfield K
<!-- PINNED-SIGNATURE:END -->


`VTask.maximalRealSubfield : (K : Type u_2) -> [Field K] -> Subfield K`

The explicit argument `K` is the ambient field whose maximal real subfield is being constructed. The implicit `Field K` instance supplies the field structure on `K` needed to form a subfield.

### Conventions

No special junk-value or boundary conventions are declared for this definition: it is a total construction producing a `Subfield K` for any field `K`, with no distinguished degenerate input needing special treatment.

### Worked examples

- Claim: For `K = ℝ`, every element of `ℝ` belongs to `VTask.maximalRealSubfield ℝ`, since all embeddings `ℝ →+* ℂ` send real numbers to real numbers, so `VTask.maximalRealSubfield ℝ = ⊤` as a subfield of `ℝ`.

- Claim: For `K = ℂ`, an element `z : ℂ` belongs to `VTask.maximalRealSubfield ℂ` if and only if `star z = z`, i.e., `z` is a real number; so the maximal real subfield of `ℂ` is (isomorphic to) `ℝ`.

- Claim: For a cyclotomic field `K = ℚ(ζₙ)`, the maximal real subfield is `ℚ(ζₙ + ζₙ⁻¹)`, the totally real subfield fixed by complex conjugation.

- Claim: If `K` is itself totally real (all embeddings into ℂ have image in ℝ), then `VTask.maximalRealSubfield K = ⊤`.

### Boundaries

- When `K` has **no** ring homomorphisms to ℂ (e.g., a field of positive characteristic), the condition `∀ φ : K →+* ℂ, star (φ x) = φ x` is vacuously true for every `x`, so `VTask.maximalRealSubfield K = ⊤` (the whole field).
- When `K = ℚ`, the maximal real subfield is all of `ℚ` itself, since `ℚ` is totally real.
- The subfield is never empty: it always contains `0` and `1`, and more generally all of `ℚ` (or the prime subfield) in characteristic zero.

### Not to be confused with

- **`Subfield.center K`**: the center of a division ring, which captures commutativity rather than reality under complex embeddings.
- **`IntermediateField.fixedField`** (fixed field of a subgroup of automorphisms): a related but more general construction; the maximal real subfield is the fixed field of complex conjugation on `K`, but expressed via all complex embeddings rather than automorphisms of `K` itself.
- **`IsTotallyReal`** (the predicate asserting a field is totally real): this is a *property* of a field, not a subfield construction; `VTask.maximalRealSubfield K` is the largest subfield of `K` satisfying this property.