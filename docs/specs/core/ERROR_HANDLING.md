---
doc_id: ERROR_HANDLING
name: ERROR_HANDLING.md
title: Error Handling
kind: spec
scope: core:core
status: active
authority: normative
gate_applies_to: 1-6
phase_applies_to: all
description: Defines rejection vs error semantics and invariant enforcement policy.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references:
  - GAME_STATE
---

# ERROR HANDLING

**Core Error Handling and Rejection Policy (Normative)**

## 1. Purpose

This document defines:

- what is considered an error vs a rejected action,
- how invalid states/inputs are handled,
- what must be asserted/validated by the core.

It prevents silent corruption and “best-effort guessing.”

---

## 2. Definitions

### 2.1 Rejected action (normal)

A rejected action is a user input that cannot be applied due to rules, e.g.:

- moving into a wall,
- rotating into collision,
- holding twice per piece,
- soft dropping into an occupied cell.

Rejections are normal and must:

- not raise exceptions,
- not mutate the state (except tick/gravity counters as usual),
- optionally emit deterministic rejection events.

### 2.2 Error (exceptional)

An error is a violation of the core’s API contract or state invariants, e.g.:

- invalid board dimensions,
- unknown tetromino type,
- invalid rotation enum,
- duplicate blocks in a shape definition,
- negative score or level < 1,
- RNG/bag containing invalid contents.

Errors indicate a bug in caller or implementation and must:

- fail fast (raise an exception) in debug/test modes,
- never be silently ignored.

---

## 3. Input validation

### 3.1 Unknown input events

If the core receives an input event not in the allowed set:

- this is an **error**, not a rejection.
- raise an exception (e.g., `ValueError`).

### 3.2 Multiple hard drops in a tick

Per [docs/INPUT_MODEL.md](INPUT_MODEL.md), multiple `HARD_DROP` events in the same tick are invalid input.

Handling rule:

- This is treated as a **caller error**.
- Raise an exception in debug/test contexts.

If you choose to support “robust mode” (not required for MVP), it must be explicit and default must remain strict. In robust mode, only the first `HARD_DROP` is applied and the rest are rejected.

**Default required behavior for this project: strict (exception).**

---

## 4. State validation

### 4.1 Mandatory invariants (must always hold)

After every successful `step()` call (even if all inputs were rejected), the core must satisfy:

- Board is 20×10.
- Board cells are boolean/0/1.
- `score >= 0`
- `lines_cleared_total >= 0`
- `level >= 1`
- `tick_count` increases by exactly 1 per step unless `is_game_over` is true
  (see GAME_STATE.md ordering; if game over short-circuits, tick_count remains unchanged).
- RNG/bag contain only valid tetromino types.
- `next_piece` is always defined unless `is_game_over` is true due to spawn collision that tick
  (even then, next_piece should remain defined for inspection; preferred).

If invariants fail, raise an exception.

### 4.2 Active piece validity

If `is_game_over` is false:

- active piece must exist,
- it must occupy exactly 4 blocks,
- those blocks must not collide with filled board cells,
- all blocks must be within bounds.

If any of these fail, raise an exception.

If `is_game_over` is true:

- active piece may be retained for debugging, but no further state progression occurs.

---

## 5. Serialization (recommended for tests)

State should be serializable to a JSON-compatible form for:

- golden test snapshots,
- regression debugging.

Serialization errors (e.g., non-serializable RNG state) are considered implementation errors.

---

## 6. Logging and diagnostics (recommended)

The core may optionally emit structured events ([GAME_STATE.md](GAME_STATE.md) §7).
These are preferred over ad-hoc logging and are test-friendly.

No printing to stdout/stderr in the core.

---

## 7. Required policy summary (MVP gate)

- Collision-based inability to apply a user action: **reject, do not error**.
- Unknown input event: **error**.
- Invalid state/invariants: **error**.
- Multiple `HARD_DROP` in one tick: **error** (strict mode required).
- Multiple `HOLD` in one tick: **reject after first** (normal), but may also be treated as caller error if you choose strictness; default is rejection.

---

## Notes (important)

* `ERROR_HANDLING.md` **intentionally prefers strictness** because this project is about evaluating agentic correctness, not building a forgiving product.
* The one exception is repeated `HOLD` in a tick: I defaulted to *reject after first* because it’s harmless and consistent with the “rejected action” model. If you want that strict too, we can flip it to exception.
