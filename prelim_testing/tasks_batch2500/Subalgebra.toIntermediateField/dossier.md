## Object

Given a subalgebra `S` of a field extension `L / K` that is additionally closed under taking multiplicative inverses, `VTask.toIntermediateField` produces the corresponding **intermediate field** — a substructure of `L` that contains `K`, is closed under the field operations (including inverses of nonzero elements), and sits inside `L` as a `K`-algebra. In other words, it "upgrades" a subalgebra to an intermediate field by supplying the one axiom a subalgebra might lack: inverse-closure.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toIntermediateField : {K : Type u_1} -> {L : Type u_2} -> [Field K] -> [Field L] -> [Algebra K L] -> (S : Subalgebra K L) -> (inv_mem : ∀ x ∈ S, x⁻¹ ∈ S) -> IntermediateField K L
<!-- PINNED-SIGNATURE:END -->


`VTask.toIntermediateField : {K : Type u_1} -> {L : Type u_2} -> [Field K] -> [Field L] -> [Algebra K L] -> (S : Subalgebra K L) -> (inv_mem : ∀ x ∈ S, x⁻¹ ∈ S) -> IntermediateField K L`

`K` is the base field and `L` is the ambient (extension) field; both are implicit. The three instance arguments supply the field structures on `K` and `L` and the `K`-algebra structure on `L`. `S` is the subalgebra of `L` over `K` that one wishes to promote. `inv_mem` is the proof obligation that the subalgebra is closed under taking inverses: for every element `x` belonging to `S`, its multiplicative inverse `x⁻¹` also belongs to `S`.

## Conventions

For the element `0 ∈ L`, its "inverse" `0⁻¹` is defined to be `0` (by the junk-value convention for fields in Lean/Mathlib), so the hypothesis `inv_mem` must hold for `x = 0` as well; since `0⁻¹ = 0 ∈ S` is automatic whenever `S` contains zero (which every subalgebra does), no special case is required from the caller.

## Worked examples

- Claim: The carrier set (underlying set of elements) of `VTask.toIntermediateField S inv_mem` equals the carrier set of `S`.

- Claim: An element `x : L` belongs to `VTask.toIntermediateField S inv_mem` if and only if `x ∈ S`.

- Claim: If `S` is the `⊤` subalgebra of `L` over `K` (all of `L`), then `VTask.toIntermediateField ⊤ (fun x _ => Subfield.inv_mem _ ‹_›)` (with an appropriate inverse-closure proof) produces an intermediate field whose carrier is all of `L`, equal to `⊤ : IntermediateField K L`.

## Boundaries

- The closure-under-inverses hypothesis `inv_mem` must be supplied for **all** elements of `S`, including `0`. Because `0⁻¹ = 0` by convention, this is never a real burden — any subalgebra automatically satisfies `0⁻¹ ∈ S`.
- If `S` happens to already be an intermediate field in disguise (e.g., it is the image of some field under a ring map into `L`), this construction is the canonical way to coerce it to `IntermediateField K L`.
- There is no restriction on the size or type of `K` and `L`; the construction is completely general for field extensions in Mathlib's universe-polymorphic sense.
- The resulting `IntermediateField K L` carries the identical carrier set, addition, multiplication, and `K`-algebra structure as `S`; no elements are added or removed.

## Not to be confused with

- `Subfield.toIntermediateField`: converts a `Subfield` of `L` (which already knows about `K`-algebra structure separately) into an `IntermediateField`, rather than converting a `Subalgebra`.
- `IntermediateField.toSubalgebra`: the reverse direction — forgets the inverse-closure data from an intermediate field to obtain a subalgebra.
- `Subalgebra.toSubfield`: produces a `Subfield` (not an `IntermediateField`) from a subalgebra closed under inverses, without reference to the base field `K`.