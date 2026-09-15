## VTask.mk

### Object

Given a commutative, linearly ordered group `M` that satisfies the ordered-monoid axioms, and given any element `a` of `M` that is not the identity element `1`, `VTask.mk a h` produces the *finite Archimedean class* of `a`. A finite Archimedean class is the Archimedean equivalence class of a non-identity element: two non-identity elements belong to the same class when each is dominated (in the Archimedean sense) by a sufficiently high power of the other. The "finite" qualifier distinguishes these classes from the degenerate "top" class that would otherwise be assigned to the identity.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mk : {M : Type u_1} -> [CommGroup M] -> [LinearOrder M] -> [IsOrderedMonoid M] -> (a : M) -> (h : a ≠ 1) -> FiniteMulArchimedeanClass M
<!-- PINNED-SIGNATURE:END -->


The type-class arguments supply the algebraic structure: `CommGroup M` gives the group operations, `LinearOrder M` gives a total ordering, and `IsOrderedMonoid M` ties the two together. The explicit argument `a : M` is the element whose Archimedean class is being wrapped. The argument `h : a ≠ 1` is the proof that `a` is not the identity, which is required to guarantee that the resulting class is genuinely finite (non-top).

### Conventions

There are no special junk-value or boundary conventions for this constructor: it is only defined when the non-identity proof `h` is supplied, so there is no "default" behavior for the identity element.

### Worked examples

- Claim: In the additive integers viewed multiplicatively (i.e., `ℤ` as a `CommGroup` under multiplication, or more naturally `ℤ` under addition with the ordered structure), calling `VTask.mk a h` for any non-zero integer `a` yields a value of type `FiniteMulArchimedeanClass ℤ`.

- Claim: For the ordered commutative group `ℤ` (written multiplicatively), the elements `2` and `4` have the same finite Archimedean class, because each is an Archimedean power-multiple of the other; so `VTask.mk 2 h₁` and `VTask.mk 4 h₂` are equal as values of `FiniteMulArchimedeanClass ℤ`.

- Claim: For any non-identity element `a` in a linearly ordered commutative group, `VTask.mk a h` is a well-typed term of `FiniteMulArchimedeanClass M`.

### Boundaries

- The constructor cannot be applied to the identity element `1`; the proof obligation `h : a ≠ 1` must be discharged before the constructor can be used.
- When the underlying group has only one Archimedean class (e.g., the integers, which are Archimedean), all applications of `VTask.mk` to any non-identity element yield the same `FiniteMulArchimedeanClass`.
- In a non-Archimedean ordered group (e.g., a lexicographic product), distinct non-identity elements may produce distinct finite Archimedean classes, reflecting the richer structure of the Archimedean quotient.

### Not to be confused with

- `MulArchimedeanClass.mk`: constructs the full (possibly top) Archimedean class of any element, including the identity; `VTask.mk` adds the finiteness guarantee by requiring `a ≠ 1`.
- `FiniteMulArchimedeanClass` as a type: the type itself is the collection of all finite Archimedean classes; `VTask.mk` is the constructor that produces a *particular* element of that type.
- Archimedean class equality: two calls `VTask.mk a h` and `VTask.mk b h'` may be equal even if `a ≠ b`, because Archimedean equivalence is coarser than equality of group elements.