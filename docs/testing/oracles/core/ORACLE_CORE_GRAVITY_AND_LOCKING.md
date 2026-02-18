---
doc_id: ORACLE_CORE_GRAVITY_AND_LOCKING
name: ORACLE_CORE_GRAVITY_AND_LOCKING.md
title: Core Gravity and Locking Test Oracles
kind: testing
scope: core:core
status: active
authority: normative
gate_applies_to: 1-6
phase_applies_to: all
description: Mandatory test oracles for gravity counter semantics, locking rules, and hard-drop behavior in the deterministic core.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references:
  - GAME_STATE
  - GAME_RULES
  - CORE_API
---

# ORACLE_CORE_GRAVITY_AND_LOCKING

**Tetris Core — Gravity and Locking Test Oracles (Normative)**

---

## 1. Purpose

This document defines the **mandatory automated test oracles** for:

* gravity counter behavior,
* gravity-triggered downward movement,
* lock triggering conditions,
* hard drop atomicity,
* tick ordering guarantees related to gravity and locking.

It applies only to the **pure deterministic core** (`core:core`) and is normative for Gates **1–6**.

---

## 2. Harness assumptions

The harness must be able to:

* create deterministic board configurations,
* control level and gravity parameters,
* invoke `step(state, inputs, config)`,
* inspect:

  * `active` piece position,
  * `gravity_counter`,
  * `tick_count`,
  * board state,
  * `is_game_over`,
  * emitted events (if implemented).

All tests must use deterministic seeds.

---

## 3. Gravity interval correctness

### ORACLE GL1: Gravity formula correctness

For representative levels (minimum: 1, 5, 19, 20):

Assert:

```
gravity_ticks_per_cell(level) == max(1, 20 - level)
```

Additionally:

* If `level < 1`, `gravity_ticks_per_cell` must raise `ValueError`.

---

## 4. Gravity counter semantics

### ORACLE GL2: Gravity counter increments deterministically

Given:

* no locking,
* no hard drop,
* empty space below the active piece,

On each `step()`:

* `gravity_counter` increments by exactly 1,
* `tick_count` increments by exactly 1.

No downward movement occurs until the counter reaches the gravity threshold.

---

### ORACLE GL3: Gravity triggers exactly one downward move

Given:

* active piece has empty space below,
* `gravity_counter == gravity_ticks_per_cell - 1`,

On the next `step()`:

* gravity attempts exactly one downward move,
* `origin_y` increases by exactly 1,
* `gravity_counter` resets to 0,
* no additional downward movement occurs in the same tick.

---

## 5. Locking via gravity

### ORACLE GL4: Gravity-triggered lock when blocked

Given:

* active piece has a filled cell immediately below (or bottom boundary),
* `gravity_counter == gravity_ticks_per_cell - 1`,

On next `step()`:

* downward move attempt fails,
* piece locks in the same tick,
* blocks materialize onto the board,
* gravity_counter resets to 0,
* no additional grace ticks occur.

There must be **no lock delay**.

---

### ORACLE GL5: No premature locking

Given:

* active piece has empty space below,
* `gravity_counter < gravity_ticks_per_cell - 1`,

On `step()`:

* piece must not lock,
* only gravity_counter increments.

---

## 6. Hard drop semantics

### ORACLE GL6: Hard drop is atomic

Given:

* active piece at known height,
* empty landing space below,

On `step(state, [HARD_DROP], config)`:

* active piece moves directly to lowest valid position,
* piece locks in the same tick,
* no intermediate gravity movement is observable,
* gravity processing for that tick is skipped,
* board reflects locked piece immediately.

---

### ORACLE GL7: Hard drop distance correctness

Construct deterministic board:

* known landing surface.

Assert:

* final `origin_y` equals the mathematically lowest valid y,
* locked blocks exactly match expected landing configuration.

---

### ORACLE GL8: Hard drop does not increment gravity_counter

On a tick with `HARD_DROP`:

* gravity_counter must reset (or remain at 0),
* no additional gravity increment is applied afterward in that tick.

---

## 7. Tick ordering guarantees

### ORACLE GL9: Input before gravity

Construct scenario:

* active piece has empty space below,
* gravity_counter is at threshold - 1,
* input contains `MOVE_LEFT`.

On `step()`:

1. `MOVE_LEFT` must apply first,
2. then gravity must apply based on updated position.

If gravity now causes lock due to the movement, that lock must occur.

This ensures:

* input processing precedes gravity processing.

---

### ORACLE GL10: Lock resolution completes within same tick

Given:

* gravity-triggered lock or hard drop,

In the same `step()` call:

* locking must occur,
* line clearing (if any) must occur,
* scoring update (if any) must occur,
* spawning must occur (unless game over),
* `tick_count` increments exactly once.

No multi-tick lock resolution is allowed.

(Line-clear semantics are validated in `ORACLE_CORE_LINE_CLEAR.md`.)

---

## 8. Interaction with spawn

### ORACLE GL11: Spawn occurs immediately after lock

After lock resolution (gravity or hard drop):

* new active piece must be spawned in the same tick,
* `hold_used_for_current_piece` must reset,
* `gravity_counter` must be 0 for the new piece.

---

### ORACLE GL12: No extra gravity on newly spawned piece

On a tick where spawn occurs:

* gravity must not apply again to the newly spawned piece in that same tick.

---

## 9. Game-over short circuit

### ORACLE GL13: Game-over short circuit prevents ticking

If `state.is_game_over == true`:

On `step()`:

* returned state must be identical,
* `tick_count` must not increment,
* gravity_counter must not change,
* no locking or spawning occurs.

---

## 10. Minimum required set contribution (MVP)

For MVP acceptance (Gates 1–6), at minimum:

* GL1
* GL2
* GL3
* GL4
* GL6
* GL9
* GL10
* GL13

must pass.

---
