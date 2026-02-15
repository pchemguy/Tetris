---
doc_id: INPUT_MODEL
name: INPUT_MODEL.md
title: Input Model
kind: spec
scope: core:core
status: active
authority: normative
gate_applies_to: 1-6
phase_applies_to: all
description: Defines discrete input events, per-tick ordering, and input application rules.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references:
  - GAME_STATE
---

# INPUT MODEL

**Input Semantics and Tick Integration (Normative)**

## 1. Purpose

This document defines the authoritative model for:

- how inputs are represented to the core,
- how they are applied within a tick,
- what is explicitly NOT modeled (e.g., key repeat timing).

It complements [docs/GAME_STATE.md](GAME_STATE.md) and is binding.

If a rule is missing or ambiguous, the agent must not guess.

---

## 2. Input representation

### 2.1 Discrete events (only)

The core accepts **discrete input events** per tick.

Allowed input events:

- `MOVE_LEFT`
- `MOVE_RIGHT`
- `SOFT_DROP`
- `HARD_DROP`
- `ROTATE_CW`
- `ROTATE_CCW`
- `HOLD` (only if hold is enabled)

No other inputs exist.

### 2.2 Per-tick event list

On each tick, the caller provides:

- `inputs: list[InputEvent]`

The list is **ordered**, and ordering is semantically meaningful.

The core must process inputs **in list order** (see §4).

### 2.3 No implicit repetition

There is **no implicit key repeat** inside the core.

If the user holds a key in the UI, the UI layer must translate that into repeated discrete events across ticks.

---

## 3. Input application semantics

### 3.1 Atomicity

Each input event is an independent attempted action.

For each event:

- the core computes the candidate state transition,
- if the transition is valid, it is applied,
- otherwise it is rejected with no state changes (except optional emitted events).

### 3.2 No batching / no simultaneous moves

If the input list contains multiple events, they are not treated as simultaneous.

Example:

- `MOVE_LEFT, MOVE_LEFT` can move two columns in one tick if both are valid.
- `ROTATE_CW, MOVE_LEFT` is different from `MOVE_LEFT, ROTATE_CW`.

### 3.3 Rejection behavior

If an action is rejected:

- the state is unchanged (piece, board, score, level, RNG)
- processing continues with the next event in the list.

Tick counters proceed normally.

---

## 4. Tick ordering relative to gravity

The ordering within one `step(state, inputs)` call is:

1. If `is_game_over`: return unchanged state, no events.
2. Apply all `inputs` **in order**.
3. Apply gravity according to `docs/GAME_STATE.md` §4.2.
4. If a lock occurs:
    - resolve line clears,
    - update score/level,
    - spawn next piece,
    - evaluate game over,
      all within the same tick.
5. Increment `tick_count` by exactly 1.

Hard drop special case:

- `HARD_DROP` locks immediately and triggers resolution within that tick.
- If `HARD_DROP` occurs, gravity processing for that tick is skipped.

If multiple `HARD_DROP` events appear in one tick:

- the first one that successfully applies ends the active-piece phase (lock+spawn).
- subsequent `HARD_DROP` events apply to the *new* active piece only if they occur after spawn
  within the same tick. **This is prohibited**.

Therefore:

**Constraint**: An input list must not contain more than one `HARD_DROP`.

If it does, only the first is processed and the rest are ignored (or rejected) deterministically.
The preferred behavior is: reject subsequent `HARD_DROP` events with no effect.

---

## 5. Conflicts and normalization (caller responsibilities)

The core does not normalize contradictory inputs.

Examples:

- `MOVE_LEFT, MOVE_RIGHT` may cancel out depending on collisions, but the core just applies them sequentially.
- `ROTATE_CW, ROTATE_CCW` sequentially rotates twice.

The caller (UI layer) may choose to filter inputs, but the core must not depend on it.

---

## 6. Hold input constraints (if enabled)

If hold is enabled:

- `HOLD` is processed as an input event in the same ordering rules.
- Only one successful hold is permitted per active piece:
    - the core must track and enforce `hold_used_for_current_piece`.

If the input list contains `HOLD` multiple times in a tick:

- the first may succeed,
- subsequent holds in the same tick must be rejected.

---

## 7. Optional event emissions (recommended)

If events are implemented (see GAME_STATE.md §7), the following are recommended:

- `INPUT_APPLIED(event)`
- `INPUT_REJECTED(event, reason)`

Events must be deterministic and aligned with actual state transitions.

---
