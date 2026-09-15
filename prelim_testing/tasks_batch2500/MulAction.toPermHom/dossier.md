## VTask.toPermHom

### Object

Given a group `G` acting on a set `α` (by left multiplication), `VTask.toPermHom G α` is the canonical **group homomorphism** from `G` to the symmetric group `Equiv.Perm α` (the group of all bijections `α → α`). It sends each group element `g : G` to the permutation of `α` given by the action of `g`, i.e., the bijection `x ↦ g • x`. The fact that this is a group homomorphism encodes both that the identity acts as the identity permutation and that composing actions corresponds to composing permutations.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toPermHom : (G : Type u_1) -> (α : Type u_5) -> [Group G] -> [MulAction G α] -> G →* Equiv.Perm α
<!-- PINNED-SIGNATURE:END -->


The first argument `G` is the group doing the acting. The second argument `α` is the set (type) being acted upon. The `Group G` instance supplies the group structure on `G`. The `MulAction G α` instance supplies the left group action of `G` on `α`. The result is a monoid (group) homomorphism from `G` to `Equiv.Perm α`.

### Conventions

No special junk-value or edge conventions are declared: the homomorphism is defined for every group `G` and every type `α` equipped with a `MulAction G α` instance, with no domain restrictions.

### Worked examples

- Claim: For the natural action of `ZMod 3` (as an additive group, but thinking multiplicatively via `AddAction`) — or more concretely, for a group acting on itself by left multiplication, the image of the identity element under `VTask.toPermHom` is the identity permutation of `α`.

- Claim: For `G = Equiv.Perm α` acting on `α` by evaluation (the canonical action), `VTask.toPermHom (Equiv.Perm α) α` is injective, because distinct permutations must act differently on at least one point.

- Claim: For any group `G` acting on `α`, applying `VTask.toPermHom G α` to a product `g * h` equals the composition of the permutations for `g` and `h` separately, i.e., `VTask.toPermHom G α (g * h) = VTask.toPermHom G α g * VTask.toPermHom G α h`.

- Claim: The kernel of `VTask.toPermHom G α` consists exactly of those `g : G` that act trivially on every element of `α`, i.e., `g • x = x` for all `x : α`.

### Boundaries

- When the action is trivial (every group element acts as the identity), `VTask.toPermHom G α` maps every element to the identity permutation; it is the zero homomorphism.
- When `α` is empty, every permutation of `α` is the identity, so `VTask.toPermHom G α` maps every element to the unique permutation of the empty type.
- When `G` is the trivial group, the homomorphism is trivially the zero map.
- The homomorphism is not in general injective: its kernel can be nontrivial if multiple group elements act identically on all of `α`.

### Not to be confused with

- `MulAction.toPerm`: the underlying bare function `G → Equiv.Perm α` (sending `g` to its permutation), without the homomorphism structure bundled.
- `Equiv.Perm α` itself: the target group of all bijections on `α`, not the homomorphism into it.
- A right-action analogue: `VTask.toPermHom` is specifically for left `MulAction`s; a right action would give a homomorphism into the opposite group.