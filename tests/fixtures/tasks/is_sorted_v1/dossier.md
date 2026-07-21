# is_sorted_v1

Fixture task for the schema validator test suite (`tests/test_task_schema.py`). Not a real
mined task -- hand-authored, deliberately not the divisor function τ used elsewhere in this
repo, to keep schema tests independent of that one worked example.

## The object

`isSorted` decides whether a `List Nat` is sorted in non-decreasing order.

## Domain and conventions

Defined on every list (no restriction). By convention the empty list is considered sorted
(vacuously true), matching the usual convention for list-sorting predicates.

## Worked examples

- `isSorted [] = true` (vacuous)
- `isSorted [1, 2, 3] = true`
- `isSorted [3, 1, 2] = false` (3 precedes 1)
- `isSorted [2, 1, 3] = false` (2 precedes 1 -- an adjacent-swap near-miss of a sorted list)
