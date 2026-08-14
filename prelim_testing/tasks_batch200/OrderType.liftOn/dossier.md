## 1. Object

A *quotient-lifting* operator: given an `OrderType` (an equivalence class of linearly ordered types under order-isomorphism) and a function `f` defined uniformly on all linearly ordered types, `VTask.liftOn` produces a well-defined value of type `δ` by evaluating `f` at any representative of the equivalence class. The key guarantee is that the result does not depend on which representative is chosen, as enforced by the compatibility condition `c`.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.liftOn : {δ : Sort v} -> (o : OrderType.{u_1}) -> (f : (α : Type u_1) → [LinearOrder α] → δ) -> (c :
    ∀ (α : Type u_1) [inst : LinearOrder α] (β : Type u_1) [inst_1 : LinearOrder β],
      OrderType.type α = OrderType.type β → f α = f β) -> δ
<!-- PINNED-SIGNATURE:END -->


`{δ : Sort v} -> (o : OrderType.{u_1}) -> (f : (α : Type u_1) → [LinearOrder α] → δ) -> (c : ∀ (α : Type u_1) [inst : LinearOrder α] (β : Type u_1) [inst_1 : LinearOrder β], OrderType.type α = OrderType.type β → f α = f β) -> δ`

The implicit argument `δ` is the target sort into which the result lives. The argument `o` is the `OrderType` on which the function is being defined — the quotient element whose representative will be used. The argument `f` is the function to be descended to order types: it takes any linearly ordered type and produces a value of `δ`. The argument `c` is the compatibility (well-definedness) proof: it asserts that whenever two linearly ordered types `α` and `β` have the same `OrderType`, `f` gives the same result on both.

## 3. Conventions

There are no junk-value or boundary conventions to declare: the function is total on all valid inputs and every argument is fully constrained by the types.

## 4. Worked examples

- Claim: If `f` maps every linearly ordered type to its `OrderType`, and `o = VTask.liftOn (OrderType.type ℕ) (fun α [LinearOrder α] => (0 : ℕ)) (fun α _ β _ _ => rfl)`, then the result equals `0`.

- Claim: For a concrete linearly ordered type `γ`, evaluating `VTask.liftOn (OrderType.type γ) f c` reduces to `f γ`. That is, `VTask.liftOn (OrderType.type γ) f c = f γ` (this is the content of the theorem `liftOn_type`).

- Claim: If `f` is the constant function returning `true : Bool` for every linearly ordered type, and `c` is the trivial proof that `true = true`, then `VTask.liftOn o f c = true` for every `OrderType` `o`.

## 5. Boundaries

- The function is total: every `OrderType`, every compatible `f`, and every proof `c` yield a result.
- The canonical computation rule is: when `o` is of the form `OrderType.type γ` for some concrete linearly ordered type `γ`, the result equals `f γ` directly. This is the only reduction that occurs in practice.
- The compatibility condition `c` is not optional: without it, the result would be ill-defined because an `OrderType` may be represented by many non-isomorphic-looking but order-isomorphic types.
- Universe levels: `α` and `β` must live in the same universe `u_1` as the `OrderType`, and `δ` may live in any `Sort v`.

## 6. Not to be confused with

- `VTask.liftOn₂`: the two-argument variant, which lifts a binary function on pairs of linearly ordered types to a function on pairs of `OrderType`s.
- `Quotient.liftOn`: the general quotient-lift on an arbitrary `Setoid`; `VTask.liftOn` is the specialization to the `OrderType` quotient.
- `OrderType.type`: the constructor that sends a concrete linearly ordered type into its `OrderType` equivalence class; the inverse direction of `VTask.liftOn`.