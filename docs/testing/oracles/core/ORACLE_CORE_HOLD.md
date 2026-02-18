---
doc_id: ORACLE_CORE_HOLD
name: ORACLE_CORE_HOLD.md
title: Core Oracle – Hold
kind: testing
scope: core:core
status: active
authority: normative
gate_applies_to: 1-6
phase_applies_to: all
description: Mandatory automated test oracles for hold semantics in the deterministic core (when hold is enabled).
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references:
  - GAME_RULES
  - GAME_STATE
  - INPUT_MODEL
  - ERROR_HANDLING
  - CORE_API
---

# ORACLE_CORE_HOLD

**Core Oracle – Hold Semantics (Normative)**

## 1. Purpose

This document defines the **mandatory automated test oracles** for hold behavior in the deterministic core.

Hold is **optional** at the rules/spec layer; therefore this oracle is **conditionally applicable**:

- If hold is disabled by configuration, all hold-related behavior must be rejected or treated as an input error as specified by `CORE_API` and `ERROR_HANDLING`.
- If hold is enabled, the oracles in this document must pass.

This oracle is normative for Gates **1–6**.

---

## 2. Applicability and configuration requirements

### ORACLE H0: Hold-gating behavior is explicit

Tests must cover both configurations:

1. `enable_hold = false`
2. `enable_hold = true`

### ORACLE H0.1: Hold field presence is stable

`GameState` must contain:

- `hold_piece: TetrominoType | None`
- `hold_used_for_current_piece: bool`

These fields must exist regardless of whether hold is enabled.

---

## 3. Hold disabled behavior (strictness boundary)

### ORACLE H1: HOLD is invalid when disabled

Given `enable_hold = false`, and `inputs` includes `HOLD`:

- If `strict_input = true`: `step()` must raise (caller error).
- If `strict_input = false`: `HOLD` must be rejected with no effect.

In both cases:

- No state progression other than allowed tick/gravity semantics may occur before the error/rejection rule applies.
- No partial hold side-effects are permitted.

---

## 4. Hold enabled behavior (core semantics)

All oracles below assume `enable_hold = true`.

### ORACLE H2: First hold stores active and spawns next

Given:

- `hold_piece is None`
- `hold_used_for_current_piece == false`

When processing `HOLD`:

- `hold_piece` becomes the pre-hold active piece type.
- The active piece becomes the pre-hold `next_piece`.
- A new `next_piece` is drawn deterministically from the RNG state.
- The new active piece is spawned at the canonical spawn position and rotation:
  - `origin_x == 3`, `origin_y == 0`, `rotation == R0`
- `hold_used_for_current_piece` becomes `true`.

### ORACLE H3: Subsequent hold swaps active with hold slot

Given:

- `hold_piece is not None`
- `hold_used_for_current_piece == false`

When processing `HOLD`:

- active piece type and hold piece type are swapped:
  - `hold_piece` becomes previous active type
  - active becomes previous `hold_piece`
- active piece is spawned/reset at:
  - `origin_x == 3`, `origin_y == 0`, `rotation == R0`
- `next_piece` remains unchanged by the swap itself.
- `hold_used_for_current_piece` becomes `true`.

---

## 5. Once-per-piece rule

### ORACLE H4: Hold may succeed at most once per active piece

Given `hold_used_for_current_piece == true`, when processing `HOLD`:

- `HOLD` must be rejected (normal rejection, not error).
- The state must remain unchanged except for tick/gravity counters as permitted by `GAME_STATE` ordering.

This must be tested for both cases:

- after first-hold store scenario (H2)
- after swap-hold scenario (H3)

### ORACLE H5: Lock resets hold-used flag for the next piece

After a piece locks and the next piece is spawned:

- `hold_used_for_current_piece` must be reset to `false` for the newly spawned active piece.

(If spawn immediately triggers game over, the flag behavior is not semantically important, but must remain deterministic.)

---

## 6. Interaction with per-tick input ordering

### ORACLE H6: HOLD is applied in list order like any other input

Given a tick input list, `HOLD` must be processed in sequence, with observable effect on subsequent inputs.

Mandatory scenarios:

1. `HOLD` then `MOVE_LEFT` in the same tick:
   - movement applies to the post-hold active piece.
2. `MOVE_LEFT` then `HOLD`:
   - movement applies to the pre-hold active piece, then hold acts on the moved piece.

### ORACLE H7: Multiple HOLD events in a tick are handled deterministically

Given an input list containing multiple `HOLD` events in one tick:

- The first `HOLD` may succeed (if `hold_used_for_current_piece == false`).
- All subsequent `HOLD` events in the same tick must be rejected due to the once-per-piece rule.

This must not raise an error by default.

(If you later decide “multiple HOLD per tick is caller error”, that policy must be specified in `INPUT_MODEL` and/or `ERROR_HANDLING`, then this oracle must be updated accordingly.)

---

## 7. Collision and spawn constraints

Hold is effectively a “respawn” operation. Therefore:

### ORACLE H8: Hold-induced spawn obeys collision and game-over semantics

If after a hold operation the spawned active piece collides immediately at spawn:

- `is_game_over` must become true deterministically (same as normal spawn collision rule).
- No partial state corruption is permitted.

This oracle does not re-define collision rules; it asserts that hold respects them.

---

## 8. Determinism obligations

### ORACLE H9: Hold behavior is deterministic under seed

Given:

- fixed seed,
- identical starting state,
- identical inputs including hold events,

All of the following must match across runs:

- hold slot contents over time,
- active piece sequence over time,
- next piece sequence over time,
- resulting board outcomes after locks.

---

## 9. Required minimum test set

At minimum, the test suite must include:

- H1 (disabled hold strictness)
- H2 (first hold stores and spawns next)
- H3 (swap hold)
- H4 (once-per-piece rejection)
- H5 (reset on lock)
- H6 (input ordering interaction)
- H7 (multi-hold same tick determinism)
- H9 (determinism with seed)

H8 is mandatory if your framework includes any spawn-collision tests; it is strongly recommended regardless.

---
