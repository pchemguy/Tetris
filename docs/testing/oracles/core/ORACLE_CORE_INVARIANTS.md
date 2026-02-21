---
doc_id: ORACLE_CORE_INVARIANTS
name: ORACLE_CORE_INVARIANTS.md
title: Core State Invariant Test Oracles
status: active
authority: normative
description: Mandatory cross-cutting state invariants that must hold after every successful step.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references: [GAME_STATE, ERROR_HANDLING, CORE_API]
---

# ORACLE_CORE_INVARIANTS

**Tetris Core — Cross-Cutting State Invariant Test Oracles (Normative)**

---

## 1. Purpose

This document defines the **mandatory automated invariant checks** that must hold:

* after every successful `step()` call,
* after `new_game()`,
* after any lock/clear/spawn transition.

These invariants are global safety guarantees.
If any invariant fails, the implementation is incorrect.

This document applies only to the **pure deterministic core** (`core:core`) and is normative for Gates **1–6**.

---

## 2. General rule

After every call to:

```
new_game(config)
step(state, inputs, config)
```

the resulting `GameState` must satisfy all invariants defined below.

If `strict_state == true`, violations must raise exceptions.

---

## 3. Board invariants

### ORACLE X1: Board shape

After every step:

* Board has exactly 20 rows.
* Each row has exactly 10 columns.

### ORACLE X2: Board cell domain

For every cell:

```
board[y][x] ∈ {0, 1}
```

No other values permitted.

### ORACLE X3: No floating corruption

Board must remain rectangular and index-safe:

* No missing rows,
* No variable-length rows,
* No negative indexing artifacts.

---

## 4. Active piece invariants

### ORACLE X4: Active piece exists unless game over

If:

```
is_game_over == false
```

Then:

* `active` exists,
* `blocks_for(active)` returns exactly 4 unique coordinates.

### ORACLE X5: Active piece within bounds

If not game over:

For each block `(x, y)` of active piece:

* `0 ≤ x ≤ 9`
* `0 ≤ y ≤ 19`
* Block must not overlap filled board cell.

### ORACLE X6: No ghost overlap

Active piece blocks must not overlap filled board cells.

If overlap occurs → invariant violation.

---

## 5. Scalar invariants

### ORACLE X7: Score validity

* `score >= 0`

### ORACLE X8: Lines cleared validity

* `lines_cleared_total >= 0`

### ORACLE X9: Level validity

* `level >= 1`

Additionally:

```
level == 1 + floor(lines_cleared_total / 10)
```

must always hold.

---

## 6. Tick invariants

### ORACLE X10: Tick monotonicity

If:

```
previous_state.is_game_over == false
```

Then:

```
new_state.tick_count == previous_state.tick_count + 1
```

If:

```
previous_state.is_game_over == true
```

Then:

```
new_state.tick_count == previous_state.tick_count
```

### ORACLE X11: Gravity counter range

After every step:

```
0 ≤ gravity_counter < gravity_ticks_per_cell(level)
```

---

## 7. RNG invariants

### ORACLE X12: Bag contents validity

At all times:

* Bag contains 0–7 elements.
* All elements ∈ {I, O, T, S, Z, J, L}.
* No duplicates within a bag instance.

### ORACLE X13: Deterministic continuity

Given identical:

* initial state,
* input sequence,
* seed,

Resulting:

* active pieces,
* board states,
* RNG state

must be identical across runs.

---

## 8. Preview invariants

### ORACLE X14: Next piece always defined

At all times:

```
next_piece != None
```

Even immediately after game over.

---

## 9. Hold invariants (if enabled)

### ORACLE X15: Hold type validity

If `hold_piece` is not None:

* It must be a valid `TetrominoType`.

### ORACLE X16: Hold usage reset

After locking and spawning a new piece:

```
hold_used_for_current_piece == false
```

---

## 10. Immutability invariant

### ORACLE X17: Step returns new state

Calling:

```
new_state = step(old_state, ...)
```

Must satisfy:

* `new_state is not old_state`
* Board tuple identity must differ if mutated
* No externally observable mutable aliasing

Functional semantics required.

---

## 11. No silent corruption invariant

### ORACLE X18: Rejected action preserves structural fields

If an input is rejected:

* Board unchanged
* Active piece unchanged
* Score unchanged
* RNG unchanged
* Only tick_count and gravity_counter may evolve per defined ordering

---

## 12. Forbidden behavior

The following immediately fails this oracle:

* Active piece overlapping board cells.
* Gravity counter outside valid range.
* Level inconsistent with total lines.
* RNG bag containing invalid or duplicate elements.
* State mutation after game over.
* Sharing mutable board structures across states.

---

## 13. Minimum required set (MVP)

For MVP acceptance (Gates 1–6), at minimum:

* X1
* X4
* X7
* X9
* X10
* X11
* X14

must pass.

Full correctness requires all invariants.

---
