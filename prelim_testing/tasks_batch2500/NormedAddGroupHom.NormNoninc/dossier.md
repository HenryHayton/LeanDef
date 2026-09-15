## VTask.NormNoninc

### Object

A predicate on a normed additive group homomorphism `f : V → W` asserting that `f` is *norm-nonincreasing*: for every vector `v` in `V`, the norm of the image `f v` in `W` is at most the norm of `v`. In other words, `f` does not stretch any element in terms of its norm.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.NormNoninc : {V : Type u_1} -> {W : Type u_2} -> [SeminormedAddCommGroup V] -> [SeminormedAddCommGroup W] -> (f : NormedAddGroupHom V W) -> Prop
<!-- PINNED-SIGNATURE:END -->


The implicit type arguments `V` and `W` are the source and target seminormed additive commutative groups, respectively. The instance arguments supply the seminorm structures on `V` and `W`. The explicit argument `f` is the normed additive group homomorphism being tested for the norm-nonincreasing property.

### Conventions

No special junk-value or boundary conventions are declared for this predicate: it is a straightforward universal statement that applies uniformly to every homomorphism, with no degenerate inputs producing conventionally assigned truth values.

### Worked examples

- Claim: The zero homomorphism `0 : NormedAddGroupHom V W` satisfies `VTask.NormNoninc 0`, since `‖0 v‖ = 0 ≤ ‖v‖` for all `v`.

- Claim: The identity homomorphism `NormedAddGroupHom.id V` satisfies `VTask.NormNoninc (NormedAddGroupHom.id V)`, since `‖id v‖ = ‖v‖ ≤ ‖v‖` for all `v`.

- Claim: If `f : NormedAddGroupHom V W` and `g : NormedAddGroupHom W X` both satisfy `VTask.NormNoninc`, then their composition `g.comp f` also satisfies `VTask.NormNoninc`, because `‖g (f v)‖ ≤ ‖f v‖ ≤ ‖v‖`.

### Boundaries

- The predicate holds trivially for any homomorphism from the zero (trivial) group, since the only element is `0` and `‖f 0‖ = 0 ≤ 0 = ‖0‖`.
- Because only a seminorm (not a full norm) is required, `‖v‖ = 0` does not force `v = 0`; thus the bound `‖f v‖ ≤ ‖v‖ = 0` still meaningfully constrains the image when `‖v‖ = 0`.
- The predicate is strictly weaker than requiring `f` to be a norm-preserving isometry; an isometry additionally demands `‖f v‖ = ‖v‖`.

### Not to be confused with

- **Norm-nonincreasing vs. norm-bounded (operator norm ≤ 1):** For linear maps between normed spaces the two notions coincide, but `NormNoninc` is stated pointwise and does not refer to the operator norm directly.
- **`NormedAddGroupHom.NormBound`:** A related predicate asserting that the operator norm is bounded by a specific constant `C`; `NormNoninc` corresponds to the special case `C = 1` but is defined without referencing the operator norm.
- **Lipschitz maps with constant 1 (nonexpansive maps):** A seminormed additive group homomorphism that is norm-nonincreasing is automatically 1-Lipschitz, but the Lipschitz predicate is more general and applies to arbitrary metric spaces.